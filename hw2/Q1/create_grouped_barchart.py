#!/usr/bin/env python3
"""
Q1.2: Create a grouped bar chart for popular board games
Show game count by category and playtime
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data
df = pd.read_csv('popular_board_game.csv')

# Count games by category and playtime
grouped = df.groupby(['category', 'playtime']).size().reset_index(name='count')

# Get unique categories and playtimes
categories = sorted(df['category'].unique())
playtimes = ['<=30', '(30, 60]', '(60, 90]', '>90']  # Order by duration

# Create a pivot table for easier plotting
pivot_data = grouped.pivot(index='category', columns='playtime', values='count').fillna(0)

# Ensure all playtime categories are present in the correct order
for pt in playtimes:
    if pt not in pivot_data.columns:
        pivot_data[pt] = 0
pivot_data = pivot_data[playtimes]

# Create the grouped bar chart
fig, ax = plt.subplots(figsize=(14, 8))

# Set the width of bars and positions
bar_width = 0.2
x = np.arange(len(categories))

# Color scheme - use a professional palette
colors = ['#3498DB', '#E74C3C', '#F39C12', '#9B59B6']  # Blue, Red, Orange, Purple

# Create bars for each playtime group
for i, playtime in enumerate(playtimes):
    values = [pivot_data.loc[cat, playtime] if cat in pivot_data.index else 0 
              for cat in categories]
    offset = (i - len(playtimes)/2 + 0.5) * bar_width
    bars = ax.bar(x + offset, values, bar_width, label=playtime, color=colors[i], 
                   alpha=0.9, edgecolor='white', linewidth=1.2)
    
    # Add value labels on top of bars (optional, comment out if too cluttered)
    # for j, bar in enumerate(bars):
    #     height = bar.get_height()
    #     if height > 0:
    #         ax.text(bar.get_x() + bar.get_width()/2., height,
    #                f'{int(height)}',
    #                ha='center', va='bottom', fontsize=8)

# Customize the chart
ax.set_xlabel('Game Category', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel('Number of Games', fontsize=13, fontweight='bold', labelpad=10)
ax.set_title('Popular Board Games by Category and Playtime', 
             fontsize=16, fontweight='bold', pad=20)

# Set x-axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=0, ha='center')

# Customize y-axis
ax.set_ylim(0, max(pivot_data.max()) * 1.1)  # Add 10% padding at top
ax.yaxis.grid(True, linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# Legend
legend = ax.legend(title='Playtime (minutes)', 
                   loc='upper right', 
                   frameon=True, 
                   fontsize=10,
                   title_fontsize=11)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.9)

# Add GT username in bottom left
fig.text(0.08, 0.02, 'wlin99', fontsize=10, ha='left', style='italic', 
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))

# Styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout(rect=[0, 0.03, 1, 1])

# Save as high-resolution PNG
plt.savefig('grouped_barchart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Grouped bar chart saved as grouped_barchart.png")

# Print summary statistics
print("\nSummary Statistics:")
print(pivot_data)
print(f"\nTotal categories: {len(categories)}")
print(f"Total games: {df.shape[0]}")
print(f"\nBreakdown by playtime:")
for playtime in playtimes:
    total = int(pivot_data[playtime].sum())
    print(f"  {playtime}: {total} games")

