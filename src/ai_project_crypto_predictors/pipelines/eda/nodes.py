import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

def load_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Wczytano dane: {raw_data.shape[0]} wierszy, {raw_data.shape[1]} kolumn")
    return raw_data

def describe_data(df: pd.DataFrame) -> dict:
    logger.info("Analiza podstawowych statystyk i typów danych")
    summary = {
        "info": df.dtypes.to_dict(),
        "describe": df.describe(include="all").to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum()
    }
    logger.info(f"Liczba duplikatów: {summary['duplicates']}")
    return summary

def visualize_data(df: pd.DataFrame) -> None:
    logger.info("Generowanie wykresów EDA")
    plt.figure(figsize=(10,6))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
    plt.title("Korelacja między zmiennymi numerycznymi")
    plt.tight_layout()
    plt.savefig("docs/heatmap_correlation.png")

    for col in df.select_dtypes(include='number').columns:
        sns.histplot(df[col], kde=True)
        plt.title(f"Rozkład {col}")
        plt.savefig(f"docs/hist_{col}.png")
        plt.close()

    logger.info("Wizualizacje zapisane w katalogu docs/")
