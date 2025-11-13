import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Rozpoczynam czyszczenie danych...")


    threshold = 0.4
    df = df.loc[:, df.isnull().mean() < threshold]


    for col in df.columns:
        if df[col].dtype in [np.float64, np.int64]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "unknown")


    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            continue


    df = df.drop_duplicates()


    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]

    logger.info(f"Po czyszczeniu: {df.shape[0]} wierszy, {df.shape[1]} kolumn.")
    return df

def scale_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Standaryzacja danych (StandardScaler)...")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    logger.info("Dane zostały zeskalowane.")
    return df_scaled

def split_data(df: pd.DataFrame):
    logger.info("Podział danych na zbiory: train / val / test")

    train, temp = train_test_split(df, test_size=0.3, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)

    logger.info(f"Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")
    return train, val, test
