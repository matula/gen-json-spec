# GEN-JSON Specification (v1.0) - Proposal

## Overview

GEN-JSON (Genealogy JSON) is a modern, human-readable, and machine-friendly format designed to store, exchange, and analyze genealogical data efficiently. It would replace the GEDCOM format with a structured, flexible JSON schema that is easy to parse, extend, and integrate with modern web and database applications.

## Key Features

- **Human-Readable & Machine-Processable**: Uses clear key-value pairs instead of cryptic codes.
- **Hierarchical Structure**: Represents individuals, families, events, and sources in a structured format.
- **Flexible & Extensible**: Can be expanded with additional attributes without breaking compatibility.
- **Supports Multimedia & Sources**: Includes references to images, documents, and research citations.
- **Encodes in UTF-8**: Ensures compatibility with international characters and datasets.

## File Structure

GEN-JSON is structured as a JSON object with the following primary sections:

- `version`: Specifies the format version.
- `individuals`: Contains all individuals with their details and relationships.
- `families`: Defines family relationships, including spouses and children.
- `sources`: Stores citation data for historical records and research materials.
- `media`: Links to multimedia objects such as images and documents.

## Schema Definition

### Root Structure

```json
{
  "version": "1.0",
  "individuals": { ... },
  "families": { ... },
  "sources": { ... },
  "media": { ... }
}
```

### Individuals Section

Each individual is stored as an object with a unique ID.

```json
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
    "children": ["I5"],
    "sources": ["S3"]
  }
}
```

### Families Section

Each family defines relationships between individuals.

```json
"families": {
  "F1": {
    "husband": "I1",
    "wife": "I2",
    "marriage": {
      "date": "1925-06-10",
      "place": "New York, USA",
      "sources": ["S4"]
    },
    "children": ["I5"]
  }
}
```

### Sources Section

Historical records and references are stored here.

```json
"sources": {
  "S1": {
    "title": "1900 US Census",
    "url": "https://example.com/record/12345",
    "description": "Birth record of John Doe"
  },
  "S2": {
    "title": "Death Certificate",
    "url": "https://example.com/death/6789",
    "description": "Death record of John Doe"
  },
  "S3": {
    "title": "Family Bible Records",
    "url": "https://example.com/familybible",
    "description": "John Doe's family genealogy records"
  }
}
```

### Media Section

Multimedia objects such as images, audio, or scanned documents.

```json
"media": {
  "M1": {
    "type": "photo",
    "url": "https://example.com/photo1.jpg",
    "description": "Wedding photo of John and Jane Doe",
    "sources": ["S3"]
  }
}
```

## Integrating Sources into Individuals & Events

Each individual, event, or record can have a `sources` key that stores an array of source IDs linking to the `sources` section. This enables easy citation tracking and referencing.

## Comparison with GEDCOM

| Feature                  | GEN-JSON     | GEDCOM 5.5.1 |
| ------------------------ | ------------ | ------------ |
| **Readability**          | ✅ High       | ❌ Low        |
| **Flexibility**          | ✅ Extensible | ❌ Rigid      |
| **Multimedia Support**   | ✅ Yes        | ❌ Limited    |
| **Internationalization** | ✅ UTF-8      | ❌ ANSEL      |
| **Modern Compatibility** | ✅ JSON-based | ❌ Text-based |

## Future Enhancements

- **Graph Database Compatibility**: Integration with Neo4j for advanced relationship analysis.
- **Blockchain for Record Validation**: Ensuring data integrity.
- **AI-Assisted Genealogy Matching**: Auto-suggesting relatives using AI pattern recognition.

## Implementation Considerations

- JSON should be stored using **UTF-8 encoding**.
- Unique identifiers (e.g., `I1`, `F1`, `S1`) should be used consistently.
- Dates should follow the **ISO 8601 format (**``**)**.

## Conclusion

GEN-JSON is a modern genealogy data format designed for clarity, usability, and interoperability. It simplifies data sharing and improves compatibility with modern genealogy software and databases.

