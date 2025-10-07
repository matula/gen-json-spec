# GEN-JSON: A Modern Genealogy Data Format

## 🌳 Overview
**GEN-JSON** (Genealogy JSON) is an open, structured, and human-readable format for storing and sharing genealogical data. It serves as a modern replacement for the GEDCOM format, providing better flexibility, extensibility, and ease of use for genealogy applications, researchers, and AI/LLM systems.

**Current Version: 2.0** - Now optimized for AI and machine learning with structured data, explicit metadata, and comprehensive event support.

## 🔹 Key Features
✅ **Human-Readable & Machine-Friendly** – Uses clear JSON structures for better data handling.
✅ **AI/LLM Optimized** – Structured names, dates, and places for easy parsing and analysis.
✅ **Data Quality Tracking** – Confidence levels and source quality indicators for research accuracy.
✅ **Comprehensive Event Support** – Track all life events: birth, death, marriage, immigration, occupation, and more.
✅ **Flexible & Extensible** – Supports additional fields without breaking compatibility.
✅ **Rich Source Citations** – Detailed metadata for historical records and research materials.
✅ **Hierarchical Places** – Structured location data with coordinates for geocoding.
✅ **Supports Multimedia & Sources** – Includes references to images, documents, and citations.
✅ **Internationalization Support** – Uses **UTF-8** for seamless global character encoding.
✅ **Works with Modern Web & Desktop Apps** – Easily integrates with genealogy applications, APIs, and databases.

## 📂 File Structure

### Version 2.0 Structure (Current)
```json
{
  "version": "2.0",
  "metadata": {},
  "individuals": {},
  "families": {},
  "events": {},
  "sources": {},
  "repositories": {},
  "media": {},
  "places": {},
  "notes": {}
}
```

- **`metadata`** → File-level information (creator, timestamps, change log)
- **`individuals`** → People with structured names, relationships, and confidence levels
- **`families`** → Family units linking partners and children
- **`events`** → All life events (birth, death, marriage, immigration, occupation, etc.)
- **`sources`** → Detailed citations with quality ratings
- **`repositories`** → Archives and institutions holding source materials
- **`media`** → Images, documents, audio, video with metadata
- **`places`** → Hierarchical location data with coordinates
- **`notes`** → Research notes with attribution and conflict tracking

### Version 1.0 Structure (Legacy)
```json
{
  "version": "1.0",
  "individuals": {},
  "families": {},
  "sources": {},
  "media": {}
}
```

v1.0 files are still supported. See [CHANGES-v2.0.md](CHANGES-v2.0.md) for migration guidance.

## 📌 Example GEN-JSON v2.0 File

### Structured Individual with Events
```json
{
  "version": "2.0",
  "individuals": {
    "I1": {
      "name": {
        "given_name": "John",
        "surname": "Doe",
        "suffix": "Jr.",
        "full_name": "John Doe Jr."
      },
      "sex": "M",
      "events": ["E1", "E2", "E3"],
      "confidence_level": "high"
    }
  },
  "events": {
    "E1": {
      "type": "birth",
      "individual_id": "I1",
      "date": {
        "value": "1900-01-01",
        "date_type": "exact"
      },
      "place": {
        "place_id": "P1"
      },
      "confidence_level": "high",
      "sources": ["S1"]
    },
    "E2": {
      "type": "immigration",
      "individual_id": "I1",
      "date": {
        "value": "1920",
        "date_type": "approximate",
        "circa": true
      },
      "details": {
        "ship_name": "SS Bremen",
        "from_location": "Bremen, Germany"
      }
    }
  },
  "places": {
    "P1": {
      "name": "New York, New York, USA",
      "components": {
        "locality": "New York",
        "state": "New York",
        "country": "United States"
      },
      "coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
      }
    }
  }
}
```

See [examples/example-v2-comprehensive.json](examples/example-v2-comprehensive.json) for a complete example with all v2.0 features.

## 🛠 How to Use GEN-JSON

### ✅ **Loading & Parsing**
- Load a GEN-JSON file into any **JSON-compatible** system.
- Use **JavaScript (Node.js, Deno)**, **Python (json module)**, or any other language that supports JSON.

### ✅ **Validating a GEN-JSON File**
Run a JSON Schema validator (supports both v1.0 and v2.0):
```sh
npm install ajv-cli -g
ajv validate -s schemas/gen-json-schema.json -d my-family-tree.json
```

Or use the included Node.js validator:
```sh
node tools/gen-json-validator.js examples/example-v2-comprehensive.json
```

### ✅ **Converting from GEDCOM to GEN-JSON**
A Python script (in `tools/gedcom-to-genjson.py`) converts GEDCOM files to GEN-JSON v1.0:
```sh
python tools/gedcom-to-genjson.py input.ged output.json
```

Options:
- `--verbose` - Enable detailed logging
- `--compact` - Output minified JSON
- `--skip-empty` - Omit empty fields

**Note:** The converter currently outputs v1.0 format. See [CHANGES-v2.0.md](CHANGES-v2.0.md) for upgrading to v2.0.

## 🤖 AI/LLM Integration

GEN-JSON v2.0 is optimized for AI and machine learning applications:

- **Structured Data** - Names, places, and dates are pre-parsed for direct field access
- **Explicit Uncertainty** - Date types and confidence levels enable probabilistic reasoning
- **Event-Centric** - Unlimited event types support rich timeline analysis
- **Data Quality** - Confidence and quality indicators help weigh conflicting information
- **Graph-Ready** - Clean ID references perfect for knowledge graphs and relationship analysis

Example AI query:
```javascript
// "When did John immigrate to America?"
const immigrationEvents = events.filter(e =>
  e.type === "immigration" && e.individual_id === "I1"
);
// Returns: {date: {value: "1920", date_type: "approximate"}, confidence_level: "high"}
```

## 🆕 What's New in v2.0

- ✨ **Structured Names** - Separate fields for given name, surname, suffix, nickname
- ✨ **Enhanced Dates** - Date type (exact/approximate/before/after) with original format preserved
- ✨ **Hierarchical Places** - Structured locations with coordinates for geocoding
- ✨ **Centralized Events** - Unlimited event types (immigration, occupation, census, military, etc.)
- ✨ **Data Quality Tracking** - Confidence levels and source quality ratings
- ✨ **Typed Relationships** - Distinguish biological/adoptive/step/foster relationships
- ✨ **Rich Sources** - Detailed citation metadata with quality assessment
- ✨ **Repositories** - Track archives and institutions
- ✨ **Research Notes** - Structured notes with conflict tracking
- ✨ **File Metadata** - Provenance tracking with change logs

See [CHANGES-v2.0.md](CHANGES-v2.0.md) for detailed comparison with v1.0.

## 📖 Documentation
- **[Specification (v2.0)](SPECIFICATION.md)** → Complete format specification with AI/LLM focus
- **[Changes in v2.0](CHANGES-v2.0.md)** → Detailed comparison and migration guide
- **[Examples](examples/)** → Sample files for v1.0 and v2.0
  - [example1.json](examples/example1.json) - Simple v1.0 example
  - [example-v2-comprehensive.json](examples/example-v2-comprehensive.json) - Full v2.0 demonstration
- **[Integration Guide](docs/integration.md)** → How to use GEN-JSON with genealogy software

## 📜 License
GEN-JSON is released under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🌎 Community & Support
📢 Discussions: [GitHub Issues](https://github.com/matula/gen-json-spec/issues)  
📖 Wiki: [GEN-JSON Wiki](https://github.com/matula/gen-json-spec/wiki)

---
🚀 **Start using GEN-JSON today to preserve and share your family history!**
