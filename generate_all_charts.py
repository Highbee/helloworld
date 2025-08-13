# -*- coding: utf-8 -*-
"""
This script generates a series of performance analysis charts for a cotton factory
based on production data from an Excel file.

Requirements:
- Python 3
- The following Python packages: pandas, openpyxl, matplotlib, plotly

Installation:
To install the required packages, run the following command in your terminal:
pip install pandas openpyxl matplotlib plotly

Usage:
1. Make sure the `production_history.xlsx` file is in the same directory as this script.
2. Run the script from your terminal: python generate_all_charts.py
3. The script will generate several .png image files with the analysis charts.

It produces the following reports:
1. A radar chart for bale weight accuracy.
2. Bar charts for monthly target achievement (bales and cotton weight).
3. A suite of performance dashboards (daily, monthly, quarterly trends, and production mix).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
EXCEL_FILE_PATH = "production_history.xlsx"
# Correcting the column name with a leading space as discovered during debugging.
MONTHLY_TARGET_BALE_COL = ' (bales/ carton)'
MONTHLY_TARGET_WEIGHT_COL = 'cotton_weight (kg)'


# --- Data Loading and Cleaning ---

def load_all_data(file_path):
    """Loads all necessary sheets from the Excel file."""
    try:
        xls = pd.ExcelFile(file_path)
        data = {
            'bales': xls.parse('bales_produced'),
            'cotton': xls.parse('cotton_used_in_production'),
            'acceptable_weight': xls.parse('acceptable_weight_per_bale'),
            'monthly_target': xls.parse('monthly_target')
        }
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def clean_production_data(df, set_date_index=False):
    """Generic cleaning for production-related dataframes."""
    df = df.rename(columns={df.columns[0]: 'Date'})
    df['Date'] = pd.to_datetime(df['Date'])

    if set_date_index:
        df = df.set_index('Date')

    product_cols = [col for col in df.columns if col not in ['Date']]
    for col in product_cols:
        df[col] = pd.to_numeric(df[col].replace('-', '0').fillna(0))
    return df


# --- Chart Generation Functions ---

def create_radar_chart(df, title, filename):
    """Creates and saves a radar chart."""
    categories = list(df.columns)
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)

    for i, row in df.iterrows():
        values = row.values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=row.name)
        ax.fill(angles, values, alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title(title, size=14, y=1.1)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved as {filename}")

def create_achievement_bar_chart(actual, target, title, filename):
    """Creates a bar chart showing percentage achievement against a target."""
    achievement_pct = (actual / target * 100).fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(achievement_pct.index, achievement_pct.values, color='skyblue')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

    ax.set_ylabel('Percentage of Target Achieved (%)')
    ax.set_title(title)
    ax.axhline(100, color='red', linestyle='--', linewidth=1, label='100% Target')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")

def create_trend_line_chart(series, title, filename):
    """Creates a time-series line chart."""
    plt.figure(figsize=(12, 6))
    series.plot(kind='line', marker='.', linestyle='-')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Total Bales Produced')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")

def create_trend_bar_chart(series, title, xlabel, filename):
    """Creates a bar chart for trends (monthly, quarterly)."""
    plt.figure(figsize=(10, 6))
    series.plot(kind='bar', color='teal')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Total Bales Produced')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")

def create_pie_chart(series, title, filename):
    """Creates a pie chart."""
    series = series[series > 0] # Exclude zero values
    plt.figure(figsize=(8, 8))
    series.plot(kind='pie', autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
    plt.ylabel('')
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")


# --- Main Report Generation Logic ---

def generate_weight_accuracy_report(bales_df, cotton_df, acceptable_df):
    """Generates the radar chart for bale weight accuracy."""
    print("\n--- Generating Bale Weight Accuracy Report ---")
    product_cols = [col for col in bales_df.columns if col not in ['Date', 'Cotton Balls']]

    total_bales = bales_df[product_cols].sum()
    total_cotton = cotton_df[product_cols].sum()
    avg_weights = (total_cotton / total_bales).fillna(0)

    acceptable_df['Product'] = acceptable_df['Product'].str.strip()
    ranges = acceptable_df['Acceptable_weight_range_per_bale (kg)'].str.split('-', expand=True)
    acceptable_df['min_weight'] = pd.to_numeric(ranges[0])
    acceptable_df['max_weight'] = pd.to_numeric(ranges[1])
    acceptable_df = acceptable_df.set_index('Product')

    radar_df = pd.DataFrame({
        'Produced': avg_weights,
        'Min Acceptable': acceptable_df['min_weight'],
        'Max Acceptable': acceptable_df['max_weight']
    }).loc[avg_weights.index].T

    create_radar_chart(radar_df, 'Bale Weight Accuracy (kg)', 'radar_chart.png')

def generate_target_achievement_report(bales_df, cotton_df, target_df):
    """Generates bar charts for monthly target achievement."""
    print("\n--- Generating Target Achievement Report ---")
    latest_date = bales_df['Date'].max()
    last_full_month = latest_date.to_period('M') - 1
    last_month_filter = (bales_df['Date'] >= last_full_month.start_time) & (bales_df['Date'] <= last_full_month.end_time)

    product_cols = [col for col in bales_df.columns if col not in ['Date', 'Cotton Balls']]

    actual_bales = bales_df[last_month_filter][product_cols].sum()
    actual_weight = cotton_df[last_month_filter][product_cols].sum()

    target_df = target_df.rename(columns={
        target_df.columns[0]: 'Product',
        MONTHLY_TARGET_BALE_COL: 'Target Bales',
        MONTHLY_TARGET_WEIGHT_COL: 'Target Weight'
    })
    target_df['Product'] = target_df['Product'].str.strip()
    target_df = target_df.set_index('Product')

    target_bales = target_df['Target Bales'].loc[actual_bales.index]
    target_weight = target_df['Target Weight'].loc[actual_weight.index]

    create_achievement_bar_chart(actual_bales, target_bales, 'Monthly Bale Production vs. Target', 'monthly_bale_target_achievement.png')
    create_achievement_bar_chart(actual_weight, target_weight, 'Monthly Cotton Weight vs. Target', 'monthly_weight_target_achievement.png')

def generate_performance_dashboard_report(bales_df_indexed):
    """Generates daily, monthly, quarterly, and mix dashboards."""
    print("\n--- Generating Overall Performance Dashboards ---")
    daily_total = bales_df_indexed.sum(axis=1)

    # Daily
    create_trend_line_chart(daily_total, 'Daily Production Trend', 'daily_production_trend.png')

    # Monthly
    monthly_total = daily_total.resample('ME').sum()
    monthly_total.index = monthly_total.index.strftime('%Y-%m')
    create_trend_bar_chart(monthly_total, 'Monthly Production Trend', 'Month', 'monthly_production_trend.png')

    # Quarterly
    quarterly_total = daily_total.resample('QE').sum()
    quarterly_total.index = quarterly_total.index.to_period('Q').astype(str)
    create_trend_bar_chart(quarterly_total, 'Quarterly Production Trend', 'Quarter', 'quarterly_production_trend.png')

    # Mix
    total_mix = bales_df_indexed.sum(axis=0)
    create_pie_chart(total_mix, 'Production Mix by Bales Produced', 'production_mix_pie_chart.png')


# --- Main Execution ---

def main():
    """Main function to run all report generation."""
    print("Starting report generation...")

    data = load_all_data(EXCEL_FILE_PATH)
    if data is None:
        return

    # Clean dataframes
    bales_cleaned = clean_production_data(data['bales'])
    cotton_cleaned = clean_production_data(data['cotton'])
    bales_cleaned_indexed = clean_production_data(data['bales'].copy(), set_date_index=True)

    # Generate all reports
    generate_weight_accuracy_report(bales_cleaned, cotton_cleaned, data['acceptable_weight'])
    generate_target_achievement_report(bales_cleaned, cotton_cleaned, data['monthly_target'])
    generate_performance_dashboard_report(bales_cleaned_indexed)

    print("\nAll reports generated successfully.")

if __name__ == '__main__':
    main()
