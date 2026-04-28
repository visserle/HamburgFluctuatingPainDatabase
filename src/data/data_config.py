from pathlib import Path

import tomllib


class DataConfig:
    ROOT = Path(__file__).resolve().parents[2]

    DB_FILE = ROOT / "pain-measurement.duckdb"
    DOWNLOAD_SCRIPT = ROOT / "download_database.py"

    MODALITIES = ["Stimulus", "EDA", "EEG", "HR", "Pupil", "Face"]

    STIMULUS_CONFIG_PATH = ROOT / "src/data/stimulus_config.toml"

    @classmethod
    def require_database_file(cls) -> None:
        if cls.DB_FILE.is_file():
            return

        raise FileNotFoundError(
            "Expected the DuckDB database at "
            f"{cls.DB_FILE}, but it was not found. "
            "Download it into the repository root with "
            f"`python3 {cls.DOWNLOAD_SCRIPT.name}`."
        )

    @classmethod
    def load_stimulus_config(cls):
        with open(cls.STIMULUS_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)["stimulus"]
