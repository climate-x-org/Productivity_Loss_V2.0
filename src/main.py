# python src/main.py --input "$INPUT_FILE" --output "$OUTPUT_FILE" --loss-function "$LOSS_FUNCTION" --makeplots "$MAKE_PLOTS"

#### imports
import xarray as xr
import numpy as np
import argparse
import pandas as pd
import os
# from src.visualisation import generate_figures


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


def main(input_file, loss_function, save_figures, scenarios):
    ####### deal with files
    asset_map = pd.read_csv("../src/asset_map.csv")  # load asset mapping
    df_in = load_input_data(input_file)  # Load input CSV

    ## load aircon
    aircon = xr.open_zarr(
        "s3://hazard-science-data/productivity_loss_v2/aircon/AirCon_SSPs.zarr/"
    )
    aircon = aircon.sel(SSP="2.0").isel(year=0)["ac_penetration"]

    ## load loss zarrs
    ds_dict = {}
    for scenario in ["ssp126", "ssp245", "ssp370", "ssp585"]:
        ds_dict[scenario] = {}
        for intensity in ["low", "moderate", "high"]:
            ds_dict[scenario][intensity] = xr.open_zarr(
                f"s3://hazard-science-data/productivity_loss_v2/climate_outputs/projections_corrected/{scenario}/CMIP6-ScenarioMIP_{loss_function}_productivity_loss_{intensity}_{scenario}.zarr.zarr/"
            )

    ######## sample the dataset
    df_out = {}
    for scenario in scenarios:
        df_out[scenario] = df_in.copy(deep=True).set_index("asset_id")
        df_out[scenario]["work_intensity"] = df_out[scenario]["asset_type"].map(
            asset_map.set_index("asset_type").to_dict()["intensity"]
        )
        df_out[scenario] = df_out[scenario].reset_index()

    def extract_values(row):
        """Fetches nearest productivity loss values for given lat, lon, and work intensity."""
        ds = ds_dict["ssp126"][row["work_intensity"]]
        result = {
            f"{year}_{stat}": np.round(
                ds.sel(lat=row["lat"], lon=row["lon"], year=year, method="nearest")[
                    stat
                ].values,
                4,
            )
            for stat in newcols
            for year in years
        }
        return pd.Series(result)

    for scenario in scenarios:
        years = ds_dict[scenario]["high"].year.values
        newcols = ["median", "minimum", "maximum"]
        # Create new columns in one operation
        col_names = [f"{year}_{stat}" for year in years for stat in newcols]
        df_out[scenario] = df_out[scenario].assign(**{col: np.nan for col in col_names})
        # apply function across all rows
        df_out[scenario][col_names] = df_out[scenario].apply(extract_values, axis=1)

        ## intermediate checkout - save unscaled results
        df_out[scenario].set_index("asset_id").drop(
            columns=["lat", "lon"]
        ).transpose().to_csv(f"output_csvs/unscaled_{scenario}.csv")

    ### AC scaling
    df_scaled = {}
    for scenario in scenarios:
        df_scaled[scenario] = df_out[scenario].copy(deep=True)
        df_scaled[scenario]["AC_penetration"] = np.full_like(
            df_scaled[scenario]["lat"], np.nan
        )
        for i in df_scaled[scenario].index:
            df_scaled[scenario].loc[i, "AC_penetration"] = np.round(
                aircon.sel(
                    lat=df_scaled[scenario].loc[i, "lat"],
                    lon=df_scaled[scenario].loc[i, "lat"],
                    method="nearest",
                ).values,
                3,
            )
            if not pd.isna(df_scaled[scenario].loc[i, "AC_penetration"]):
                df_scaled[scenario].iloc[i, 5:-1] *= (
                    1 - df_scaled[scenario].iloc[i, -1]
                )  # if ac penetration not null, multiple loss by 1 - AC%

        df_out[scenario].set_index("asset_id").drop(
            columns=["lat", "lon"]
        ).transpose().to_csv(f"output_csvs/scaled_{scenario}.csv")

    if save_figures:
        os.makedirs("figures", exist_ok=True)
        # generate_figures(results, output_dir="figures")
        print("Figures saved in /figures/")

    print("HeatProd sampling = complete 8-) ")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Sample CX Productivity Loss model V2")
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
        "--makeplots", action="store_true", help="Flag to generate and save figures"
    )

    parser.add_argument(
        "--scenarios",
        type=list,
        required=True,
        help="Which scenarios do you want? Each will be returned as a separate csv",
        default=["ssp126", "ssp245", "ssp370", "ssp585"],
    )
    args = parser.parse_args()

    # Run the model
    main(args.input, args.loss_function, args.makeplots, args.scenarios)
