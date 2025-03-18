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
    return df.drop_duplicates("asset_id")


def save_output_data(df, file_path):
    """Save productivity loss results to a CSV file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f";-) Results saved to: {file_path}")


def main(input_file, output_file, loss_function, save_figures):
    # load asset mapping
    asset_map = pd.read_csv("../src/asset_map.csv")

    # Load input CSV
    df_in = load_input_data(input_file)

    ## load aircon
    aircon = xr.open_zarr(
        "s3://hazard-science-data/productivity_loss_v2/aircon/AirCon_SSPs.zarr/"
    )
    aircon = aircon.sel(SSP="2.0").isel(year=0)["ac_penetration"]

    ## load losses
    ds_dict = {}
    for scenario in ["ssp126", "ssp245", "ssp370", "ssp585"]:
        ds_dict[scenario] = {}
        for intensity in ["low", "moderate", "high"]:
            ds_dict[scenario][intensity] = xr.open_zarr(
                f"s3://hazard-science-data/productivity_loss_v2/climate_outputs/projections_corrected/{scenario}/CMIP6-ScenarioMIP_{loss_function}_productivity_loss_{intensity}_{scenario}.zarr.zarr/"
            )

    ## sample
    df_out = df_in.copy(deep=True).set_index('asset_id')
    df_out['work_intensity'] = df_out['asset_type'].map(asset_map.set_index('asset_type').to_dict()['intensity'])

    df_out_ssp126 = df_out.copy(deep=True)
    df_out_ssp245 = df_out.copy(deep=True)
    df_out_ssp370 = df_out.copy(deep=True)
    df_out_ssp585 = df_out.copy(deep=True)

    for asset in df_out.index:
        intensity = df_out.loc[asset,'work_intensity']
        ds_ = ds_dict['ssp585'][intensity].sel(lat=df_out.loc[asset,'latitude'],lon=df_out.loc[asset,'longitude'],method='nearest')




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
        "--output", type=str, required=True, help="Path to save the output CSV file"
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
    args = parser.parse_args()

    # Run the model
    main(args.input, args.output, args.loss_function, args.makeplots)
