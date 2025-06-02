#!/usr/bin/env python3
# GEDCOM to GEN-JSON Converter
# Converts a GEDCOM file to a GEN-JSON formatted file
#
# Usage:
#   python gedcom-to-genjson.py input.ged output.json [options]
#
# Options:
#   -v, --verbose       Enable verbose output
#   --no-validate       Skip validation of the output
#   --compact           Output compact JSON (no indentation)
#   --pretty            Output pretty-printed JSON (default)
#   --indent N          Number of spaces for indentation (default: 2)
#   --skip-empty        Skip empty fields in the output
#
# Examples:
#   python gedcom-to-genjson.py family.ged family.json
#   python gedcom-to-genjson.py family.ged family.json --verbose
#   python gedcom-to-genjson.py family.ged family.json --compact
#   python gedcom-to-genjson.py family.ged family.json --skip-empty
#
# This script parses GEDCOM files and converts them to the GEN-JSON format.
# It handles individuals, families, relationships, events, sources, and media.
# The output is a JSON file that conforms to the GEN-JSON schema.

import json
import sys
import os
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

def parse_gedcom_date(date_str: str) -> Optional[str]:
    """
    Parse GEDCOM date format to ISO 8601 format (YYYY-MM-DD).
    Returns None if the date cannot be parsed.
    """
    if not date_str:
        return None

    # Remove any "ABT", "EST", "BEF", "AFT" prefixes
    date_str = re.sub(r'^(ABT|EST|BEF|AFT)\s+', '', date_str.strip())

    # Try to parse common date formats
    formats = [
        # DD MMM YYYY
        r'(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})',
        # MMM YYYY
        r'([A-Za-z]{3})\s+(\d{4})',
        # YYYY
        r'(\d{4})'
    ]

    month_map = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }

    for fmt in formats:
        match = re.search(fmt, date_str)
        if match:
            groups = match.groups()
            if len(groups) == 3:  # DD MMM YYYY
                day, month, year = groups
                month = month_map.get(month.upper(), '01')
                return f"{year}-{month}-{day.zfill(2)}"
            elif len(groups) == 2:  # MMM YYYY
                month, year = groups
                month = month_map.get(month.upper(), '01')
                return f"{year}-{month}-01"
            elif len(groups) == 1:  # YYYY
                year = groups[0]
                return f"{year}-01-01"

    return None

def parse_gedcom(file_path: str) -> Dict[str, Any]:
    """
    Parse a GEDCOM file and convert it to GEN-JSON format.

    Args:
        file_path: Path to the GEDCOM file

    Returns:
        Dictionary containing the GEN-JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    individuals: Dict[str, Dict[str, Any]] = {}
    families: Dict[str, Dict[str, Any]] = {}
    sources: Dict[str, Dict[str, Any]] = {}
    media: Dict[str, Dict[str, Any]] = {}

    current_id: Optional[str] = None
    current_type: Optional[str] = None  # 'INDI', 'FAM', 'SOUR', etc.
    current_event: Optional[str] = None  # 'BIRT', 'DEAT', 'MARR', etc.

    # First pass: Create all individuals and families
    for line in lines:
        parts = line.strip().split(' ', 2)
        if len(parts) < 2:
            continue

        level = parts[0]
        tag = parts[1]
        value = parts[2] if len(parts) > 2 else ""

        # Handle special case for INDI, FAM, SOUR records
        if level == '0' and value.startswith('@') and value.endswith('@'):
            record_id = value.strip('@')
            record_type = tag

            if record_type == 'INDI':
                current_id = record_id
                current_type = 'INDI'
                individuals[current_id] = {
                    "full_name": "",
                    "sex": "U",  # Default to Unknown
                    "birth": {},
                    "death": {},
                    "parents": [],
                    "spouses": [],
                    "children": [],
                    "sources": [],
                    "notes": []
                }
            elif record_type == 'FAM':
                current_id = record_id
                current_type = 'FAM'
                families[current_id] = {
                    "husband": "",
                    "wife": "",
                    "marriage": {},
                    "children": [],
                    "notes": []
                }
            elif record_type == 'SOUR':
                current_id = record_id
                current_type = 'SOUR'
                sources[current_id] = {
                    "title": "",
                    "description": ""
                }
            else:
                current_id = None
                current_type = None

        # Process individual records
        elif current_type == 'INDI' and current_id:
            if level == '1':
                if tag == 'NAME':
                    individuals[current_id]['full_name'] = value.replace('/', '').strip()
                elif tag == 'SEX':
                    individuals[current_id]['sex'] = value.strip()
                elif tag == 'BIRT':
                    current_event = 'BIRT'
                elif tag == 'DEAT':
                    current_event = 'DEAT'
                elif tag == 'FAMS':
                    spouse_id = value.strip('@')
                    if spouse_id not in individuals[current_id]['spouses']:
                        individuals[current_id]['spouses'].append(spouse_id)
                elif tag == 'FAMC':
                    family_id = value.strip('@')
                    # We'll process parent-child relationships in a second pass
                elif tag == 'NOTE':
                    # Handle notes for individuals
                    if value:
                        individuals[current_id]['notes'].append(value)

            elif level == '2' and current_event:
                if tag == 'DATE':
                    date = parse_gedcom_date(value)
                    if date:
                        if current_event == 'BIRT':
                            individuals[current_id]['birth']['date'] = date
                        elif current_event == 'DEAT':
                            individuals[current_id]['death']['date'] = date
                elif tag == 'PLAC':
                    if current_event == 'BIRT':
                        individuals[current_id]['birth']['place'] = value
                    elif current_event == 'DEAT':
                        individuals[current_id]['death']['place'] = value

        # Process family records
        elif current_type == 'FAM' and current_id:
            if level == '1':
                if tag == 'HUSB':
                    husband_id = value.strip('@')
                    families[current_id]['husband'] = husband_id
                elif tag == 'WIFE':
                    wife_id = value.strip('@')
                    families[current_id]['wife'] = wife_id
                elif tag == 'CHIL':
                    child_id = value.strip('@')
                    if child_id not in families[current_id]['children']:
                        families[current_id]['children'].append(child_id)
                elif tag == 'MARR':
                    current_event = 'MARR'
                elif tag == 'NOTE':
                    # Handle notes for families
                    if value:
                        families[current_id]['notes'].append(value)

            elif level == '2' and current_event == 'MARR':
                if tag == 'DATE':
                    date = parse_gedcom_date(value)
                    if date:
                        families[current_id]['marriage']['date'] = date
                elif tag == 'PLAC':
                    families[current_id]['marriage']['place'] = value

        # Process source records
        elif current_type == 'SOUR' and current_id:
            if level == '1':
                if tag == 'TITL':
                    sources[current_id]['title'] = value
                elif tag == 'TEXT':
                    sources[current_id]['description'] = value

    # Second pass: Process relationships
    for family_id, family in families.items():
        # Add children to parents
        husband_id = family.get('husband')
        wife_id = family.get('wife')

        for child_id in family.get('children', []):
            if child_id in individuals:
                # Add parents to child
                if husband_id and husband_id in individuals:
                    if husband_id not in individuals[child_id]['parents']:
                        individuals[child_id]['parents'].append(husband_id)

                if wife_id and wife_id in individuals:
                    if wife_id not in individuals[child_id]['parents']:
                        individuals[child_id]['parents'].append(wife_id)

                # Add child to parents
                if husband_id and husband_id in individuals:
                    if child_id not in individuals[husband_id]['children']:
                        individuals[husband_id]['children'].append(child_id)

                if wife_id and wife_id in individuals:
                    if child_id not in individuals[wife_id]['children']:
                        individuals[wife_id]['children'].append(child_id)

        # Add spouses to each other
        if husband_id and wife_id:
            if husband_id in individuals and wife_id in individuals:
                if wife_id not in individuals[husband_id]['spouses']:
                    individuals[husband_id]['spouses'].append(wife_id)
                if husband_id not in individuals[wife_id]['spouses']:
                    individuals[wife_id]['spouses'].append(husband_id)

    # Clean up empty objects
    for individual_id, individual in individuals.items():
        if not individual['birth']:
            individual['birth'] = {}
        if not individual['death']:
            individual['death'] = {}

    gen_json = {
        "version": "1.0",
        "individuals": individuals,
        "families": families
    }

    # Only include sources and media if they have entries
    if sources:
        gen_json["sources"] = sources
    if media:
        gen_json["media"] = media

    return gen_json

def validate_output(gen_json: Dict[str, Any]) -> bool:
    """
    Basic validation of the GEN-JSON output.

    Args:
        gen_json: The GEN-JSON data to validate

    Returns:
        True if valid, False otherwise
    """
    # Check required fields
    if "version" not in gen_json or "individuals" not in gen_json:
        return False

    # Check individuals format
    for individual_id, individual in gen_json["individuals"].items():
        if "full_name" not in individual or "sex" not in individual:
            return False

    return True

def main():
    """Main function to run the converter."""
    parser = argparse.ArgumentParser(description='Convert GEDCOM files to GEN-JSON format.')
    parser.add_argument('input_file', help='Path to the input GEDCOM file')
    parser.add_argument('output_file', help='Path to the output GEN-JSON file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--no-validate', action='store_true', help='Skip validation of the output')
    parser.add_argument('--compact', action='store_true', help='Output compact JSON (no indentation)')
    parser.add_argument('--pretty', action='store_true', help='Output pretty-printed JSON (default)')
    parser.add_argument('--indent', type=int, default=2, help='Number of spaces for indentation (default: 2)')
    parser.add_argument('--skip-empty', action='store_true', help='Skip empty fields in the output')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)

    try:
        if args.verbose:
            print(f"Parsing GEDCOM file: {args.input_file}")

        gen_json_data = parse_gedcom(args.input_file)

        # Remove empty fields if requested
        if args.skip_empty:
            # Clean up individuals
            for individual_id, individual in list(gen_json_data['individuals'].items()):
                if not individual['birth']:
                    del individual['birth']
                if not individual['death']:
                    del individual['death']
                if not individual['parents']:
                    del individual['parents']
                if not individual['spouses']:
                    del individual['spouses']
                if not individual['children']:
                    del individual['children']
                if not individual['sources']:
                    del individual['sources']
                if not individual['notes']:
                    del individual['notes']

            # Clean up families
            if 'families' in gen_json_data:
                for family_id, family in list(gen_json_data['families'].items()):
                    if not family['marriage']:
                        del family['marriage']
                    if not family['children']:
                        del family['children']
                    if not family['notes']:
                        del family['notes']
                    if not family['husband']:
                        del family['husband']
                    if not family['wife']:
                        del family['wife']

        # Validate output
        if not args.no_validate:
            if args.verbose:
                print("Validating output...")

            if not validate_output(gen_json_data):
                print("Warning: Generated GEN-JSON may not be valid.")

        # Determine indentation
        indent = None
        if not args.compact:
            indent = args.indent

        # Write output
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(gen_json_data, f, indent=indent)

        # Print summary
        print(f"Conversion complete! Saved to {args.output_file}")
        stats = [
            f"{len(gen_json_data['individuals'])} individuals",
            f"{len(gen_json_data.get('families', {}))} families"
        ]

        if 'sources' in gen_json_data:
            stats.append(f"{len(gen_json_data['sources'])} sources")

        if 'media' in gen_json_data:
            stats.append(f"{len(gen_json_data['media'])} media items")

        print(f"Converted {', '.join(stats)}.")

        if args.verbose:
            print("\nSample of converted data:")
            # Print a sample of the first individual
            if gen_json_data['individuals']:
                first_id = next(iter(gen_json_data['individuals']))
                print(f"Individual {first_id}:")
                print(json.dumps(gen_json_data['individuals'][first_id], indent=2))

    except Exception as e:
        print(f"Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
