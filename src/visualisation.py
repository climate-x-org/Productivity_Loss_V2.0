import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


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
            color="xkcd:navy",
        )
        a.bar(
            x + bar_width / 2,
            data_pivot["2100_median"],
            yerr=err_2100,
            width=bar_width,
            capsize=5,
            label="2100",
            color="xkcd:ruby",
        )

        a.set_xticks(x)
        a.set_xticklabels(data_pivot["asset_id"], rotation=45, fontsize=6, ha="right")
        a.set_ylim(0, data_pivot["2100_maximum"] + 1)
        # a.set_yscale('log')
        a.set_ylabel("Productivity Loss (%)")
        a.legend()
        a.set_title(scenario)

    plt.savefig(f"figures/{project}_barplots.png", dpi=300, bbox_inches="tight")
