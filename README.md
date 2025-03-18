# Climate × Heat Productivity Loss Model (v2) – Sample Repo

## 📌 Overview

This repository provides a sample implementation of the Climate × Heat Productivity Loss Model (v2), designed for Product and Sales Engineers. Users can run the model to estimate productivity loss (%) due to heat exposure based on climate conditions and asset-specific characteristics.

## 🚀 How It Works
	1.	Upload a CSV file containing asset locations and building types/uses.
	2.	The model applies the default HOTHAPS loss curve to compute productivity loss (%).
	3.	Retrieve results showing productivity impacts across different assets.

### ⚙️ Environment Setup

Before you run the script, you MUST to set up a custom Conda environment. You first need to make sure you have access to the relevant S3 buckets and setup aws configuration on your machine. To do so, run the following in you terminal:
```
aws configure
```

Once configured, setup the environment by running the following code in the terminal:

```
conda env create -f environment.yaml
conda activate productivity_loss_v2
```

### 📁 Input Requirements
	•	CSV File Format with asset locations and building types.
	•	Ensure latitude and longitude columns are included.

### 📤 Output
	•	Productivity loss (%) estimates for each asset, calculated using the HOTHAPS default loss curve.

### 🔗 Next Steps
	•	Upload sample data and test the model.
	•	Modify parameters if needed for custom productivity loss curves.
	•	Extend functionality for additional climate scenarios.

For questions, please reach out to the Science team (Aidan / Sally) 🚀


# Appendix
## Assignment of asset work intensities
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