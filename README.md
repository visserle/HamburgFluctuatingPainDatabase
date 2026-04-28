# Hamburg Fluctuating Pain Database

This repository contains the source code for data accessing and data transformation utilities for the Hamburg Fluctuating Pain Database.

The codebase provides an API to the DuckDB database, containing the experimental data and physiological signals (EEG, EDA, Heart Rate, Pupil Diameter, and Facial Expressions).

## Repository Structure

```text
├── notebooks/               # Analysis and visualization notebooks
├── src/
│   ├── data/                # Database management and stimulus generation
│   └── features/            # Signal preprocessing and labeling
└── pain-measurement.duckdb  # DuckDB database (not included in repo)
```

## Installation

### Prerequisites

-   **Python**: ≥ 3.12
-   **Conda**: Recommended for environment management

### Setup

1. Clone the repository and navigate into it:
```bash
git clone https://github.com/visserle/HamburgFluctuatingPainDataset.git
cd pain-measurement
```

#TODO add figshare download

2. Create and activate the conda environment using the provided `requirements.yaml`:
```bash
conda env create -f requirements.yaml
conda activate pain
```

## Usage

The project uses a local DuckDB database for efficient data querying. Most users will
want to open it in read-only mode:

```python
from src.data.database_manager import DatabaseManager

db = DatabaseManager(read_only=True)
with db:
    # Retrieve preprocessed feature data, automatically filtering invalid trials
    df = db.get_trials("Feature_Data", exclude_problematic=True)
    
    # Or execute direct SQL queries
    panas = db.execute("SELECT * FROM Questionnaire_PANAS LIMIT 5").pl()
```

A minimal end-to-end example is available in
[notebooks/quickstart.ipynb](notebooks/quickstart.ipynb).

## Contact

For questions regarding the code or dataset, please open an issue or contact the corresponding author.
