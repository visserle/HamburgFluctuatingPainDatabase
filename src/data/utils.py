"""Utility functions for data processing and configuration."""

import tomllib

def load_configuration(file_path: str) -> dict:
    """Load configuration from a TOML file."""
    with open(file_path, "rb") as file:
        return tomllib.load(file)
