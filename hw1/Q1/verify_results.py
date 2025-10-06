#!/usr/bin/env python3
"""Verify the results of Q4 data cleaning."""

import pandas as pd

def main():
    # Load the cleaned data
    df = pd.read_csv('/Users/mxy1998/Documents/rileygit/6242_hw1/Q1/Q4.csv')
    
    print("=== Q4 Data Cleaning Results Verification ===\n")
    
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    
    print("\n=== Airport Column Analysis ===")
    airport_counts = df['Airport'].value_counts()
    print(f"Unique airports: {len(airport_counts)}")
    print(f"Rows with airport extracted: {len(df[df['Airport'] != ''])}")
    print(f"Rows without airport extracted: {len(df[df['Airport'] == ''])}")
    
    print("\n=== Top 10 Airports by Incident Count ===")
    print(airport_counts.head(10))
    
    print("\n=== Sample Records with Airport Extraction ===")
    sample_df = df[df['Airport'] != ''][['Subject', 'Airport']].head(10)
    for idx, row in sample_df.iterrows():
        print(f"Subject: {row['Subject'][:80]}...")
        print(f"Airport: {row['Airport']}")
        print("-" * 50)
    
    print("\n=== Common Name Check ===")
    print(f"Null/empty Common Names: {df['Common Name'].isnull().sum() + (df['Common Name'] == '').sum()}")
    
    print("\n=== Airport Keyword Check ===")
    airport_mentions = df['Subject'].str.contains('Airport', na=False).sum()
    print(f"Rows mentioning 'Airport' in Subject: {airport_mentions}")
    print(f"Total rows: {len(df)}")
    print(f"Match rate: {airport_mentions/len(df)*100:.1f}%")

if __name__ == "__main__":
    main()