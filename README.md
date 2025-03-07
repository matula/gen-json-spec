# GEN-JSON: A Modern Genealogy Data Format

## 🌳 Overview
**GEN-JSON** (Genealogy JSON) is an open, structured, and human-readable format for storing and sharing genealogical data. It serves as a modern replacement for the GEDCOM format, providing better flexibility, extensibility, and ease of use for genealogy applications and researchers and Large Language Model (AI).

## 🔹 Key Features
✅ **Human-Readable & Machine-Friendly** – Uses clear JSON structures for better data handling.  
✅ **Flexible & Extensible** – Supports additional fields without breaking compatibility.  
✅ **Supports Multimedia & Sources** – Includes references to images, documents, and citations.  
✅ **Internationalization Support** – Uses **UTF-8** for seamless global character encoding.  
✅ **Works with Modern Web & Desktop Apps** – Easily integrates with genealogy applications, APIs, and databases.

## 📂 File Structure
GEN-JSON files are structured hierarchically with the following sections:

```json
{
  "version": "1.0",
  "individuals": { ... },
  "families": { ... },
  "sources": { ... },
  "media": { ... }
}
```

- **`individuals`** → Stores all people and their relationships.
- **`families`** → Links parents, spouses, and children.
- **`sources`** → Tracks citations for historical records.
- **`media`** → Stores references to images and documents.

## 📌 Example GEN-JSON File
```json
{
  "version": "1.0",
  "individuals": {
    "I1": {
      "full_name": "John Doe",
      "sex": "M",
      "birth": {
        "date": "1900-01-01",
        "place": "New York, USA",
        "sources": ["S1"]
      },
      "death": {
        "date": "1985-03-15",
        "place": "Los Angeles, USA",
        "sources": ["S2"]
      },
      "parents": ["I3", "I4"],
      "spouses": ["I2"],
      "children": ["I5"]
    }
  }
}
```

## 🛠 How to Use GEN-JSON
### ✅ **Loading & Parsing**
- Load a GEN-JSON file into any **JSON-compatible** system.
- Use **JavaScript (Node.js, Deno)**, **Python (json module)**, or any other language that supports JSON.

### ✅ **Validating a GEN-JSON File**
Run a JSON Schema validator:
```sh
npm install ajv-cli -g
ajv validate -s schemas/gen-json-schema.json -d my-family-tree.json
```

### ✅ **Converting from GEDCOM to GEN-JSON**
A Python script (in `tools/gedcom-to-genjson.py`) helps convert old GEDCOM files:
```sh
python tools/gedcom-to-genjson.py input.ged output.json
```

## 📖 Documentation
- **[Specification](SPECIFICATION.md)** → Full breakdown of the GEN-JSON format.
- **[Examples](examples/)** → Real-world family tree files.
- **[Integration Guide](docs/integration.md)** → How to use GEN-JSON with genealogy software.

## 📜 License
GEN-JSON is released under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🌎 Community & Support
📧 Email: support@example.com  
📢 Discussions: [GitHub Issues](https://github.com/matula/gen-json-spec/issues)  
📖 Wiki: [GEN-JSON Wiki](https://github.com/matula/gen-json-spec/wiki)

---
🚀 **Start using GEN-JSON today to preserve and share your family history!**
