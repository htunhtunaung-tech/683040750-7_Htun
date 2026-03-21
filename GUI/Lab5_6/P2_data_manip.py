"""
Htun Htun Aung
683040750-7
Lab5_6 P2"
"""

import json
import numpy as np
import pandas as pd
import pyqtgraph as pg

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    TODO 1 — Read a CSV file and return a clean DataFrame.
    - Read the CSV into a DataFrame
    - Raise if empty
    - Raise if required columns are missing
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The CSV file is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    return df


def read_json(path: str) -> pd.DataFrame:
    """
    TODO 2 — Read a JSON file and return a DataFrame.
    - Read the JSON into a DataFrame
    - Raise if empty
    - Raise if required columns are missing
    """
    df = pd.read_json(path)

    if df.empty:
        raise ValueError("The JSON file is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"JSON is missing required columns: {missing}")

    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    TODO 3 — Save a DataFrame to a CSV file.
    - Raise if the DataFrame is empty
    - Raise on any write error
    """
    if df.empty:
        raise ValueError("Cannot save — the data is empty.")

    try:
        df.to_csv(path, index=False)
    except Exception as e:
        raise IOError(f"Failed to write CSV: {e}")


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    TODO 4 — Save a DataFrame to a JSON file.
    - Raise if the DataFrame is empty
    - Raise on any write error
    """
    if df.empty:
        raise ValueError("Cannot save — the data is empty.")

    try:
        df.to_json(path, orient="records", indent=2)
    except Exception as e:
        raise IOError(f"Failed to write JSON: {e}")


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    TODO 5 — Compute per-city statistics and return a QTableWidget.
    Rows: avg_temp, max_temp, min_temp, total_rain, avg_humidity
    Columns: city names
    """
    if df.empty:
        raise ValueError("Cannot build statistics — the DataFrame is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")

    # Stat rows to compute
    stat_labels = ["records", "avg_temp", "max_temp", "min_temp", "total_rain", "avg_humidity"]
    cities = sorted(df["city"].unique())

    table = QTableWidget(len(stat_labels), len(cities))
    table.setVerticalHeaderLabels(stat_labels)
    table.setHorizontalHeaderLabels(cities)
    table.horizontalHeader().setStretchLastSection(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)

    for col_idx, city in enumerate(cities):
        city_df = df[df["city"] == city]
        stats = [
            str(len(city_df)),
            f"{city_df['temp_c'].mean():.1f}",
            f"{city_df['temp_c'].max():.1f}",
            f"{city_df['temp_c'].min():.1f}",
            f"{city_df['rainfall_mm'].sum():.1f}",
            f"{city_df['humidity'].mean():.1f}",
        ]
        for row_idx, value in enumerate(stats):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_idx, col_idx, item)

    table.resizeColumnsToContents()
    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    TODO 6 — Draw a Rainfall Histogram using pyqtgraph and return a PlotWidget.
    """
    if df.empty:
        raise ValueError("Cannot draw chart — the DataFrame is empty.")

    if "rainfall_mm" not in df.columns:
        raise ValueError("DataFrame is missing the 'rainfall_mm' column.")

    rainfall = df["rainfall_mm"].dropna().values

    # Compute histogram bins
    counts, bin_edges = np.histogram(rainfall, bins=10)

    plot = pg.PlotWidget()
    plot.setBackground("w")
    plot.setTitle("Rainfall Distribution", color="k", size="12pt")
    plot.setLabel("left",  "Frequency")
    plot.setLabel("bottom", "Rainfall (mm)")
    plot.showGrid(x=True, y=True, alpha=0.3)

    # Draw bars manually using BarGraphItem
    bar_width = bin_edges[1] - bin_edges[0]
    x_centers = bin_edges[:-1] + bar_width / 2

    bars = pg.BarGraphItem(
        x=x_centers,
        height=counts,
        width=bar_width * 0.85,
        brush=pg.mkBrush(100, 149, 237, 200),   # cornflower blue
        pen=pg.mkPen("w", width=0.5),
    )
    plot.addItem(bars)

    return plot