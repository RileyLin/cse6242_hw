# Q4 Data Cleaning - Python Alternative to OpenRefine

This Python solution provides an alternative to OpenRefine for cleaning wildlife trafficking incident data, specifically addressing macOS security restrictions that prevent OpenRefine from opening.

## Overview

The data cleaning pipeline processes wildlife trafficking incidents from CITES data, focusing on airport-related incidents. It performs the following operations:

1. **Filter blank Common Names**: Removes rows with null or empty 'Common Name' values
2. **Filter Airport incidents**: Keeps only rows mentioning "Airport" (case-sensitive) in the 'Subject' column
3. **Extract Airport names**: Creates a new 'Airport' column with standardized airport names
4. **Cluster similar airports**: Merges similar airport names to reduce duplicates
5. **Export results**: Saves cleaned data as Q4.csv and operation history as history.json

## Files Generated

- **Q4.csv**: Cleaned dataset with 1,764 rows and 15 columns (original 14 + new Airport column)
- **history.json**: Complete operation log documenting all transformations performed
- **Q4_data_cleaning.py**: Main cleaning script
- **verify_results.py**: Verification script to validate results

## Results Summary

- **Original dataset**: 23,861 rows
- **After removing blank Common Names**: 16,612 rows (-7,249 rows)
- **After filtering for Airport incidents**: 1,764 rows (-14,848 rows)
- **Airport names extracted**: 1,700 out of 1,764 rows (96.4% success rate)
- **Unique airports identified**: 260 (after clustering)

### Top 10 Airports by Incident Count:
1. Guangzhou Baiyun International Airport (154 incidents)
2. Hong Kong International Airport (94 incidents)
3. Chengdu Shuangliu International Airport (55 incidents)
4. Shanghai Pudong International Airport (49 incidents)
5. Qingdao Liuting International Airport (47 incidents)
6. Hangzhou Xiaoshan International Airport (41 incidents)
7. Kunming Changshui International Airport (40 incidents)
8. Hanoi Noi Bai International Airport (38 incidents)
9. Chennai International Airport (37 incidents)
10. Tan Son Nhat International Airport (35 incidents)

## Technical Implementation

### Airport Name Extraction
The script uses multiple regex patterns to extract airport names:
- `at [the] <Airport Name> Airport` (most specific)
- `seized at/in <Airport Name>`
- `from <Airport Name>`
- General `<Airport Name> Airport` patterns

### Name Validation
Extracted airport names are validated to ensure they:
- End with "Airport"
- Don't contain measurements (kg), animal names, or other invalid content
- Start with capital letters (proper nouns)
- Are reasonable length (< 60 characters)

### Clustering Algorithm
Similar airport names are merged using normalized comparison:
- Removes common words (International, Airport, etc.)
- Handles abbreviations (Intl → International)
- Groups variations of the same airport name

## Usage

### Running the Data Cleaning Pipeline
```bash
python3 Q4_data_cleaning.py
```

### Verifying Results
```bash
python3 verify_results.py
```

## Dependencies
- pandas: Data manipulation and analysis
- re: Regular expressions for text processing
- json: JSON file handling
- datetime: Timestamp generation
- pathlib: File path operations

## Data Quality Notes

1. **100% Airport Filtering**: All 1,764 rows contain "Airport" in the Subject field
2. **96.4% Airport Extraction**: 1,700 out of 1,764 rows have successfully extracted airport names
3. **Zero Blank Common Names**: All rows have valid Common Name values
4. **90 Clustering Groups**: Similar airport names were merged, reducing unique airports from 398 to 260

## History File Structure

The history.json file contains:
- **Summary**: Pipeline completion info, statistics, and file paths
- **Operations**: Detailed log of each transformation step with before/after counts
- **Timestamps**: ISO format timestamps for each operation
- **Validation metrics**: Success rates and data quality measures

This Python solution provides equivalent functionality to OpenRefine while being more reproducible and scriptable for future use.