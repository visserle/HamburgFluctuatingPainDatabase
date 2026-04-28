from pathlib import Path

import tomllib


class DataConfig:
    ROOT = Path(__file__).resolve().parents[2]

    DB_FILE = ROOT / "pain-measurement.duckdb"

    MODALITIES = ["Stimulus", "EDA", "EEG", "HR", "Pupil", "Face"]

    STIMULUS_CONFIG_PATH = ROOT / "src/data/stimulus_config.toml"

    @classmethod
    def load_stimulus_config(cls):
        with open(cls.STIMULUS_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)["stimulus"]
