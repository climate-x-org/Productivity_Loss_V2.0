# Climate X Heat Productivity Loss Model v2.0

This repository provides a sample interface for estimating annual productivity loss (%) due to heat exposure based on climate conditions and asset-specific data.

---

## 🏎️ Quickstart

1. **Clone the Repo:**

   ```bash
   git clone https://github.com/climate-x-org/Productivity_Loss_V2.0.git
    ```

2. **AWS Setup:**
    Configure AWS (contact Monisha for credentials if needed):
    
    ```bash
    aws configure
    ```

3.	**Conda Environment:**
    Create and activate the environment:
    ```bash
    conda env create -f environment.yml
    conda activate productivity_loss_v2
    ``` 

4.	**Prepare Your Input:**
	Place your CSV in the /data/ folder.
	Required columns (additional columns are allowed):
	- `Asset ID`
	- `Parent Name`
	- `Premise Type`
	- `Latitude`
	- `Longitude`
	- `Asset Criticality`

    See data/hsbc_poc_mar25_all_assets_dropped_bad_lats.csv

5. **Run the script:**
    Execute the CLI:
    ```bash
    ./run.sh --input data/{YOUR_FILE.csv} --scenarios SSP126,SSP585 --project {YOUR_PROJECT_NAME}
    ```
> [!NOTE]  
> You may need to run `chmod +x run.sh` before the shell script can run

6. **Review Outputs:**

    Check the /output_csvs/ folder for two files:
	- Unscaled: Base productivity loss estimates.
	- AC Scaled: Loss estimates adjusted for air conditioning availability.


# 📌 Overview
- Purpose: Estimate productivity loss (%) due to heat exposure using pre-calculated global rasters.
- Loss Functions: Default is HOTHAPS (alternatives include ISO and NIOSH).
- Work Intensities: The loss curve applied depends on asset work type (low, moderate, or high intensity).

# 🚀 How It Works
1. Input: CSV with asset data (must include required columns).
2. Processing:
3. Applies loss functions based on climate scenarios (e.g., SSP126, SSP245, SSP370, SSP585) and work intensity.
4. Optionally generates plots for a subsample of assets.
5. Output:
    - Two CSV files with productivity loss estimates (unscaled and AC-scaled).


# ⚙️ Environment & Running the Script
- AWS: Ensure AWS permissions are configured.
- Conda: Build the environment with:
    ```bash
    conda env create -f environment.yml
    conda activate productivity_loss_v2 
    ```
Note: If any packages (e.g., xarray) are missing after activation, you might need to install them manually (this is a bug I'm aware of but don't understand)

## CLI Arguments:
- `--input`: Path to the input CSV (default: data/test_assets.csv).
- `--loss-function`: Loss function to use (default: HOTHAPS).
- `--make-plots`: Generate plots? (True/False; default: False).
- `--scenario`s`: Comma-separated list of scenarios (default: SSP126,SSP245,SSP370,SSP585).
- `--project`: Project name identifier (default: test).

**Example:**
    ```
    ./run.sh --input data/my_assets.csv --loss-function HOTHAPS --make-plots True --scenarios SSP126,SSP585 --project my_project
    ```

# 📁 File structure 
```shell
├── README.md
├── data/                  # Input CSV files
├── dev/                   # Development notebooks
├── environment.yml        # Conda environment file
├── figures/               # Generated plots
├── output_csvs/           # Output CSVs with productivity loss estimates
├── run.sh                 # Entry point script
└── src/                   # Python source code
    ├── asset_map.csv      # Asset type to work intensity mapping
    ├── main.py            # Main processing script
    ├── visualisation.py   # Plotting utilities
    └── validation.py      # CSV validation functions
----
```

# 📤 Output
The model produces two primary CSV outputs:
- `{project}_Productivity_Loss_UNSCALED.csv`: Productivity loss (%) without AC adjustments.
- `{project}_Productivity_Loss_AC_SCALED.csv`: Loss estimates scaled by regional air conditioning penetration.

# 🤝 Support

For any questions or issues, please contact the Science team (Aidan / Sally).

# Appendix
## Assignment of asset work intensities
**There is a file called `asset_map.csv` which contains the mapping between Spectra/Carta building use types and work intensity levels (low, moderate, or high). Feel free to change these in the file and they will automatically be updated in the script.**

### Justification/method to the current assignment:
Various industry standards and research studies classify work intensity levels by typical metabolic power output (Watts). Across occupational health guidelines and energy/climate reports, there is consistent grouping into three broad categories: roughly 200 W for light office work, 300 W for moderately active work, and 400 W for heavy industrial work. Below is a summary of each category and the relevant citation/source:

### Low Intensity (~200 W) – Office/Clerical Work
Light workloads (around 200 watts) correspond to sedentary or minimal physical activity, such as office tasks, desk jobs, and clerical work. Authoritative sources consistently define ~200 W as the metabolic power for “clerical or light physical work”. For example, an International Labour Organization (ILO) analysis of heat stress explicitly uses 200 W to represent services/office work. Similarly, a World Bank climate impacts report notes that “200 W represents clerical or light physical work”, aligning with the low-intensity category. In occupational health standards, this level falls under “light work” – e.g. ISO and NIOSH guidelines consider any task under ~234 W as light intensity, which covers typical office and administrative duties.

### Moderate Intensity (~300 W) – General Commercial & Transport Work
Moderate workloads (on the order of 300 watts) involve continual but not extreme physical effort. This covers many general commercial, light industrial, or transport jobs – for instance, assembly line work, driving or operating equipment, and routine maintenance. Research and standards place ~300 W in the “moderate work” category. The ILO and related studies use 300 W as a representative metabolic rate for “moderate physical work in industry” – essentially general commercial/manufacturing activities. An ILO report on climate and labor similarly assigns 300 W to the industry/transport sector in its models. This consensus is echoed in government and academic sources: for example, OSHA’s technical background for heat safety cites research defining moderate work at approximately 300 W. Overall, ~300 W is validated as the mid-level intensity typical of active work in commerce and infrastructure.

### High Intensity (~400 W) – Heavy Industry, Manufacturing & Energy Production
High-intensity workloads (around 400 watts or more) correspond to strenuous, heavy labor found in sectors like heavy industry, construction, heavy manufacturing, agriculture, or energy production. Authoritative sources consistently classify ~400 W as “heavy physical work”. For instance, the ILO’s analysis equates 400 W with “heavy physical work in agriculture or construction” – both being labor-intensive sectors. This ~400 W benchmark is widely applied to any heavy-industrial or manual work category. A World Bank technical report (drawing on ISO 7243 standards) confirms that “400 W [represents] heavy physical work” in high-intensity sectors. Likewise, an EU study on occupational heat exposure divided work into light (200 W), moderate (300 W), and heavy (400 W) bands for analysis, underscoring 400 W as the heavy-work norm. Even safety regulators note similar values – OSHA references ~415 W as a typical “heavy” workload in its heat stress guidelines. In summary, ~400 W is validated by standards and studies as the expected power output for heavy work, characteristic of physically demanding industrial and energy-related jobs.

### Supporting Standards and Studies
Sources: 
- The International Labour Office and ISO climate/labor studies
- OSHA/NIOSH heat stress guidelines
- Academic research on occupational heat exposure corroborate these work-intensity definitions. Each source consistently assigns office or clerical work at ~200 W (light), general industrial or transport work at ~300 W (moderate), and heavy industry or similar labor around ~400 W (heavy).
Full bibliography available on the Climate X Zotero library. 
