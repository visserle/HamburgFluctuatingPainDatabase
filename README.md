# Hamburg Fluctuating Pain Database

This repository provides an API to the DuckDB database of the Hamburg Fluctuating Pain Dataset. The database encompasses behavioural and physiological recordings (EEG, EDA, heart rate, pupil diameter, facial expressions, pain ratings) during tonic fluctuating heat pain in healthy adults (n = 45). 

> [!NOTE]
> The database file is not included in the repository due to its size (∼ 8 GB; 27 hours of time series data). Please use the `download_database.py` script or download it manually from the companion [Figshare](https://doi.org/10.6084/m9.figshare.32112442) record and place it in the repository root.

## Repository Structure

```text
├── notebooks/               # Analysis and visualization notebooks
├── src/
│   ├── data/                # Database management and stimulus generation
│   └── features/            # Signal preprocessing and labeling
└── pain-measurement.duckdb  # DuckDB database (not included in repo)
```

## Installation

Requires Python ≥ 3.12 and Conda for environment management.

1. Clone the repository and navigate into it:
```bash
git clone https://github.com/visserle/HamburgFluctuatingPainDataset.git
cd HamburgFluctuatingPainDataset
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

## Usage

The project uses a local DuckDB database for efficient data querying. Most users will want to open it in read-only mode:

```python
from src.data.database_manager import DatabaseManager

db = DatabaseManager()
with db:
    # Retrieve preprocessed feature data, automatically filtering invalid trials
    df = db.get_trials("Feature_Data", exclude_problematic=True)
    
    # Or execute direct SQL queries
    panas = db.execute("SELECT * FROM Questionnaire_PANAS LIMIT 5").pl()
```

A minimal end-to-end example is available in [notebooks/quickstart.ipynb](notebooks/quickstart.ipynb).

## Contact

For questions regarding the code or dataset, please open an issue or contact the corresponding author.
