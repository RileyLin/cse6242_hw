#!/usr/bin/env python3
"""
Q1.1: Create a data table for popular board games
Grouped by Solo Support (min_players = 1 vs > 1)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.table import Table
import numpy as np

# Read the data
df = pd.read_csv('popular_board_game.csv')

# Create solo support column
df['solo_support'] = df['min_players'].apply(lambda x: 'Solo Supported' if x == 1 else 'Solo Not Supported')

# Group by solo_support and category
grouped = df.groupby(['solo_support', 'category'])

# Calculate statistics for each group
results = []
for (solo_support, category), group in grouped:
    # a. Total number of games
    total_games = len(group)
    
    # b. Game with highest number of ratings (if tie, take first)
    top_game_row = group.loc[group['num_ratings'].idxmax()]
    top_game = top_game_row['name']
    top_game_ratings = int(top_game_row['num_ratings'])
    
    # c. Average rating (rounded to 2 decimals)
    avg_rating = round(group['avg_rating'].mean(), 2)
    
    # d. Average playtime (use playtime_num, rounded to 2 decimals)
    avg_playtime = round(group['playtime_num'].mean(), 2)
    
    results.append({
        'Solo Support': solo_support,
        'Category': category,
        'Total Games': total_games,
        'Top Game': top_game,
        'Top Game Ratings': f'{top_game_ratings:,}',
        'Avg Rating': avg_rating,
        'Avg Playtime (min)': avg_playtime
    })

# Create DataFrame
result_df = pd.DataFrame(results)

# Sort by Solo Support (descending so "Solo Supported" comes first) and Category
result_df = result_df.sort_values(['Solo Support', 'Category'], ascending=[False, True])

# Create figure for the table
fig, ax = plt.subplots(figsize=(16, 10))
ax.axis('tight')
ax.axis('off')

# Prepare data for table display
# We'll create a multi-level header structure
solo_supported = result_df[result_df['Solo Support'] == 'Solo Supported'].copy()
solo_not_supported = result_df[result_df['Solo Support'] == 'Solo Not Supported'].copy()

# Create table data
table_data = []

# Header row
header = ['Category', 'Total\nGames', 'Top Game\n(by # Ratings)', '# Ratings', 'Avg\nRating', 'Avg Playtime\n(minutes)']
table_data.append(header)

# Add a separator row for "Solo Supported"
table_data.append(['SOLO SUPPORTED', '', '', '', '', ''])

# Add Solo Supported data
for _, row in solo_supported.iterrows():
    table_data.append([
        row['Category'],
        str(row['Total Games']),
        row['Top Game'],
        row['Top Game Ratings'],
        str(row['Avg Rating']),
        str(row['Avg Playtime (min)'])
    ])

# Add a separator row for "Solo Not Supported"
table_data.append(['SOLO NOT SUPPORTED', '', '', '', '', ''])

# Add Solo Not Supported data
for _, row in solo_not_supported.iterrows():
    table_data.append([
        row['Category'],
        str(row['Total Games']),
        row['Top Game'],
        row['Top Game Ratings'],
        str(row['Avg Rating']),
        str(row['Avg Playtime (min)'])
    ])

# Create table
table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                colWidths=[0.15, 0.08, 0.32, 0.12, 0.10, 0.15])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)

# Color scheme
header_color = '#2C3E50'
section_color = '#34495E'
solo_supported_color = '#E8F8F5'
solo_not_supported_color = '#FEF9E7'
border_color = '#95A5A6'

# Style header row (row 0)
for i in range(len(header)):
    cell = table[(0, i)]
    cell.set_facecolor(header_color)
    cell.set_text_props(weight='bold', color='white', ha='center')
    cell.set_edgecolor(border_color)

# Style section headers
section_rows = []
current_row = 1
# "SOLO SUPPORTED" header
section_rows.append(current_row)
current_row += len(solo_supported) + 1
# "SOLO NOT SUPPORTED" header
section_rows.append(current_row)

for row_idx in section_rows:
    for col_idx in range(len(header)):
        cell = table[(row_idx, col_idx)]
        cell.set_facecolor(section_color)
        cell.set_text_props(weight='bold', color='white', ha='left')
        cell.set_edgecolor(border_color)

# Style Solo Supported rows
for i in range(2, 2 + len(solo_supported)):
    for j in range(len(header)):
        cell = table[(i, j)]
        cell.set_facecolor(solo_supported_color)
        cell.set_edgecolor(border_color)
        if j == 0:  # Category column
            cell.set_text_props(weight='bold')
        elif j in [1, 3, 4, 5]:  # Numeric columns
            cell.set_text_props(ha='right')

# Style Solo Not Supported rows
start_row = 3 + len(solo_supported)
for i in range(start_row, start_row + len(solo_not_supported)):
    for j in range(len(header)):
        cell = table[(i, j)]
        cell.set_facecolor(solo_not_supported_color)
        cell.set_edgecolor(border_color)
        if j == 0:  # Category column
            cell.set_text_props(weight='bold')
        elif j in [1, 3, 4, 5]:  # Numeric columns
            cell.set_text_props(ha='right')

# Add title
plt.title('Popular Board Games: Solo Support Analysis', 
          fontsize=16, weight='bold', pad=20, loc='left')

# Add GT username in bottom left
fig.text(0.05, 0.02, 'wlin99', fontsize=10, ha='left', style='italic')

# Add legend/note
legend_text = 'Solo Supported: min_players = 1  |  Solo Not Supported: min_players > 1'
fig.text(0.5, 0.02, legend_text, fontsize=9, ha='center', style='italic', color='#7F8C8D')

plt.tight_layout(rect=[0, 0.03, 1, 0.98])

# Save as high-resolution PNG
plt.savefig('table.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Table saved as table.png")

# Also save the raw data for reference
result_df.to_csv('table_data.csv', index=False)
print("Data saved as table_data.csv")

