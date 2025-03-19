# Climate × Heat Productivity Loss Model (v2) – Sample Repo

## 📌 Overview

This repository provides an interface to sample the Climate × Heat Productivity Loss Model (v2), designed for Product and Sales Engineers. Users can run the model to estimate productivity loss (%) due to heat exposure based on climate conditions and asset-specific characteristics.

## 🚀 How It Works
	1.	Upload a CSV file containing asset locations and building types/uses to the `/data` folder.
	2.	Run the command-line script `./run.sh` with parameters of your chosing (see below).
	3.	Retrieve results showing productivity impacts across different assets (csvs and figures, if you so desire).

### ⚙️ Environment Setup
Before you run the script, you MUST to set up a custom Conda environment. You first need to make sure you have access to the relevant S3 buckets and setup aws configuration on your machine. If you don't have access to the `hazard-science-data` S3 bnucket, contact Monisha!! Once you've got access, run the following in you terminal and follow the prompts:
```
aws configure
```

Once configured, setup the environment by running the following code in the terminal:

```
conda env create -f environment.yaml
conda activate productivity_loss_v2
```

### Running the script
This repository contains a shell script that serves as the entry point for ssampling the Productivity Loss Model. The script allows you to customize the execution by specifying an input file, loss function, whether to generate plots, a list of scenarios, and a project name.

**MINIMUM WORKING EXAMPLE**:
To run the script with the default parameters:
```
./run.sh
```

To run the script with custom parameters:
```
./run.sh --input data/my_assets.csv --loss-function HOTHAPS --make-plots True --scenarios SSP126,SSP585 --project my_project_name
```

Default Parameter Values
- Input File: data/test_assets.csv
- Loss Function: HOTHAPS
- Generate Plots: False
- Scenarios: SSP126,SSP245,SSP370,SSP585
- Project Name: test

Command-Line Arguments
- `--input`: Path to the input CSV file containing asset data.
- `--loss-function`: The loss function to use (e.g., HOTHAPS).
- `--make-plots`: Set to True or False to generate plots. The plots randomly select a subsample of the assets run for visualisation.
- `--scenarios`: A comma-separated list of scenarios (e.g., SSP126,SSP245,SSP370,SSP585).
- `--project`: Project name identifier (used in outputs).


File Structure:
- Input Data: The default input CSV file (data/test_assets.csv) should exist, or you can supply an alternative via the --input parameter.
- Main Script: The model’s Python code is all in src/main.py.
- Output Files: Output CSV files will be generated in the /output_csvs/ directory.
- Figures: Optional "sense check" figures can be generated and will be saved as pngs in /figures/

### 📁 Input Requirements
The following columns must be included in the input csv:
- "asset_id"
- "latitude"
- "longitude"
- "asset_type"

### 📤 Output
The main output is Productivity loss (%) estimates for each asset, calculated using the selected loss function (HOTHAPS by default). Optional output of figures.

The output csvs are:
- `output_csvs/{project}_Productivity_Loss_UNSCALED` (where {project} is the project name you give) -- this is the table of productivity losses (in annual %) without any air conditioning scaling. The column 'work_intensity' tells you which loss curve intensity level has been used.
- `output_csvs/{project}_Productivity_Loss_AC_SCALED` -- this is the same as unscaled, but each value has been multiplied by 1-AC ownership% for each asset's region. The AC ownership % is taken from Falchetta et al., 2024 and reflects residential ownership of AC in 2020. The AC % is given as the column `AC_penetration` 


For questions, please reach out to the Science team (Aidan / Sally) 🚀


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