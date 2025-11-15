#!/usr/bin/env python3
"""Test script that mimics Gradescope's import test"""

import sys
import traceback

print("Python version:", sys.version)
print("Attempting to import from submission.py...")
print("-" * 60)

try:
    from submission import PageRank, author, gtid
    print("✓ Import successful!")
    print(f"  - PageRank: {PageRank}")
    print(f"  - author(): {author()}")
    print(f"  - gtid(): {gtid()}")
    
    # Test instantiation
    print("\nTesting PageRank instantiation...")
    pr = PageRank("network.tsv")
    print(f"✓ PageRank instance created: {pr}")
    print(f"  - node_degree: {type(pr.node_degree)}")
    print(f"  - max_node_id: {pr.max_node_id}")
    
except ImportError as e:
    print(f"✗ ImportError: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
