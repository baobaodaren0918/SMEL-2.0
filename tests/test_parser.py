"""
SMEL Parser Test Script
Tests parsing of SMEL migration scripts using the parser factory.
Supports both SMEL_Specific (.smel) and SMEL_Pauschalisiert (.smel_ps) grammars.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser_factory import parse_smel_auto, get_grammar_info


def parse_smel_file(filepath: str, verbose: bool = True) -> tuple:
    """
    Parse a SMEL file and return success status and any errors.

    Args:
        filepath: Path to the .smel or .smel_ps file
        verbose: Whether to print detailed information

    Returns:
        Tuple of (success: bool, context, operations, errors: list[str])
    """
    print(f"\n{'='*60}")
    print(f"Parsing: {filepath}")
    print('='*60)

    # Get grammar info
    try:
        grammar_info = get_grammar_info(filepath)
        if verbose:
            print(f"\nGrammar: {grammar_info['type']}")
            print(f"Extension: {grammar_info['file_extension']}")
            print(f"Lexer: {grammar_info['lexer']}")
            print(f"Parser: {grammar_info['parser']}")
    except Exception as e:
        print(f"[ERROR] Failed to detect grammar: {e}")
        return False, None, None, [str(e)]

    # Parse file
    try:
        context, operations, errors = parse_smel_auto(filepath)

        # Check for errors
        if errors:
            print("\n[FAILED] Syntax errors found:")
            for error in errors:
                print(f"  - {error}")
            return False, context, operations, errors

        print("\n[SUCCESS] No syntax errors")

        if verbose:
            # Print migration context
            print("\n--- Migration Context ---")
            print(f"Name: {context.name}:{context.version}")
            print(f"Direction: {context.source_db_type} -> {context.target_db_type}")

            # Print operations
            print(f"\n--- Parsed Operations ({len(operations)} total) ---")
            for i, op in enumerate(operations, 1):
                print(f"{i}. {op.op_type}")
                if op.original_keyword and op.original_keyword != op.op_type:
                    print(f"   (Original keyword: {op.original_keyword})")
                if op.params:
                    for key, value in op.params.items():
                        if isinstance(value, list):
                            print(f"   - {key}: {value}")
                        elif isinstance(value, dict):
                            print(f"   - {key}:")
                            for k, v in value.items():
                                print(f"     • {k}: {v}")
                        else:
                            print(f"   - {key}: {value}")

        return True, context, operations, []

    except Exception as e:
        print(f"\n[ERROR] Parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None, [str(e)]


def count_operations(operations: list) -> dict:
    """Count different operation types."""
    counts = {}
    for op in operations:
        op_type = op.op_type
        counts[op_type] = counts.get(op_type, 0) + 1
    return counts


def main():
    """Main test function."""
    # Get test files directory
    tests_dir = Path(__file__).parent

    # Test files - scan for .smel and .smel_ps files
    test_files = []
    test_files.extend(tests_dir.glob("**/*.smel"))
    test_files.extend(tests_dir.glob("**/*.smel_ps"))

    if not test_files:
        print("No test files found in tests directory")
        print(f"Searched in: {tests_dir}")
        return 1

    results = []

    for filepath in sorted(test_files):
        success, context, operations, errors = parse_smel_file(str(filepath), verbose=True)
        results.append((filepath.name, success, errors))

        if success and operations:
            counts = count_operations(operations)
            print("\n--- Operation Counts ---")
            for op, count in sorted(counts.items()):
                print(f"  {op}: {count}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    all_passed = True
    for name, success, errors in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {name}")
        if not success:
            all_passed = False

    print("="*60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
