import pandas as pd


def load_data(file_path):

    file_path = str(file_path)

    if file_path.lower().endswith(".csv"):

        return pd.read_csv(file_path)

    if file_path.lower().endswith(".xlsx"):

        return pd.read_excel(file_path)

    raise ValueError(
        "Only CSV and XLSX files are supported."
    )


def get_data_summary(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": int(
            df.isnull().sum().sum()
        )
    }
    