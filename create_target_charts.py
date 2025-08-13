import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clean_production_data(df):
    """Cleans the production-related dataframes."""
    df = df.rename(columns={df.columns[0]: 'Date'})
    df['Date'] = pd.to_datetime(df['Date'])
    product_cols = [col for col in df.columns if col != 'Date']
    for col in product_cols:
        df[col] = pd.to_numeric(df[col].replace('-', '0').fillna(0))
    return df

def get_last_full_month_data(df):
    """Filters the dataframe to only include data from the last full month."""
    latest_date = df['Date'].max()
    last_full_month = latest_date.to_period('M') - 1

    start_date = last_full_month.start_time
    end_date = last_full_month.end_time

    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

def prepare_target_data(df, target_col, weight_col):
    """Prepares the target dataframe."""
    df = df.rename(columns={df.columns[0]: 'Product',
                            target_col: 'Target Bales',
                            weight_col: 'Target Weight'})
    df['Product'] = df['Product'].str.strip()
    df = df.set_index('Product')
    return df[['Target Bales', 'Target Weight']]

def create_achievement_chart(actual_series, target_series, title, filename):
    """Creates and saves a bar chart showing percentage achievement."""
    # Align data and calculate percentage
    achievement_pct = (actual_series / target_series * 100).fillna(0)

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(achievement_pct.index, achievement_pct.values, color='skyblue')

    # Add percentage labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

    ax.set_ylabel('Percentage of Target Achieved (%)')
    ax.set_title(title)
    ax.axhline(100, color='red', linestyle='--', linewidth=1, label='100% Target')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()

    # Save the chart
    plt.savefig(filename, dpi=300)
    print(f"Chart saved as {filename}")

if __name__ == '__main__':
    excel_file = "production_history.xlsx"

    # Load data
    bales_df = pd.read_excel(excel_file, sheet_name='bales_produced')
    cotton_df = pd.read_excel(excel_file, sheet_name='cotton_used_in_production')
    monthly_target_df = pd.read_excel(excel_file, sheet_name='monthly_target')

    # Clean data
    bales_df = clean_production_data(bales_df)
    cotton_df = clean_production_data(cotton_df)

    # Get data for the last full month
    last_month_bales = get_last_full_month_data(bales_df)
    last_month_cotton = get_last_full_month_data(cotton_df)

    # Get product columns (excluding Date and Cotton Balls for now)
    product_cols = [col for col in bales_df.columns if col not in ['Date', 'Cotton Balls']]

    # Calculate actuals for the last month
    actual_bales = last_month_bales[product_cols].sum()
    actual_weight = last_month_cotton[product_cols].sum()

    # Prepare target data
    # Note: The column names in the excel file are a bit ambiguous
    # Assuming ' (bales/ carton)' is the bale target and 'cotton_weight (kg)' is the weight target.
    monthly_targets = prepare_target_data(monthly_target_df, ' (bales/ carton)', 'cotton_weight (kg)')

    # Align target data with production data
    target_bales = monthly_targets['Target Bales'].loc[actual_bales.index]
    target_weight = monthly_targets['Target Weight'].loc[actual_weight.index]

    # Create and save charts
    create_achievement_chart(actual_bales, target_bales,
                             'Monthly Bale Production vs. Target',
                             'monthly_bale_target_achievement.png')

    create_achievement_chart(actual_weight, target_weight,
                             'Monthly Cotton Weight vs. Target',
                             'monthly_weight_target_achievement.png')
