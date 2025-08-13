import pandas as pd
import matplotlib.pyplot as plt

def clean_production_data(df):
    """Cleans the production-related dataframes."""
    df = df.rename(columns={df.columns[0]: 'Date'})
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    product_cols = [col for col in df.columns]
    for col in product_cols:
        df[col] = pd.to_numeric(df[col].replace('-', '0').fillna(0))
    return df

def create_line_chart(series, title, xlabel, ylabel, filename):
    """Creates and saves a line chart."""
    plt.figure(figsize=(12, 6))
    series.plot(kind='line', marker='.', linestyle='-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Chart saved as {filename}")
    plt.close()

def create_bar_chart(series, title, xlabel, ylabel, filename):
    """Creates and saves a bar chart."""
    plt.figure(figsize=(10, 6))
    series.plot(kind='bar', color='teal')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Chart saved as {filename}")
    plt.close()

def create_pie_chart(series, title, filename):
    """Creates and saves a pie chart."""
    plt.figure(figsize=(8, 8))
    series.plot(kind='pie', autopct='%1.1f%%', startangle=90,
                wedgeprops=dict(width=0.4))
    plt.ylabel('') # Hides the y-label
    plt.title(title)
    plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Chart saved as {filename}")
    plt.close()


if __name__ == '__main__':
    excel_file = "production_history.xlsx"

    # Load and clean data
    bales_df = pd.read_excel(excel_file, sheet_name='bales_produced')
    bales_df = clean_production_data(bales_df)

    # --- 1. Daily Production Trend ---
    daily_total_bales = bales_df.sum(axis=1)
    create_line_chart(daily_total_bales, 'Daily Production Trend', 'Date', 'Total Bales Produced', 'daily_production_trend.png')

    # --- 2. Monthly Production Trend ---
    monthly_total_bales = daily_total_bales.resample('M').sum()
    monthly_total_bales.index = monthly_total_bales.index.strftime('%Y-%m')
    create_bar_chart(monthly_total_bales, 'Monthly Production Trend', 'Month', 'Total Bales Produced', 'monthly_production_trend.png')

    # --- 3. Quarterly Production Trend ---
    quarterly_total_bales = daily_total_bales.resample('Q').sum()
    quarterly_total_bales.index = quarterly_total_bales.index.to_period('Q').astype(str)
    create_bar_chart(quarterly_total_bales, 'Quarterly Production Trend', 'Quarter', 'Total Bales Produced', 'quarterly_production_trend.png')

    # --- 4. Production Mix ---
    total_production_mix = bales_df.sum(axis=0)
    # Exclude products with zero production from the pie chart to avoid clutter
    total_production_mix = total_production_mix[total_production_mix > 0]
    create_pie_chart(total_production_mix, 'Production Mix by Bales Produced', 'production_mix_pie_chart.png')
