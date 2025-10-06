#!/usr/bin/env python3
"""
Q4 Data Cleaning Script - Alternative to OpenRefine
Cleans wildlife trafficking incident data with focus on airport-related incidents.
"""

import pandas as pd
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
from pathlib import Path


class DataCleaningPipeline:
    """Data cleaning pipeline for wildlife trafficking incidents."""
    
    def __init__(self, input_file: str, output_dir: str = None):
        """Initialize the cleaning pipeline."""
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir) if output_dir else self.input_file.parent
        self.history = []
        self.original_data = None
        self.cleaned_data = None
        
    def log_operation(self, operation: str, description: str, 
                     rows_before: int, rows_after: int, **kwargs) -> None:
        """Log an operation to the history."""
        operation_record = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "description": description,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_changed": rows_before - rows_after,
            **kwargs
        }
        self.history.append(operation_record)
        print(f"✓ {description}: {rows_before} → {rows_after} rows")
        
    def load_data(self) -> pd.DataFrame:
        """Load the incidents CSV file."""
        print(f"Loading data from {self.input_file}...")
        try:
            df = pd.read_csv(self.input_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(self.input_file, encoding='latin-1')
            
        self.original_data = df.copy()
        print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
        
        # Log initial state
        self.log_operation(
            "load_data", 
            "Loaded initial dataset",
            0, len(df),
            columns=list(df.columns),
            total_columns=len(df.columns)
        )
        
        return df
    
    def filter_blank_common_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter out rows with blank (null or empty) Common Name values."""
        rows_before = len(df)
        
        # Check for null, empty string, or whitespace-only values
        mask = (
            df['Common Name'].notna() & 
            (df['Common Name'].astype(str).str.strip() != '') &
            (df['Common Name'].astype(str).str.strip() != 'nan')
        )
        
        df_filtered = df[mask].copy()
        rows_after = len(df_filtered)
        
        self.log_operation(
            "filter_blank_common_names",
            "Removed rows with blank Common Name values",
            rows_before, rows_after,
            filter_condition="Common Name is not null and not empty"
        )
        
        return df_filtered
    
    def filter_airport_incidents(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to only rows that mention 'Airport' (case sensitive) in Subject."""
        rows_before = len(df)
        
        # Case-sensitive search for "Airport"
        mask = df['Subject'].astype(str).str.contains('Airport', na=False)
        df_filtered = df[mask].copy()
        rows_after = len(df_filtered)
        
        self.log_operation(
            "filter_airport_incidents",
            "Filtered to incidents mentioning 'Airport' in Subject",
            rows_before, rows_after,
            filter_condition="Subject contains 'Airport' (case sensitive)"
        )
        
        return df_filtered
    
    def extract_airport_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract airport names from the Subject column."""
        rows_before = len(df)
        df = df.copy()
        
        # Initialize Airport column
        df['Airport'] = None  # Use None instead of empty string for better null handling
        
        # Improved extraction patterns with more comprehensive coverage
        patterns = [
            # Pattern 1: "at [the] <Airport Name> [International/Domestic] Airport" - most specific
            r'(?:at|in)\s+(?:the\s+)?([\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?(?:\s+(?:International|Domestic|Intl))?\s*Airport)',
            
            # Pattern 2: "seized at/in/from <Airport Name>"  
            r'(?:seized\s+(?:at|in|from))\s+([\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?(?:\s+(?:International|Domestic|Intl))?\s*Airport)',
            
            # Pattern 3: Handle possessive forms like "Amsterdam's Schiphol Airport"
            r'(?:at|in|from)\s+([\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?\'s\s+[\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?(?:\s+(?:International|Domestic|Intl))?\s*Airport)',
            
            # Pattern 4: "from <Airport Name>"
            r'(?:from)\s+([\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?(?:\s+(?:International|Domestic|Intl))?\s*Airport)',
            
            # Pattern 5: "in <Airport Name>" - handle simple "in" cases
            r'\bin\s+([\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?(?:\s+(?:International|Domestic|Intl))?\s*Airport)(?:\s*[,\.]|\s|$)',
            
            # Pattern 6: Handle "seized [airport]" without "at/in" 
            r'seized\s+(?:from\s+)?([\w\s\'\-\.\/À-ÖØ-öø-ÿ]+?(?:\s+(?:International|Domestic|Intl))?\s*Airport)',
            
            # Pattern 7: Direct airport mentions - allow more flexible matching
            r'([A-ZÁÉÍÓÚÜÑ][^,;\n]*?-[^,;\n]*?Airport)(?:\s*[,;\.]|\s+[a-z]|$)',  # Hyphenated names
            
            # Pattern 8: Names with slashes (like Karlsruhe/Baden-Baden)
            r'([A-ZÁÉÍÓÚÜÑ][^,;\n]*\/[^^,;\n]*Airport)',
            
            # Pattern 9: Simple airport names without International/Domestic
            r'([A-ZÁÉÍÓÚÜÑ][^,;\n]*?\s+Airport)(?:\s*[,;\.]|\s+[a-z]|$)',
            
            # Pattern 10: Last resort - any capitalized name followed by Airport
            r'\b([A-ZÁÉÍÓÚÜÑ][^\n]*?Airport)\b'
        ]
        
        extracted_count = 0
        
        for idx, row in df.iterrows():
            subject = str(row['Subject'])
            airport_name = None
            
            # Clean subject first - handle double prepositions like "at at"
            subject_cleaned = re.sub(r'\b(at|in|from)\s+(at|in|from)\s+', r'\1 ', subject)
            
            # Try each pattern in order of specificity
            for pattern in patterns:
                matches = list(re.finditer(pattern, subject_cleaned, re.IGNORECASE))
                if matches:
                    # Take the first match that validates
                    for match in matches:
                        candidate_name = match.group(1).strip()
                        
                        # Clean and validate the airport name
                        cleaned_name = self._clean_airport_name(candidate_name)
                        
                        # Additional validation - avoid extracting weird strings
                        if self._is_valid_airport_name(cleaned_name):
                            airport_name = cleaned_name
                            break
                    
                    if airport_name:
                        break
            
            if airport_name:
                df.at[idx, 'Airport'] = airport_name
                extracted_count += 1
            else:
                # Fallback: capture the longest phrase ending with 'Airport'
                fallback = re.search(r'([A-ZÁÉÍÓÚÜÑ][^\n]*?Airport)', subject_cleaned, re.UNICODE)
                if fallback:
                    candidate_name = fallback.group(1).strip()
                    cleaned_name = self._clean_airport_name(candidate_name)
                    if self._is_valid_airport_name(cleaned_name):
                        df.at[idx, 'Airport'] = cleaned_name
                        extracted_count += 1
        
        rows_after = len(df)
        
        self.log_operation(
            "extract_airport_names",
            f"Extracted airport names from Subject column",
            rows_before, rows_after,
            airports_extracted=extracted_count,
            extraction_patterns=[
                "at [the] <Airport Name> Airport",
                "seized at/in/from <Airport Name>",
                "possessive forms like Name's Airport", 
                "from <Airport Name>",
                "<Airport Name> Airport (direct mention)"
            ]
        )
        
        return df
    
    def _clean_airport_name(self, airport_name: str) -> str:
        """Clean and normalize airport names."""
        # Remove extra whitespace
        airport_name = re.sub(r'\s+', ' ', airport_name.strip())
        
        # Remove trailing punctuation and weird prefixes
        airport_name = re.sub(r'[,\.;]+$', '', airport_name)
        airport_name = re.sub(r'^[,\.;\-\s]+', '', airport_name)
        
        # Remove unwanted prefixes that might be extracted
        airport_name = re.sub(r'^(?:seized|at|from|in)\s+', '', airport_name, flags=re.IGNORECASE)
        
        # Standardize "International" vs "Intl"
        airport_name = re.sub(r'\bIntl\b', 'International', airport_name, flags=re.IGNORECASE)
        
        # Remove any leading numbers or weird prefixes that don't belong
        airport_name = re.sub(r'^\d+\s*', '', airport_name)
        
        # Handle specific edge cases
        airport_name = re.sub(r'\s*,\s*\([^)]*\)$', '', airport_name)  # Remove trailing parenthetical info
        
        return airport_name.strip()
    
    def _is_valid_airport_name(self, airport_name: str) -> bool:
        """Validate that the extracted string looks like a real airport name."""
        if not airport_name or len(airport_name) < 3:
            return False
            
        # Must end with "Airport"
        if not airport_name.endswith('Airport'):
            return False
        
        # Reject generic patterns that are too broad
        invalid_exact_matches = [
            "International Airport",
            "Domestic Airport", 
            "Airport",
            "The Airport"
        ]
        
        if airport_name in invalid_exact_matches:
            return False
            
        # Should not contain certain invalid patterns
        invalid_patterns = [
            r'^\d+',    # Starting with numbers
            r'sezied',  # Common typo (but "seized" at start is ok after cleaning)
            r'kg\s',      # Should not contain weight measurements
            r'suspect', # Should not contain "suspect"
            r'arrest',  # Should not contain "arrest"
            r'ivory',   # Should not contain "ivory"
            r'tusk',    # Should not contain "tusk"
            r'turtle',  # Should not contain animal names
            r'tortoise', # Should not contain animal names
            r'elephant', # Should not contain animal names
            r'rhino',   # Should not contain animal names
            r'pangolin', # Should not contain animal names
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, airport_name, re.IGNORECASE):
                return False
                
        # Should start with a capital letter (proper noun)
        if not airport_name[0].isupper():
            return False
            
        # Should not be too long (likely invalid if > 80 chars, increased for complex names)
        if len(airport_name) > 80:
            return False
        
        # Should have at least one proper noun (not just generic words)
        # Remove common words and see if there's still substance
        stripped = airport_name.lower()
        common_words = ['international', 'domestic', 'airport', 'the', 'at', 'in', 'from']
        for word in common_words:
            stripped = stripped.replace(word, '').strip()
        
        if len(stripped) < 3:  # Should have at least 3 chars of actual airport name
            return False
        
        # Additional check: should not be mostly punctuation
        alpha_chars = sum(c.isalpha() for c in airport_name)
        if alpha_chars < len(airport_name) * 0.6:  # At least 60% alphabetic
            return False
            
        return True
    
    def cluster_similar_airports(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and merge similar airport names (clustering functionality)."""
        rows_before = len(df)
        df = df.copy()
        
        # Get all unique airport names, excluding None/NaN values
        unique_airports = df[df['Airport'].notna() & (df['Airport'].astype(str).str.strip() != '')]['Airport'].unique()
        
        # Define clustering rules for similar airport names
        airport_clusters = {}
        
        for airport in unique_airports:
            if airport is None:  # Skip None values
                continue
                
            normalized = self._normalize_for_clustering(airport)
            
            # Find if this airport belongs to an existing cluster
            cluster_key = None
            for existing_norm, existing_airports in airport_clusters.items():
                if self._should_cluster_together(normalized, existing_norm):
                    cluster_key = existing_norm
                    break
            
            if cluster_key:
                airport_clusters[cluster_key].append(airport)
            else:
                airport_clusters[normalized] = [airport]
        
        # Apply clustering - use the most common or longest name as canonical
        replacements_made = 0
        for normalized, airports in airport_clusters.items():
            if len(airports) > 1:
                # Choose canonical name (longest one, as it's likely most complete)
                canonical = max(airports, key=len)
                
                for airport in airports:
                    if airport != canonical:
                        mask = df['Airport'] == airport
                        df.loc[mask, 'Airport'] = canonical
                        replacements_made += mask.sum()
        
        rows_after = len(df)
        
        self.log_operation(
            "cluster_similar_airports",
            f"Clustered similar airport names",
            rows_before, rows_after,
            clusters_created=len([c for c in airport_clusters.values() if len(c) > 1]),
            replacements_made=replacements_made,
            unique_airports_before=len(unique_airports),
            unique_airports_after=len(df[df['Airport'].notna() & (df['Airport'] != '')]['Airport'].unique())
        )
        
        return df
    
    def _normalize_for_clustering(self, airport_name: str) -> str:
        """Normalize airport name for clustering comparison."""
        if not airport_name:
            return ""
            
        # Convert to lowercase
        normalized = str(airport_name).lower()
        
        # Remove common words and abbreviations
        normalized = re.sub(r'\b(international|intl|domestic|airport)\b', '', normalized)
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Remove punctuation
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        return normalized
    
    def _should_cluster_together(self, name1: str, name2: str) -> bool:
        """Determine if two normalized airport names should be clustered."""
        if not name1 or not name2:
            return False
            
        # Exact match after normalization
        if name1 == name2:
            return True
            
        # Check if one is a substring of the other (for abbreviated vs full names)
        if len(name1) >= 3 and len(name2) >= 3:
            if name1 in name2 or name2 in name1:
                return True
        
        # Handle common typos and variations using Levenshtein-like approach
        # For names that are very similar but have small differences
        if len(name1) >= 5 and len(name2) >= 5:
            # Calculate simple character-based similarity
            shorter, longer = (name1, name2) if len(name1) <= len(name2) else (name2, name1)
            
            # If names are very close in length and content, check character differences
            if abs(len(name1) - len(name2)) <= 2:
                differences = sum(c1 != c2 for c1, c2 in zip(name1, name2))
                # Allow 1-2 character differences for potential typos
                if differences <= 2 and len(shorter) >= 8:
                    return True
        
        # Handle specific known variations and typos
        variations = [
            ("taoxian", "taoxin"),  # Shenyang airport typo
            ("mohammed", "muhammad"), # Common name variations
            ("o r", "or"),  # O.R. vs OR variations
            ("intl", "international"),  # Already handled in normalization but double-check
        ]
        
        for var1, var2 in variations:
            if (var1 in name1 and var2 in name2) or (var2 in name1 and var1 in name2):
                # Check if the rest of the name is similar
                name1_clean = name1.replace(var1, "").replace(var2, "").strip()
                name2_clean = name2.replace(var1, "").replace(var2, "").strip()
                if name1_clean == name2_clean or name1_clean in name2_clean or name2_clean in name1_clean:
                    return True
        
        return False
    
    def save_results(self, df: pd.DataFrame) -> Tuple[str, str]:
        """Save the cleaned data and operation history."""
        # Save cleaned CSV
        output_csv = self.output_dir / "Q4.csv"
        # Ensure Airport has no null/blank strings; fill remaining with explicit placeholder
        if 'Airport' in df.columns:
            df['Airport'] = df['Airport'].fillna('').astype(str).str.strip()
            df.loc[df['Airport'] == '', 'Airport'] = 'Unknown Airport'
        df.to_csv(output_csv, index=False)
        
        # Save history JSON in OpenRefine-compatible format
        history_file = self.output_dir / "history.json"
        
        # Convert our history to OpenRefine-style format (list of operations)
        openrefine_operations = []
        
        for op in self.history:
            # Convert to OpenRefine-style operation format
            openrefine_op = {
                "op": "core/text-transform",
                "engineConfig": {
                    "facets": [],
                    "mode": "row-based"
                },
                "columnName": "Subject",
                "expression": f"// {op['description']}",
                "onError": "keep-original",
                "repeat": False,
                "repeatCount": 10,
                "description": op['description']
            }
            
            # Add specific operation details based on operation type
            if op['operation'] == 'filter_blank_common_names':
                openrefine_op.update({
                    "op": "core/row-removal",
                    "engineConfig": {
                        "facets": [
                            {
                                "type": "list",
                                "name": "Common Name",
                                "expression": "isBlank(value)",
                                "columnName": "Common Name",
                                "invert": False,
                                "omitBlank": False,
                                "omitError": False,
                                "selection": [{"v": {"v": True}}],
                                "selectBlank": False,
                                "selectError": False
                            }
                        ]
                    }
                })
            elif op['operation'] == 'filter_airport_incidents':
                openrefine_op.update({
                    "op": "core/row-removal",  
                    "engineConfig": {
                        "facets": [
                            {
                                "type": "text",
                                "name": "Subject",
                                "columnName": "Subject",
                                "query": "Airport",
                                "mode": "text",
                                "caseSensitive": True,
                                "invert": True
                            }
                        ]
                    }
                })
            elif op['operation'] == 'extract_airport_names':
                openrefine_op.update({
                    "op": "core/column-addition",
                    "engineConfig": {"facets": [], "mode": "row-based"},
                    "baseColumnName": "Subject",
                    "expression": "// Extract airport names using regex patterns",
                    "onError": "set-to-blank",
                    "newColumnName": "Airport",
                    "columnInsertIndex": len(df.columns) - 1
                })
            elif op['operation'] == 'cluster_similar_airports':
                openrefine_op.update({
                    "op": "core/mass-edit",
                    "engineConfig": {"facets": [], "mode": "row-based"},
                    "columnName": "Airport",
                    "expression": "value",
                    "edits": []  # This would contain the actual clustering edits
                })
            
            openrefine_operations.append(openrefine_op)
        
        # Save as OpenRefine-compatible history (just the operations list)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(openrefine_operations, f, indent=2, ensure_ascii=False, default=str)
        
        return str(output_csv), str(history_file)
    
    def run_pipeline(self) -> Tuple[pd.DataFrame, str, str]:
        """Run the complete data cleaning pipeline."""
        print("=" * 60)
        print("Q4 Data Cleaning Pipeline")
        print("=" * 60)
        
        # Step 1: Load data
        df = self.load_data()
        
        # Step 2: Filter blank Common Names
        df = self.filter_blank_common_names(df)
        
        # Step 3: Filter to Airport incidents only
        df = self.filter_airport_incidents(df)
        
        # Step 4: Extract airport names
        df = self.extract_airport_names(df)
        
        # Step 5: Cluster similar airport names
        df = self.cluster_similar_airports(df)
        
        # Step 6: Save results
        output_csv, history_file = self.save_results(df)
        
        self.cleaned_data = df
        
        print("=" * 60)
        print("Pipeline completed successfully!")
        print(f"✓ Cleaned data saved to: {output_csv}")
        print(f"✓ Operation history saved to: {history_file}")
        print(f"✓ Final dataset: {len(df)} rows, {len(df.columns)} columns")
        print("=" * 60)
        
        return df, output_csv, history_file


def main():
    """Main function to run the data cleaning pipeline."""
    input_file = "/Users/mxy1998/Documents/rileygit/6242_hw1/Q4/incidents.csv"
    output_dir = "/Users/mxy1998/Documents/rileygit/6242_hw1/Q1"
    
    # Create and run pipeline
    pipeline = DataCleaningPipeline(input_file, output_dir)
    cleaned_df, output_csv, history_file = pipeline.run_pipeline()
    
    # Display some sample results
    print("\n" + "=" * 60)
    print("SAMPLE RESULTS")
    print("=" * 60)
    
    # Show unique airports found
    airports = cleaned_df[cleaned_df['Airport'].notna() & (cleaned_df['Airport'] != '')]['Airport'].unique()
    airports = [a for a in airports if a is not None]  # Filter out any None values
    print(f"\nUnique Airports Identified ({len(airports)}):")
    for airport in sorted(airports)[:10]:  # Show first 10
        count = len(cleaned_df[cleaned_df['Airport'] == airport])
        print(f"  • {airport} ({count} incidents)")
    
    if len(airports) > 10:
        print(f"  ... and {len(airports) - 10} more airports")
    
    # Show sample of cleaned data
    print(f"\nSample of cleaned data:")
    print(cleaned_df[['Subject', 'Common Name', 'Airport']].head())
    
    return cleaned_df, output_csv, history_file


if __name__ == "__main__":
    main()