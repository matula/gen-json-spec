#!/usr/bin/env python3
"""
GEDCOM to GEN-JSON Converter
Converts a GEDCOM file to a GEN-JSON formatted file

Usage:
  python gedcom-to-genjson.py input.ged output.json [options]

Options:
  -v, --verbose       Enable verbose output
  --no-validate       Skip validation of the output
  --compact           Output compact JSON (no indentation)
  --pretty            Output pretty-printed JSON (default)
  --indent N          Number of spaces for indentation (default: 2)
  --skip-empty        Skip empty fields in the output
  --encoding          Input file encoding (default: utf-8-sig)

Examples:
  python gedcom-to-genjson.py family.ged family.json
  python gedcom-to-genjson.py family.ged family.json --verbose
  python gedcom-to-genjson.py family.ged family.json --compact
  python gedcom-to-genjson.py family.ged family.json --skip-empty
"""

import json
import sys
import os
import re
import argparse
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Individual:
    """Represents an individual in the genealogy."""
    id: str
    full_name: str = ""
    sex: str = "U"
    birth: Dict[str, str] = field(default_factory=dict)
    death: Dict[str, str] = field(default_factory=dict)
    parents: List[str] = field(default_factory=list)
    spouses: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self, skip_empty: bool = False) -> Dict[str, Any]:
        """Convert to dictionary, optionally skipping empty fields."""
        result = {
            "full_name": self.full_name,
            "sex": self.sex
        }

        if not skip_empty or self.birth:
            result["birth"] = self.birth
        if not skip_empty or self.death:
            result["death"] = self.death
        if not skip_empty or self.parents:
            result["parents"] = self.parents
        if not skip_empty or self.spouses:
            result["spouses"] = self.spouses
        if not skip_empty or self.children:
            result["children"] = self.children
        if not skip_empty or self.sources:
            result["sources"] = self.sources
        if not skip_empty or self.notes:
            result["notes"] = self.notes

        return result


@dataclass
class Family:
    """Represents a family unit in the genealogy."""
    id: str
    husband: str = ""
    wife: str = ""
    marriage: Dict[str, str] = field(default_factory=dict)
    children: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self, skip_empty: bool = False) -> Dict[str, Any]:
        """Convert to dictionary, optionally skipping empty fields."""
        result = {}

        if not skip_empty or self.husband:
            result["husband"] = self.husband
        if not skip_empty or self.wife:
            result["wife"] = self.wife
        if not skip_empty or self.marriage:
            result["marriage"] = self.marriage
        if not skip_empty or self.children:
            result["children"] = self.children
        if not skip_empty or self.notes:
            result["notes"] = self.notes

        return result


class GedcomParser:
    """Parser for GEDCOM files."""

    # Month abbreviations to numbers
    MONTH_MAP = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
        'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
        'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }

    # Date qualifiers to remove
    DATE_QUALIFIERS = ['ABT', 'EST', 'BEF', 'AFT', 'CAL', 'FROM', 'TO', 'BET', 'AND']

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.individuals: Dict[str, Individual] = {}
        self.families: Dict[str, Family] = {}
        self.sources: Dict[str, Dict[str, str]] = {}
        self.media: Dict[str, Dict[str, str]] = {}
        self.notes: Dict[str, str] = {}

    def parse_date(self, date_str: str) -> Optional[str]:
        """
        Parse GEDCOM date format to ISO 8601 format (YYYY-MM-DD).

        Args:
            date_str: GEDCOM date string

        Returns:
            ISO formatted date string or None
        """
        if not date_str:
            return None

        # Remove date qualifiers
        cleaned_date = date_str.strip()
        for qualifier in self.DATE_QUALIFIERS:
            cleaned_date = re.sub(rf'^{qualifier}\s+', '', cleaned_date, flags=re.IGNORECASE)

        # Remove any parenthetical information
        cleaned_date = re.sub(r'\([^)]*\)', '', cleaned_date).strip()

        # Try various date patterns
        patterns = [
            # DD MMM YYYY
            (r'(\d{1,2})\s+([A-Za-z]{3,})\s+(\d{4})', lambda m: f"{m[3]}-{self.MONTH_MAP.get(m[2][:3].upper(), '01')}-{m[1].zfill(2)}"),
            # MMM DD, YYYY
            (r'([A-Za-z]{3,})\s+(\d{1,2}),?\s+(\d{4})', lambda m: f"{m[3]}-{self.MONTH_MAP.get(m[1][:3].upper(), '01')}-{m[2].zfill(2)}"),
            # MMM YYYY
            (r'([A-Za-z]{3,})\s+(\d{4})', lambda m: f"{m[2]}-{self.MONTH_MAP.get(m[1][:3].upper(), '01')}-01"),
            # YYYY-MM-DD (already in ISO format)
            (r'(\d{4})-(\d{2})-(\d{2})', lambda m: f"{m[1]}-{m[2]}-{m[3]}"),
            # DD/MM/YYYY or DD-MM-YYYY
            (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', lambda m: f"{m[3]}-{m[2].zfill(2)}-{m[1].zfill(2)}"),
            # YYYY only
            (r'^(\d{4})$', lambda m: f"{m[1]}-01-01")
        ]

        for pattern, formatter in patterns:
            match = re.search(pattern, cleaned_date)
            if match:
                try:
                    return formatter(match.groups())
                except (KeyError, IndexError):
                    continue

        if self.verbose:
            logger.warning(f"Could not parse date: {date_str}")
        return None

    def parse_line(self, line: str) -> Tuple[int, str, Optional[str], Optional[str]]:
        """
        Parse a GEDCOM line into its components.

        Args:
            line: Raw GEDCOM line

        Returns:
            Tuple of (level, xref_id, tag, value)
        """
        line = line.strip()
        if not line:
            return -1, "", None, None

        parts = line.split(' ', 2)
        if len(parts) < 2:
            return -1, "", None, None

        level = int(parts[0])

        # Check if this is a record with XREF ID (e.g., "0 @I1@ INDI")
        if parts[1].startswith('@') and parts[1].endswith('@'):
            xref_id = parts[1][1:-1]  # Remove @ symbols
            tag = parts[2] if len(parts) > 2 else None
            value = None
        else:
            xref_id = ""
            tag = parts[1]
            value = parts[2] if len(parts) > 2 else ""

        return level, xref_id, tag, value

    def parse_file(self, file_path: str, encoding: str = 'utf-8-sig') -> Dict[str, Any]:
        """
        Parse a GEDCOM file and convert it to GEN-JSON format.

        Args:
            file_path: Path to the GEDCOM file
            encoding: File encoding (default: utf-8-sig to handle BOM)

        Returns:
            Dictionary containing the GEN-JSON data
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                self._parse_lines(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    self._parse_lines(f)
            except Exception as e:
                raise Exception(f"Error reading file with encoding issues: {e}")

        # Post-process relationships
        self._process_relationships()

        return self._build_output()

    def _parse_lines(self, file_handle):
        """Parse lines from the file handle."""
        current_record = None
        current_record_type = None
        current_event = None
        current_note_id = None

        for line_num, line in enumerate(file_handle, 1):
            try:
                level, xref_id, tag, value = self.parse_line(line)

                if level == -1:
                    continue

                # Handle level 0 records
                if level == 0:
                    current_event = None

                    if xref_id:
                        if tag == 'INDI':
                            current_record = Individual(id=xref_id)
                            current_record_type = 'INDI'
                            self.individuals[xref_id] = current_record
                        elif tag == 'FAM':
                            current_record = Family(id=xref_id)
                            current_record_type = 'FAM'
                            self.families[xref_id] = current_record
                        elif tag == 'SOUR':
                            current_record = {'title': '', 'description': ''}
                            current_record_type = 'SOUR'
                            self.sources[xref_id] = current_record
                        elif tag == 'NOTE':
                            current_note_id = xref_id
                            self.notes[xref_id] = value or ""
                            current_record_type = 'NOTE'
                        else:
                            current_record = None
                            current_record_type = None
                    else:
                        current_record = None
                        current_record_type = None

                # Handle subordinate levels
                elif current_record_type == 'INDI' and isinstance(current_record, Individual):
                    self._parse_individual_tag(level, tag, value, current_record, current_event)
                    if tag in ['BIRT', 'DEAT', 'BAPM', 'CHR', 'BURI']:
                        current_event = tag

                elif current_record_type == 'FAM' and isinstance(current_record, Family):
                    self._parse_family_tag(level, tag, value, current_record, current_event)
                    if tag == 'MARR':
                        current_event = tag

                elif current_record_type == 'SOUR' and isinstance(current_record, dict):
                    if level == 1:
                        if tag == 'TITL':
                            current_record['title'] = value
                        elif tag == 'TEXT':
                            current_record['description'] = value

                elif current_record_type == 'NOTE' and current_note_id:
                    if level == 1 and tag == 'CONT':
                        self.notes[current_note_id] += '\n' + value

            except Exception as e:
                logger.warning(f"Error parsing line {line_num}: {line.strip()} - {e}")

    def _parse_individual_tag(self, level: int, tag: str, value: str, individual: Individual, current_event: Optional[str]):
        """Parse tags for an individual record."""
        if level == 1:
            if tag == 'NAME':
                # Remove slashes used to denote surnames
                individual.full_name = value.replace('/', '').strip()
            elif tag == 'SEX':
                individual.sex = value.strip() if value.strip() in ['M', 'F'] else 'U'
            elif tag == 'FAMS':
                spouse_fam_id = value.strip('@')
                if spouse_fam_id not in individual.spouses:
                    individual.spouses.append(spouse_fam_id)
            elif tag == 'FAMC':
                # This will be processed in relationship processing
                pass
            elif tag == 'NOTE':
                if value.startswith('@'):
                    # Reference to a NOTE record
                    note_id = value.strip('@')
                    if note_id in self.notes:
                        individual.notes.append(self.notes[note_id])
                else:
                    individual.notes.append(value)
            elif tag == 'SOUR':
                if value.startswith('@'):
                    source_id = value.strip('@')
                    individual.sources.append(source_id)

        elif level == 2 and current_event:
            if tag == 'DATE':
                date = self.parse_date(value)
                if date:
                    if current_event == 'BIRT':
                        individual.birth['date'] = date
                    elif current_event == 'DEAT':
                        individual.death['date'] = date
            elif tag == 'PLAC':
                if current_event == 'BIRT':
                    individual.birth['place'] = value
                elif current_event == 'DEAT':
                    individual.death['place'] = value

    def _parse_family_tag(self, level: int, tag: str, value: str, family: Family, current_event: Optional[str]):
        """Parse tags for a family record."""
        if level == 1:
            if tag == 'HUSB':
                family.husband = value.strip('@')
            elif tag == 'WIFE':
                family.wife = value.strip('@')
            elif tag == 'CHIL':
                child_id = value.strip('@')
                if child_id not in family.children:
                    family.children.append(child_id)
            elif tag == 'NOTE':
                if value.startswith('@'):
                    note_id = value.strip('@')
                    if note_id in self.notes:
                        family.notes.append(self.notes[note_id])
                else:
                    family.notes.append(value)

        elif level == 2 and current_event == 'MARR':
            if tag == 'DATE':
                date = self.parse_date(value)
                if date:
                    family.marriage['date'] = date
            elif tag == 'PLAC':
                family.marriage['place'] = value

    def _process_relationships(self):
        """Process family relationships to update individual records."""
        # First, process parent-child relationships
        for family_id, family in self.families.items():
            husband_id = family.husband
            wife_id = family.wife

            # Add children to parents and parents to children
            for child_id in family.children:
                if child_id in self.individuals:
                    child = self.individuals[child_id]

                    # Add parents to child
                    if husband_id and husband_id in self.individuals:
                        if husband_id not in child.parents:
                            child.parents.append(husband_id)
                        # Add child to father
                        if child_id not in self.individuals[husband_id].children:
                            self.individuals[husband_id].children.append(child_id)

                    if wife_id and wife_id in self.individuals:
                        if wife_id not in child.parents:
                            child.parents.append(wife_id)
                        # Add child to mother
                        if child_id not in self.individuals[wife_id].children:
                            self.individuals[wife_id].children.append(child_id)

        # Update spouse relationships from family records
        for family_id, family in self.families.items():
            if family.husband and family.wife:
                # Replace family ID with actual spouse ID
                if family.husband in self.individuals:
                    husband = self.individuals[family.husband]
                    # Remove family ID and add spouse ID
                    if family_id in husband.spouses:
                        husband.spouses.remove(family_id)
                    if family.wife and family.wife not in husband.spouses:
                        husband.spouses.append(family.wife)

                if family.wife in self.individuals:
                    wife = self.individuals[family.wife]
                    # Remove family ID and add spouse ID
                    if family_id in wife.spouses:
                        wife.spouses.remove(family_id)
                    if family.husband and family.husband not in wife.spouses:
                        wife.spouses.append(family.husband)

    def _build_output(self) -> Dict[str, Any]:
        """Build the final GEN-JSON output."""
        output = {
            "version": "1.0",
            "individuals": {},
            "families": {}
        }

        # Convert individuals
        for ind_id, individual in self.individuals.items():
            output["individuals"][ind_id] = individual.to_dict()

        # Convert families
        for fam_id, family in self.families.items():
            output["families"][fam_id] = family.to_dict()

        # Add sources if present
        if self.sources:
            output["sources"] = self.sources

        # Add media if present
        if self.media:
            output["media"] = self.media

        return output


def validate_gen_json(data: Dict[str, Any]) -> List[str]:
    """
    Validate GEN-JSON data against the schema requirements.

    Args:
        data: The GEN-JSON data to validate

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Check required top-level fields
    if "version" not in data:
        errors.append("Missing required field: version")
    if "individuals" not in data:
        errors.append("Missing required field: individuals")

    # Validate individuals
    if "individuals" in data:
        for ind_id, individual in data["individuals"].items():
            if "full_name" not in individual:
                errors.append(f"Individual {ind_id}: missing required field 'full_name'")
            if "sex" not in individual:
                errors.append(f"Individual {ind_id}: missing required field 'sex'")
            elif individual["sex"] not in ["M", "F", "U"]:
                errors.append(f"Individual {ind_id}: invalid sex value '{individual['sex']}'")

            # Validate dates if present
            for event in ["birth", "death"]:
                if event in individual and "date" in individual[event]:
                    date_str = individual[event]["date"]
                    try:
                        datetime.strptime(date_str, "%Y-%m-%d")
                    except ValueError:
                        errors.append(f"Individual {ind_id}: invalid {event} date format '{date_str}'")

    # Validate relationships
    all_individual_ids = set(data.get("individuals", {}).keys())

    for ind_id, individual in data.get("individuals", {}).items():
        # Check parent references
        for parent_id in individual.get("parents", []):
            if parent_id not in all_individual_ids:
                errors.append(f"Individual {ind_id}: parent '{parent_id}' not found")

        # Check spouse references
        for spouse_id in individual.get("spouses", []):
            if spouse_id not in all_individual_ids:
                errors.append(f"Individual {ind_id}: spouse '{spouse_id}' not found")

        # Check children references
        for child_id in individual.get("children", []):
            if child_id not in all_individual_ids:
                errors.append(f"Individual {ind_id}: child '{child_id}' not found")

    return errors


def main():
    """Main function to run the converter."""
    parser = argparse.ArgumentParser(
        description='Convert GEDCOM files to GEN-JSON format.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('input_file', help='Path to the input GEDCOM file')
    parser.add_argument('output_file', help='Path to the output GEN-JSON file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--no-validate', action='store_true', help='Skip validation of the output')
    parser.add_argument('--compact', action='store_true', help='Output compact JSON (no indentation)')
    parser.add_argument('--indent', type=int, default=2, help='Number of spaces for indentation (default: 2)')
    parser.add_argument('--skip-empty', action='store_true', help='Skip empty fields in the output')
    parser.add_argument('--encoding', default='utf-8-sig', help='Input file encoding (default: utf-8-sig)')

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    # Check input file exists
    if not os.path.exists(args.input_file):
        logger.error(f"Input file '{args.input_file}' not found.")
        sys.exit(1)

    try:
        # Parse GEDCOM file
        logger.info(f"Parsing GEDCOM file: {args.input_file}")
        parser_instance = GedcomParser(verbose=args.verbose)
        gen_json_data = parser_instance.parse_file(args.input_file, encoding=args.encoding)

        # Apply skip-empty if requested
        if args.skip_empty:
            # Rebuild with skip_empty flag
            for ind_id, individual in parser_instance.individuals.items():
                gen_json_data["individuals"][ind_id] = individual.to_dict(skip_empty=True)
            for fam_id, family in parser_instance.families.items():
                gen_json_data["families"][fam_id] = family.to_dict(skip_empty=True)

            # Remove empty top-level sections
            if not gen_json_data.get("families"):
                gen_json_data.pop("families", None)
            if not gen_json_data.get("sources"):
                gen_json_data.pop("sources", None)
            if not gen_json_data.get("media"):
                gen_json_data.pop("media", None)

        # Validate output
        if not args.no_validate:
            logger.info("Validating output...")
            validation_errors = validate_gen_json(gen_json_data)

            if validation_errors:
                logger.warning("Validation errors found:")
                for error in validation_errors:
                    logger.warning(f"  - {error}")
            else:
                logger.info("Validation passed!")

        # Write output
        indent = None if args.compact else args.indent

        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(gen_json_data, f, indent=indent, ensure_ascii=False)

        # Print summary
        print(f"\n✓ Conversion complete! Saved to {args.output_file}")

        stats = []
        stats.append(f"{len(gen_json_data.get('individuals', {}))} individuals")
        stats.append(f"{len(gen_json_data.get('families', {}))} families")

        if 'sources' in gen_json_data:
            stats.append(f"{len(gen_json_data['sources'])} sources")
        if 'media' in gen_json_data:
            stats.append(f"{len(gen_json_data['media'])} media items")

        print(f"  Converted: {', '.join(stats)}")

        # Show sample if verbose
        if args.verbose and gen_json_data.get('individuals'):
            print("\nSample individual:")
            first_id = next(iter(gen_json_data['individuals']))
            print(json.dumps({first_id: gen_json_data['individuals'][first_id]}, indent=2))

    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
