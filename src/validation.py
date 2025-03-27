import pandas as pd
import chardet

# Define your expected schema (you can adjust these as needed)
EXPECTED_COLUMNS = {
    "Asset ID",
    "Parent Name",
    "Premise Type",
    "Latitude",
    "Longitude",
}


def detect_encoding(file_path):
    """Detect the encoding of the CSV file."""
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(10000))
    return result["encoding"]


def validate_columns(df):
    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")
    return True


def validate_csv(file_path):
    """Validate a CSV file for correct encoding, columns, and missing values."""
    encoding = detect_encoding(file_path)
    try:
        df = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError:
        raise ValueError(
            "File encoding not supported. Please check your file's encoding."
        )

    # Check for expected columns
    validate_columns(df)

    missing_info = {}
    for col in EXPECTED_COLUMNS:
        if df[col].isna().any():
            missing_ids = df.loc[df[col].isna(), "Asset ID"].tolist()
            missing_info[col] = missing_ids

    if missing_info:
        raise ValueError(
            f"Missing values found in columns with corresponding Asset IDs: {missing_info}"
        )

    return df
