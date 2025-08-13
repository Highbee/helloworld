"""
This script generates a comprehensive suite of performance analysis charts for a
cotton factory based on production data from an Excel file.

It is designed to produce high-quality, visually appealing, and insightful
infographics that address the user's feedback for more detail and clarity.

-------------------------------------------------------------------------------
Requirements:
- Python 3
- The following Python packages: pandas, openpyxl, matplotlib, seaborn

Installation:
To install the required packages, run the following command in your terminal:
pip install pandas openpyxl matplotlib seaborn

Usage:
1. Make sure the `production_history.xlsx` file is in the same directory as
   this script.
2. Run the script from your terminal: python generate_infographics.py
3. The script will generate seven .png image files in the same directory,
   each containing a different analysis chart.
-------------------------------------------------------------------------------

The script produces the following reports:
1. Monthly Production Report (grouped by product)
2. Quarterly Production Report (grouped by product)
3. Enhanced Bale Weight Accuracy Radar Chart (with explanatory notes)
4. Monthly Bale Target Achievement Chart (color-coded for performance)
5. Monthly Weight Target Achievement Chart (color-coded for performance)
6. Enhanced Daily Production Trend Line Chart (with annotations)
7. Enhanced Production Mix Donut Chart
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
MONTHLY_TARGET_BALE_COL = ' (bales/ carton)'
MONTHLY_TARGET_WEIGHT_COL = 'cotton_weight (kg)'

# --- Data Loading and Cleaning ---

def load_all_data(file_path):
    """Loads all necessary sheets from the Excel file."""
    try:
        xls = pd.ExcelFile(file_path)
        data = {
            'bales_produced': xls.parse('bales_produced'),
            'cotton_used': xls.parse('cotton_used_in_production'),
            'acceptable_weight': xls.parse('acceptable_weight_per_bale'),
            'monthly_target': xls.parse('monthly_target'),
        }
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def clean_data(df):
    """Generic cleaning for production-related dataframes."""
    df = df.rename(columns={df.columns[0]: 'Date'})
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    product_cols = [col for col in df.columns if col != 'Date']
    for col in product_cols:
        df[col] = pd.to_numeric(df[col].replace('-', '0').fillna(0), errors='coerce')

    return df

# --- Chart Generation Functions ---

def create_grouped_bar_chart(df, period, title, filename):
    """Creates a grouped bar chart for monthly or quarterly data."""
    df = df.set_index('Date')

    if period == 'M':
        resampled_df = df.resample('ME').sum()
        resampled_df.index = resampled_df.index.strftime('%B %Y')
        xlabel = "Month"
    elif period == 'Q':
        resampled_df = df.resample('QE').sum()
        resampled_df.index = resampled_df.index.to_period('Q').astype(str)
        xlabel = "Quarter"
    else: return

    long_df = resampled_df.reset_index().melt(id_vars='Date', var_name='Product', value_name='Bales Produced')
    long_df = long_df.rename(columns={'Date': xlabel})

    plt.figure(figsize=(15, 8))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(data=long_df, x=xlabel, y='Bales Produced', hue='Product', palette='viridis')

    ax.set_title(title, fontsize=18, weight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("Bales Produced", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Product', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.figtext(0.5, 0.01, 'This chart shows the production volume for each product, grouped by time period.', ha='center', fontsize=10, style='italic')
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(filename, dpi=300)
    print(f"Chart saved as {filename}")
    plt.close()

def create_enhanced_radar_chart(bales_df, cotton_df, acceptable_df, filename):
    """Creates a visually enhanced radar chart with explanatory notes."""
    product_cols = [col for col in bales_df.columns if col not in ['Date', 'Cotton Balls']]

    total_bales = bales_df[product_cols].sum()
    total_cotton = cotton_df[product_cols].sum()
    avg_weights = (total_cotton / total_bales).fillna(0)

    acceptable_df['Product'] = acceptable_df['Product'].str.strip()
    ranges = acceptable_df['Acceptable_weight_range_per_bale (kg)'].str.split('-', expand=True)
    acceptable_df['min_weight'] = pd.to_numeric(ranges[0])
    acceptable_df['max_weight'] = pd.to_numeric(ranges[1])
    acceptable_df = acceptable_df.set_index('Product')

    radar_df = pd.DataFrame({'Produced': avg_weights, 'Min Acceptable': acceptable_df['min_weight'], 'Max Acceptable': acceptable_df['max_weight']}).loc[avg_weights.index].T

    categories = list(radar_df.columns)
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    plt.style.use('seaborn-v0_8-whitegrid')

    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1); ax.set_rlabel_position(0)
    plt.xticks(angles[:-1], categories, color='grey', size=12)

    ax.plot(angles, radar_df.loc['Min Acceptable'].tolist() + radar_df.loc['Min Acceptable'].tolist()[:1], linewidth=1, linestyle='dashed', label='Min Acceptable', color='green')
    ax.plot(angles, radar_df.loc['Max Acceptable'].tolist() + radar_df.loc['Max Acceptable'].tolist()[:1], linewidth=1, linestyle='dashed', label='Max Acceptable', color='red')
    ax.plot(angles, radar_df.loc['Produced'].tolist() + radar_df.loc['Produced'].tolist()[:1], linewidth=2, linestyle='solid', label='Produced', color='blue')
    ax.fill(angles, radar_df.loc['Produced'].tolist() + radar_df.loc['Produced'].tolist()[:1], 'blue', alpha=0.1)

    ax.set_title('Bale Weight Accuracy (kg)', size=20, color='black', y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.figtext(0.5, 0.01, "Note: The 'Produced' line should ideally fall between the 'Min' and 'Max' acceptable lines.", ha='center', fontsize=12, style='italic', color='black')
    plt.tight_layout(); plt.savefig(filename, dpi=300, bbox_inches='tight'); plt.close()
    print(f"Chart saved as {filename}")

def create_enhanced_target_chart(actual_series, target_series, title, filename):
    """Creates a visually enhanced bar chart for target achievement."""
    achievement_pct = (actual_series / target_series * 100).fillna(0)

    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid")

    colors = ['#d73027' if x < 100 else '#1a9850' for x in achievement_pct]
    ax = sns.barplot(x=achievement_pct.index, y=achievement_pct.values, palette=colors)

    ax.set_title(title, fontsize=18, weight='bold')
    ax.set_ylabel('Percentage of Target Achieved (%)', fontsize=12)
    ax.axhline(100, color='black', linestyle='--', linewidth=1.5, label='100% Target')

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                    textcoords='offset points')

    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")

def create_enhanced_line_chart(df, title, filename):
    """Creates a visually enhanced line chart for daily production trends."""
    daily_total = df.set_index('Date').sum(axis=1)

    plt.figure(figsize=(15, 7))
    sns.set_theme(style="whitegrid")
    ax = sns.lineplot(x=daily_total.index, y=daily_total.values, marker='o', color='b')

    ax.set_title(title, fontsize=18, weight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Total Bales Produced", fontsize=12)

    # Annotate peak and lowest production days
    peak_day = daily_total.idxmax()
    peak_val = daily_total.max()
    ax.annotate(f'Peak: {peak_val} bales\n({peak_day.date()})', xy=(peak_day, peak_val),
                xytext=(peak_day, peak_val + 10), arrowprops=dict(facecolor='black', shrink=0.05),
                ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")

def create_enhanced_pie_chart(df, title, filename):
    """Creates a visually enhanced donut chart for production mix."""
    total_production_mix = df.drop(columns='Date').sum()
    total_production_mix = total_production_mix[total_production_mix > 0]

    plt.figure(figsize=(10, 10))
    plt.style.use('seaborn-v0_8-whitegrid')

    colors = sns.color_palette('pastel')[0:len(total_production_mix)]

    plt.pie(total_production_mix, labels=total_production_mix.index, colors=colors,
            autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    # Draw a circle at the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title(title, fontsize=18, weight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Chart saved as {filename}")


def main():
    """Main function to generate all reports."""
    print("Starting all report generation...")
    file_path = "production_history.xlsx"
    data = load_all_data(file_path)

    if data:
        bales_df = clean_data(data['bales_produced'])
        cotton_df = clean_data(data['cotton_used'])
        target_df = data['monthly_target']

        # --- Monthly and Quarterly Reports ---
        create_grouped_bar_chart(bales_df.copy(), 'M', 'Monthly Production Performance by Product', 'monthly_production_report.png')
        create_grouped_bar_chart(bales_df.copy(), 'Q', 'Quarterly Production Performance by Product', 'quarterly_production_report.png')

        # --- Radar Chart ---
        create_enhanced_radar_chart(bales_df.copy(), cotton_df.copy(), data['acceptable_weight'], 'enhanced_radar_chart.png')

        # --- Target Achievement Charts ---
        latest_date = bales_df['Date'].max()
        last_full_month = latest_date.to_period('M') - 1
        last_month_filter = (bales_df['Date'] >= last_full_month.start_time) & (bales_df['Date'] <= last_full_month.end_time)
        product_cols = [col for col in bales_df.columns if col not in ['Date', 'Cotton Balls']]
        actual_bales = bales_df[last_month_filter][product_cols].sum()
        actual_weight = cotton_df[last_month_filter][product_cols].sum()
        target_df = target_df.rename(columns={target_df.columns[0]: 'Product', MONTHLY_TARGET_BALE_COL: 'Target Bales', MONTHLY_TARGET_WEIGHT_COL: 'Target Weight'})
        target_df['Product'] = target_df['Product'].str.strip()
        target_df = target_df.set_index('Product')
        target_bales = target_df['Target Bales'].loc[actual_bales.index]
        target_weight = target_df['Target Weight'].loc[actual_weight.index]
        month_name = last_full_month.strftime('%B %Y')
        create_enhanced_target_chart(actual_bales, target_bales, f'Monthly Bale Target Achievement - {month_name}', 'enhanced_bale_target_chart.png')
        create_enhanced_target_chart(actual_weight, target_weight, f'Monthly Weight Target Achievement - {month_name}', 'enhanced_weight_target_chart.png')

        # --- Other Performance Dashboards ---
        create_enhanced_line_chart(bales_df.copy(), 'Daily Production Trend', 'enhanced_daily_trend.png')
        create_enhanced_pie_chart(bales_df.copy(), 'Overall Production Mix', 'enhanced_production_mix.png')

        print("\nAll reports generated successfully.")

if __name__ == '__main__':
    main()
