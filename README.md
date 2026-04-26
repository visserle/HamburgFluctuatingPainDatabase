# Hamburg Pain Database

This repository contains the source code for data accessing and data transformation utilities for the Hamburg Pain Database.

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
git clone https://github.com/visserle/pain-measurement.git
cd pain-measurement
```

2. Create and activate the conda environment using the provided `requirements.yaml`:
```bash
conda env create -f requirements.yaml
conda activate pain
```

## Usage

The project uses a local DuckDB database for efficient data querying. You can interact with it using the provided `DatabaseManager`:

```python
from src.data.database_manager import DatabaseManager

db = DatabaseManager()
with db:
    # Retrieve preprocessed feature data, automatically filtering invalid trials
    df = db.get_trials("Feature_Data", exclude_problematic=True)
    
    # Or execute direct SQL queries
    participant_info = db.execute("SELECT * FROM Participants_Info").pl()
```

## Contact

For questions regarding the code or dataset, please open an issue or contact the corresponding author.
