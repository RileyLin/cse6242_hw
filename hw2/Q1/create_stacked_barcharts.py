#!/usr/bin/env python3
"""
Q1.3: Create stacked bar charts for board games
Show game counts by category (x-axis) stacked by mechanic (colors)
Filter by Max.Players
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data
df = pd.read_csv('games_detailed_info_filtered.csv')

print(f"Total rows in dataset: {len(df)}")
print(f"\nUnique values:")
print(f"Categories: {sorted(df['Category'].unique())}")
print(f"Max Players: {sorted(df['Max.Players'].unique())}")
print(f"Mechanics: {len(df['Mechanics'].unique())} unique mechanics")

def create_stacked_barchart(filtered_df, filter_name, filename):
    """Create a stacked bar chart for the filtered data"""
    
    # Count games by category and mechanic
    grouped = filtered_df.groupby(['Category', 'Mechanics']).size().reset_index(name='count')
    
    # Get unique categories and mechanics
    categories = sorted(filtered_df['Category'].unique())
    mechanics = sorted(filtered_df['Mechanics'].unique())
    
    # Create pivot table
    pivot_data = grouped.pivot(index='Category', columns='Mechanics', values='count').fillna(0)
    
    # Sort mechanics by total count (descending) for better legend order
    mechanic_totals = pivot_data.sum(axis=0).sort_values(ascending=False)
    top_mechanics = mechanic_totals.head(10).index.tolist()  # Top 10 mechanics
    
    # If there are more than 10 mechanics, group the rest as "Other"
    if len(mechanics) > 10:
        pivot_data['Other'] = pivot_data[[m for m in mechanics if m not in top_mechanics]].sum(axis=1)
        pivot_data = pivot_data[top_mechanics + ['Other']]
    else:
        pivot_data = pivot_data[top_mechanics]
    
    # Create the stacked bar chart
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Color palette - use a diverse set of colors
    colors = ['#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#2ECC71',
              '#1ABC9C', '#E67E22', '#95A5A6', '#34495E', '#16A085',
              '#D35400', '#7F8C8D']
    
    # Create stacked bars
    bottom = np.zeros(len(categories))
    bars = []
    
    for i, mechanic in enumerate(pivot_data.columns):
        values = [pivot_data.loc[cat, mechanic] if cat in pivot_data.index else 0 
                  for cat in categories]
        bar = ax.bar(categories, values, bottom=bottom, label=mechanic, 
                     color=colors[i % len(colors)], alpha=0.9, 
                     edgecolor='white', linewidth=0.5)
        bars.append(bar)
        bottom += values
    
    # Customize the chart
    ax.set_xlabel('Game Category', fontsize=14, fontweight='bold', labelpad=12)
    ax.set_ylabel('Number of Games', fontsize=14, fontweight='bold', labelpad=12)
    
    title = f'Game Distribution by Category and Playing Mechanic\n({filter_name})'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=0, ha='center', fontsize=11)
    
    # Customize y-axis
    max_height = int(bottom.max())
    ax.set_ylim(0, max_height * 1.05)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Legend - place outside plot area
    legend = ax.legend(title='Playing Mechanic', 
                       loc='center left', 
                       bbox_to_anchor=(1, 0.5),
                       frameon=True, 
                       fontsize=9,
                       title_fontsize=11)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.95)
    
    # Add filter indicator box in top right
    filter_box_text = f'Filter: {filter_name}'
    ax.text(0.98, 0.98, filter_box_text, 
            transform=ax.transAxes,
            fontsize=11, 
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
    
    # Add GT username in bottom left
    fig.text(0.08, 0.02, 'wlin99', fontsize=10, ha='left', style='italic', 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))
    
    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout(rect=[0, 0.03, 0.85, 1])
    
    # Save as high-resolution PNG
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n{filename} saved successfully!")
    print(f"Total games in this chart: {len(filtered_df)}")
    print(f"Categories shown: {len(categories)}")
    print(f"Mechanics shown: {len(pivot_data.columns)}")
    
    # Print summary
    print(f"\nBreakdown by category:")
    for cat in categories:
        count = len(filtered_df[filtered_df['Category'] == cat])
        print(f"  {cat}: {count} games")
    
    plt.close()

# Create chart 1: 2 Players only
print("\n" + "="*60)
print("Creating stacked_barchart_1.png (2 Players)")
print("="*60)
df_2players = df[df['Max.Players'] == '2 Players']
create_stacked_barchart(df_2players, 'Max Players: 2 Players', 'stacked_barchart_1.png')

# Create chart 2: 4 Players only
print("\n" + "="*60)
print("Creating stacked_barchart_2.png (4 Players)")
print("="*60)
df_4players = df[df['Max.Players'] == '4 Players']
create_stacked_barchart(df_4players, 'Max Players: 4 Players', 'stacked_barchart_2.png')

print("\n" + "="*60)
print("Both charts created successfully!")
print("="*60)

