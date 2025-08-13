import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_data(df):
    """Renames the date column, drops Cotton Balls, and converts values to numeric."""
    # Rename the first column to 'Date'
    df = df.rename(columns={df.columns[0]: 'Date'})
    # Drop the 'Cotton Balls' column if it exists
    if 'Cotton Balls' in df.columns:
        df = df.drop(columns=['Cotton Balls'])
    # Replace non-numeric placeholders and convert to numbers
    for col in df.columns:
        if col != 'Date':
            df[col] = pd.to_numeric(df[col].replace('-', '0').fillna(0))
    return df

def calculate_average_weights(bales_df, cotton_df):
    """Calculates the average weight per bale for each product."""
    # Get product columns (all columns except 'Date')
    product_cols = [col for col in bales_df.columns if col != 'Date']

    # Sum up total production and total cotton used for each product
    total_bales = bales_df[product_cols].sum()
    total_cotton = cotton_df[product_cols].sum()

    # Calculate average weight, handling division by zero
    average_weights = (total_cotton / total_bales).fillna(0)
    return average_weights

def prepare_radar_data(avg_weights, acceptable_df):
    """Prepares the DataFrame for the radar chart."""
    # Clean up product names in acceptable_df
    acceptable_df['Product'] = acceptable_df['Product'].str.strip()

    # Parse the min/max weight ranges
    ranges = acceptable_df['Acceptable_weight_range_per_bale (kg)'].str.split('-', expand=True)
    acceptable_df['min_weight'] = pd.to_numeric(ranges[0])
    acceptable_df['max_weight'] = pd.to_numeric(ranges[1])

    # Set Product as index
    acceptable_df = acceptable_df.set_index('Product')

    # Create the radar chart dataframe
    radar_df = pd.DataFrame({
        'Produced': avg_weights,
        'Min Acceptable': acceptable_df['min_weight'],
        'Max Acceptable': acceptable_df['max_weight']
    })

    # Ensure the order of products matches the original for consistency
    radar_df = radar_df.loc[avg_weights.index]

    return radar_df.T # Transpose so products are columns

def create_radar_chart(df, title='Bale Weight Accuracy (kg)'):
    """Creates and saves a radar chart."""
    categories = list(df.columns)
    N = len(categories)

    # Set up the angles for the radar chart
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1] # close the loop

    # Initialize the plot
    ax = plt.subplot(111, polar=True)

    # Set the first axis to be on top
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw the axis labels
    plt.xticks(angles[:-1], categories)

    # Draw y-labels
    ax.set_rlabel_position(0)

    # Plot each series
    for i, row in df.iterrows():
        values = row.values.flatten().tolist()
        values += values[:1] # close the loop
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=row.name)
        ax.fill(angles, values, alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title(title, size=14, y=1.1)

    # Save the chart to a file
    plt.savefig('radar_chart.png', dpi=300, bbox_inches='tight')
    print("Radar chart saved as radar_chart.png")

if __name__ == '__main__':
    # Define file path
    excel_file = "production_history.xlsx"

    # Load data
    bales_produced_df = pd.read_excel(excel_file, sheet_name='bales_produced')
    cotton_used_df = pd.read_excel(excel_file, sheet_name='cotton_used_in_production')
    acceptable_weight_df = pd.read_excel(excel_file, sheet_name='acceptable_weight_per_bale')

    # Clean data
    bales_produced_df = clean_data(bales_produced_df)
    cotton_used_df = clean_data(cotton_used_df)

    # Calculate average weights
    avg_weights = calculate_average_weights(bales_produced_df, cotton_used_df)

    # Prepare data for plotting
    radar_df = prepare_radar_data(avg_weights, acceptable_weight_df)

    # Create and save the chart
    create_radar_chart(radar_df)
