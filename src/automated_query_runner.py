"""
Automated query runner for Phase 4 performance analysis.
Executes all queries from queries.txt and collects statistics.
"""

import argparse
import time
import sys
import os


def run_queries_from_file(node, query_file, delay=2.0):
    """
    Execute all queries from a file.
    
    Args:
        node: Node instance to run queries on
        query_file (str): Path to file containing queries (one per line)
        delay (float): Seconds to wait between queries
    """
    print(f"\n{'='*60}")
    print(f"AUTOMATED QUERY EXECUTION")
    print(f"{'='*60}")
    print(f"Query file: {query_file}")
    print(f"Delay between queries: {delay}s")
    print(f"{'='*60}\n")
    
    try:
        with open(query_file, 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
        
        total_queries = len(queries)
        print(f"Loaded {total_queries} queries\n")
        
        results = []
        
        for i, query in enumerate(queries, 1):
            print(f"\n[Query {i}/{total_queries}] Searching for: '{query}'")
            print("-" * 60)
            
            start_time = time.time()
            node.search_file(query)
            
            # Wait for responses
            time.sleep(delay)
            
            elapsed = time.time() - start_time
            results.append({
                'query': query,
                'elapsed': elapsed
            })
            
            print(f"Query completed in {elapsed:.2f}s")
        
        # Print summary
        print(f"\n{'='*60}")
        print("EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total queries executed: {total_queries}")
        print(f"Total time: {sum(r['elapsed'] for r in results):.2f}s")
        print(f"Average time per query: {sum(r['elapsed'] for r in results)/len(results):.2f}s")
        print(f"{'='*60}\n")
        
        return results
        
    except FileNotFoundError:
        print(f"[ERROR] Query file not found: {query_file}")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to execute queries: {e}")
        return []


def main():
    """
    Run automated queries on a node.
    This is designed to be imported and used with an existing node instance.
    """
    print("Automated Query Runner")
    print("=" * 60)
    print("This module should be imported and used with a Node instance.")
    print("\nUsage example:")
    print("  from automated_query_runner import run_queries_from_file")
    print("  node = Node(...)")
    print("  node.start()")
    print("  node.register_with_bootstrap()")
    print("  run_queries_from_file(node, 'queries.txt', delay=2.0)")
    print("=" * 60)


if __name__ == '__main__':
    main()
