# python src/main.py --input "$INPUT_FILE" --output "$OUTPUT_FILE" --loss-function "$LOSS_FUNCTION" --makeplots "$MAKE_PLOTS"

#### imports
import xarray as xr
import numpy as np
import argparse
import pandas as pd
import os
import random
import matplotlib.pyplot as plt

import time


def load_input_data(file_path):
    """Load asset data from CSV file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    df = pd.read_csv(file_path)[["asset_id", "latitude", "longitude", "asset_type"]]
    return df.drop_duplicates("asset_id").rename(
        columns={"latitude": "lat", "longitude": "lon"}
    )


def save_output_data(df, file_path):
    """Save productivity loss results to a CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f";-) Results saved to: {file_path}")


def barplots(df_long_scaled, scenarios, project):
    # Select 25 random asset_ids from the entire long-format DataFrame
    sample_ids = random.sample(list(df_long_scaled["asset_id"].unique()), 25)

    # Create a subplot with one row per scenario
    f, ax = plt.subplots(
        len(scenarios), 1, figsize=(10, 3 * len(scenarios)), sharex=True
    )

    for i, scenario in enumerate(scenarios):
        # Filter for the current scenario, the sampled asset_ids, and only the years 2025 and 2100.
        data = df_long_scaled[
            (df_long_scaled["scenario"] == scenario)
            & (df_long_scaled["asset_id"].isin(sample_ids))
            & (df_long_scaled["year"].isin([2025, 2100]))
        ].copy()

        # Pivot so each asset_id is one row, and columns become "2025_median", "2025_minimum", etc.
        data_pivot = data.pivot(
            index="asset_id", columns="year", values=["median", "minimum", "maximum"]
        )
        # Flatten the MultiIndex columns to single strings.
        data_pivot.columns = [f"{year}_{stat}" for stat, year in data_pivot.columns]
        data_pivot = data_pivot.reset_index()

        # Define x-axis positions for each asset.
        x = np.arange(len(data_pivot))

        # Define error bars for 2025 and 2100.
        err_2025 = [
            np.abs(data_pivot["2025_median"] - data_pivot["2025_minimum"]),
            np.abs(data_pivot["2025_maximum"] - data_pivot["2025_median"]),
        ]
        err_2100 = [
            np.abs(data_pivot["2100_median"] - data_pivot["2100_minimum"]),
            np.abs(data_pivot["2100_maximum"] - data_pivot["2100_median"]),
        ]

        bar_width = 0.4
        # Select the appropriate axis handle.
        a = ax[i] if len(scenarios) > 1 else ax

        # Plot bars with error bars for both years.
        a.bar(
            x - bar_width / 2,
            data_pivot["2025_median"],
            yerr=err_2025,
            width=bar_width,
            capsize=5,
            label="2020",
            color="xkcd:grey",
        )
        a.bar(
            x + bar_width / 2,
            data_pivot["2100_median"],
            yerr=err_2100,
            width=bar_width,
            capsize=5,
            label="2100",
            color="xkcd:black",
        )

        a.set_xticks(x)
        a.set_xticklabels(data_pivot["asset_id"], rotation=45, fontsize=6, ha="right")
        a.set_ylim(0.01, 100)
        a.set_yscale("log")
        a.set_ylabel("Productivity Loss (%)")
        a.legend()
        a.set_title(scenario)

    plt.savefig(f"figures/{project}_barplots.png", dpi=300, bbox_inches="tight")


def main(input_file, loss_function, save_figures, scenarios, project):
    ####### deal with files
    asset_map = pd.read_csv("src/asset_map.csv")  # load asset mapping
    df_in = load_input_data(input_file)  # Load input CSV

    ## load aircon
    aircon = xr.open_zarr(
        "s3://hazard-science-data/productivity_loss_v2/aircon/AirCon_SSPs.zarr/"
    )
    aircon = aircon.sel(SSP="2.0").isel(year=0)["ac_penetration"]

    ## load loss zarrs
    ds_dict = {}
    ds_2020 = {}
    for intensity in ["low", "moderate", "high"]:
        ds_2020[intensity] = xr.open_zarr(
            f"s3://hazard-science-data/productivity_loss_v2/climate_outputs/observations/ERA5_{loss_function}_productivity_loss_{intensity}.zarr.zarr/"
        )

    for scenario in scenarios:
        ds_dict[scenario] = {}
        for intensity in ["low", "moderate", "high"]:
            ds_dict[scenario][intensity] = xr.open_zarr(
                f"s3://hazard-science-data/productivity_loss_v2/climate_outputs/projections_corrected/{scenario}/CMIP6-ScenarioMIP_{loss_function}_productivity_loss_{intensity}_{scenario}.zarr.zarr/"
            )

    ######## sample the dataset

    # List to accumulate all rows (one per asset_id, year, scenario)
    rows_list = []

    for scenario in scenarios:
        # Create a temporary copy of your asset data and map work_intensity
        df_temp = df_in.copy(deep=True)
        df_temp["work_intensity"] = df_temp["asset_type"].map(
            asset_map.set_index("asset_type")["intensity"]
        )

        # Get the years available for this scenario.
        # Here, we assume the years are the same for every asset in a scenario.
        years = np.concat([[2020], ds_dict[scenario]["high"].year.values])
        stats = ["median", "minimum", "maximum"]

        # Process each asset row
        for _, row in df_temp.iterrows():
            # Get the dataset corresponding to the asset's work intensity in the current scenario
            ds = ds_dict[scenario][row["work_intensity"]]
            ds_2020_local = ds_2020[row["work_intensity"]].sel(
                lat=row["lat"], lon=row["lon"], method="nearest"
            )

            # For each year, extract the values for all stats and build a new row
            for year in years:
                row_dict = (
                    row.to_dict()
                )  # Copy the asset info (like asset_id, lat, lon, etc.)
                row_dict["scenario"] = scenario

                if year == 2020:
                    row_dict["year"] = 2020
                    for stat in stats:
                        value = np.round(ds_2020_local[stat].values, 2)
                        row_dict[stat] = value

                else:
                    row_dict["year"] = year
                    # Get each statistic value from the dataset (using nearest neighbor)
                    for stat in stats:
                        value = np.round(
                            ds.sel(
                                lat=row["lat"],
                                lon=row["lon"],
                                year=year,
                                method="nearest",
                            )[stat].values,
                            2,
                        )
                        row_dict[stat] = value
                    # Append the new row to our list
                rows_list.append(row_dict)
    df_long = pd.DataFrame(rows_list)
    df_long.to_csv(f"output_csvs/{project}_Productivity_Loss_UNSCALED.csv")

    ### AC scaling
    # Make a deep copy of df_long so that the original remains unchanged
    df_long_scaled = df_long.copy(deep=True)

    # Create a new column for AC_penetration and initialize with NaN
    df_long_scaled["AC_penetration"] = np.nan

    # Iterate over each row to compute AC penetration and adjust the values
    for i in df_long_scaled.index:
        lat = df_long_scaled.loc[i, "lat"]
        lon = df_long_scaled.loc[i, "lon"]
        # Compute AC_penetration using the nearest neighbor from the aircon dataset
        ac_val = np.round(aircon.sel(lat=lat, lon=lon, method="nearest").values, 2)
        df_long_scaled.loc[i, "AC_penetration"] = ac_val

        # If a valid AC penetration value is found, scale the statistics accordingly
        if not pd.isna(ac_val):
            # Scale 'median', 'minimum', and 'maximum' by multiplying with (1 - AC_penetration)
            df_long_scaled.loc[i, ["median", "minimum", "maximum"]] *= 1 - ac_val
    df_long_scaled.to_csv(f"output_csvs/{project}_Productivity_Loss_AC_SCALED.csv")

    if save_figures:
        os.makedirs("figures", exist_ok=True)
        barplots(df_long, scenarios, project)
        print("Figures saved in /figures/")

    print(f"HeatProd sampling for Project = {project} is *complete* 8-) ")


if __name__ == "__main__":
    # Parse command-line arguments
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Sample CX Productivity Loss model V2")
    parser.add_argument("--project", type=str, required=True, help="Project name or ID")

    parser.add_argument(
        "--input", type=str, required=True, help="Path to input asset CSV file"
    )
    parser.add_argument(
        "--loss-function",
        type=str,
        default="HOTHAPS",
        help="Loss function (default: HOTHAPS) (options:'HOTHAPS','ISO','NIOSH)",
    )
    parser.add_argument(
        "--makeplots", type=bool, help="Flag to generate and save figures"
    )

    parser.add_argument(
        "--scenarios",
        type=str,
        required=True,
        help="Which scenarios do you want?",
        default=["ssp126", "ssp245", "ssp370", "ssp585"],
    )
    args = parser.parse_args()

    # Convert the comma-separated string into a list
    args.scenarios = [s.strip().lower() for s in args.scenarios.split(",")]
    # Run the model
    main(args.input, args.loss_function, args.makeplots, args.scenarios, args.project)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total runtime: {elapsed_time:.2f} seconds")
