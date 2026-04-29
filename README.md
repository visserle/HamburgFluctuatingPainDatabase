# Hamburg Fluctuating Pain Database

This repository provides an API to the Hamburg Fluctuating Pain Database. The DuckDB database encompasses behavioural and physiological recordings (EEG, EDA, heart rate, pupil diameter, facial expressions, pain ratings) during tonic fluctuating heat pain in healthy adults (n = 45).

> [!NOTE]
> #TODO: Add reference to the associated publication once available.

> [!TIP]
> The database file is not included in the repository due to its size (∼ 8 GB; 27 hours of time series data). Please use the `download_database.py` script or download it manually from the companion [Figshare](https://doi.org/10.6084/m9.figshare.32112442) record and place it in the repository root.

## Setup

Requires Python ≥ 3.12 and Conda for environment management.

1. Clone the repository and navigate into it:
```bash
git clone https://github.com/visserle/HamburgFluctuatingPainDatabase.git
cd HamburgFluctuatingPainDatabase
```

2. Download the DuckDB database:
```bash
python3 download_database.py
```

3. Create and activate the conda environment using the provided `requirements.yaml`:
```bash
conda env create -f requirements.yaml
conda activate pain
```

## Database Structure

The DuckDB file contains 29 tables split into metadata and time-series data. Metadata tables describe trial boundaries and exclusions (`Trials_Info`, `Invalid_Trials`), stimulus definitions (`Seeds`), participant calibration (`Calibration_Results`), and questionnaire responses (`Questionnaire_*`).

Time-series tables follow a consistent naming scheme across the six recorded modalities (`Stimulus`, `EDA`, `EEG`, `HR`, `Pupil`, `Face`):

- `Raw_*`: unprocessed recordings at their original sampling rates.
- `Feature_*`: causally preprocessed signals intended for online or real-time analyses.
- `Explore_*`: non-causally preprocessed signals for exploratory analyses; EEG is not available in this form.
- `Feature_Data` and `Explore_Data`: merged multimodal tables at 10 Hz containing all modalities except EEG.

Time-series tables share the identifiers `participant_id`, `trial_number`, `trial_id`, and `timestamp`. The merged tables additionally include `normalized_timestamp`, which resets to zero at each trial onset.

## Example Usage

The project uses a local DuckDB database for efficient data querying. A minimal end-to-end example is available in [notebooks/quickstart.ipynb](notebooks/quickstart.ipynb).

```python
from src.data.database_manager import DatabaseManager

db = DatabaseManager()
with db:
    # Retrieve preprocessed feature data, automatically filtering invalid trials
    df = db.get_trials("Feature_Data", exclude_problematic=True)
    
    # Or execute direct SQL queries
    panas = db.execute("SELECT * FROM Questionnaire_PANAS LIMIT 5").pl()
```
For further information, please refer to the original paper, the READMEs in the submodules and the documentation in the codebase.

## Repository Structure

```text
├── notebooks/               # Analysis and visualization notebooks
├── src/
│   ├── data/                # Database management and stimulus generation
│   └── features/            # Signal preprocessing and labeling
└── pain-measurement.duckdb  # DuckDB database (not included in repo)
```

## Contact

For questions regarding the code or database, please open an issue or contact the corresponding author.
