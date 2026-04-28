"""
Create dataframes that will be inserted as tables into the database (see main function
of database_manager.py).
"""

import logging

import polars as pl
from polars import col

from src.data.data_config import DataConfig
from src.data.stimulus_generator import StimulusGenerator
from src.features.eda import feature_eda
from src.features.eeg import feature_eeg
from src.features.explore_eda import explore_eda
from src.features.explore_eeg import explore_eeg
from src.features.explore_face import explore_face
from src.features.explore_hr import explore_hr
from src.features.explore_pupil import explore_pupil
from src.features.explore_stimulus import explore_stimulus
from src.features.face import feature_face
from src.features.hr import feature_hr
from src.features.labels import add_labels
from src.features.pupil import feature_pupil
from src.features.resampling import (
    add_normalized_timestamp,
    interpolate_and_fill_nulls_in_trials,
    resample_at_10_hz_equidistant,
)
from src.features.stimulus import feature_stimulus
from src.features.transforming import merge_dfs

logger = logging.getLogger(__name__.rsplit(".", maxsplit=1)[-1])


def create_seeds_df():
    config = DataConfig.load_stimulus_config()
    seeds = config["seeds"]

    # Generate labels for all seeds
    all_labels = [StimulusGenerator(config=config, seed=seed).labels for seed in seeds]

    # Get label keys from first stimulus generator
    label_keys = all_labels[0].keys()

    # Build data dictionary dynamically
    data = {"seed": seeds}
    data.update({key: [labels[key] for labels in all_labels] for key in label_keys})

    # Build schema dynamically
    schema = {
        "seed": pl.UInt16,
        **{key: pl.List(pl.List(pl.UInt32)) for key in label_keys},
    }

    return pl.DataFrame(data, schema=schema)


def remove_trials_with_thermode_or_rating_issues(
    invalid_trials_df: pl.DataFrame,
    df: pl.DataFrame,
):
    # remove trials with thermode or rating issues
    trials_with_thermode_or_rating_issues = invalid_trials_df.with_columns(
        col("participant_id").cast(pl.UInt8),
        col("trial_number").cast(pl.UInt8),
        (
            (col("modality").str.count_matches("thermode"))
            + (col("modality").str.count_matches("rating"))
        )
        .alias("issue_thermode_or_rating")
        .cast(pl.Boolean),
    ).filter(col("issue_thermode_or_rating"))
    return df.filter(
        ~pl.struct(["participant_id", "trial_number"]).is_in(
            trials_with_thermode_or_rating_issues.select(
                ["participant_id", "trial_number"]
            )
            .unique()
            .to_struct()
        )
    )


def create_feature_data_df(
    name: str,
    df: pl.DataFrame,
) -> pl.DataFrame:
    name = name.lower()
    df = df.drop(["rownumber", "samplenumber"], strict=False)
    if "stimulus" in name:
        return feature_stimulus(df)
    elif "eda" in name:
        return feature_eda(df)
    elif "eeg" in name:
        return feature_eeg(df)
    elif "hr" in name:
        return feature_hr(df)
    elif "pupil" in name:
        return feature_pupil(df)
    elif "face" in name:
        return feature_face(df)
    else:
        raise ValueError(f"Unknown feature type: {name}")


def create_explore_data_df(
    name: str,
    df: pl.DataFrame,
) -> pl.DataFrame:
    """Create exploratory data for a given feature type."""
    name = name.lower()
    if "stimulus" in name:
        return explore_stimulus(df)
    elif "eda" in name:
        return explore_eda(df)
    elif "eeg" in name:
        return explore_eeg(df)
    elif "hr" in name:
        return explore_hr(df)
    elif "pupil" in name:
        return explore_pupil(df)
    elif "face" in name:
        return explore_face(df)
    else:
        raise ValueError(f"Unknown feature type: {name}")


def merge_and_label_data_dfs(
    data_dfs: list[pl.DataFrame],
    trials_info_df: pl.DataFrame,
) -> pl.DataFrame:
    """
    Merge multiple feature DataFrames into a single DataFrame. Only for data at 10 Hz.
    """
    df = merge_dfs(data_dfs)
    df = interpolate_and_fill_nulls_in_trials(df)
    df = add_normalized_timestamp(df)
    df = resample_at_10_hz_equidistant(df)
    df = add_labels(df, trials_info_df)  #  important: always add labels at the very end
    return df.drop("rownumber", "samplenumber", strict=False)
