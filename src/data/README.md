# Data Pipeline

The database consists of two seperate pipelines (`Raw` → `Feature` and `Raw` → `Explore`) over all modalities (EEG, EDA, PPG, pupillometry, facial expressions, and rating / temperatures). In a final step, the data is merged into a single table for each pipeline and labeled according to the stimulus function. `Explore` tables are created with non-causal transformations of the data for exploratory analysis, while `Feature` tables are created with causal transformations for the classification task.

- `Raw`: Raw data from iMotions .csv output (anonymized).
- `Feature`: Extracted features from the preprocessed data.
- `Explore`: Tables for exploratory analysis with non-causal transformations of the data.
- `Feature_Data`: Merged feature data with stimulus labels, resampled to 10 Hz at equidistant time points. EEG data is handled seperately due its different sampling rate.
- `Explore_Data`: Merged feature data with stimulus labels, resampled to 10 Hz at equidistant time points, but with non-causal transformations for exploratory analysis.

Furthermore, there are additional tables for the experiment metadata, calibration results, and questionnaire responses.

## Files

- `database_schema.py` defines the SQL schema for the database.
- `database_manager.py` is for insertig data into the database and extracting data from the database.
- `data_processing.py` coordinates the data processing by creating dataframes that are ready for insertion into the database as tables. For time series data tables (Stimulus, EEG, EDA, PPG, pupillometry, facial expressions) it uses the functions from the feature module (feature modules are decoupled from the database and can be used independently on dataframes).
- `data_config.py` contains very basic configuration parameters for the data pipeline.
