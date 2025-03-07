# GEDCOM to GEN-JSON Converter
# Converts a GEDCOM file to a GEN-JSON formatted file

import json
import sys

def parse_gedcom(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    individuals = {}
    families = {}
    current_id = None

    for line in lines:
        parts = line.strip().split(' ', 2)
        if len(parts) < 3:
            continue
        level, tag, value = parts

        if tag == 'INDI':
            current_id = value.strip('@')
            individuals[current_id] = {"full_name": "", "sex": "", "birth": {}, "death": {}, "parents": [], "spouses": [], "children": []}
        elif tag == 'NAME' and current_id:
            individuals[current_id]['full_name'] = value.replace('/', '').strip()
        elif tag == 'SEX' and current_id:
            individuals[current_id]['sex'] = value.strip()

    gen_json = {
        "version": "1.0",
        "individuals": individuals,
        "families": families,
        "sources": {},
        "media": {}
    }

    return gen_json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python gedcom-to-genjson.py input.ged output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    gen_json_data = parse_gedcom(input_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gen_json_data, f, indent=2)

    print(f"Conversion complete! Saved to {output_file}")