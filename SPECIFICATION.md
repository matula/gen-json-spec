# GEN-JSON Specification (v2.0) - Proposal

## Overview

GEN-JSON (Genealogy JSON) is a modern, human-readable, and machine-friendly format designed to store, exchange, and analyze genealogical data efficiently. It would replace the GEDCOM format with a structured, flexible JSON schema that is easy to parse, extend, and integrate with modern web, database, and AI/LLM applications.

**Version 2.0 Focus**: Enhanced for AI and machine learning with structured data, explicit metadata, data quality indicators, and comprehensive event support.

## Key Features

- **Human-Readable & Machine-Processable**: Uses clear key-value pairs instead of cryptic codes.
- **AI/LLM Optimized**: Structured names, places, dates, and events for easy extraction and analysis.
- **Data Quality Tracking**: Confidence levels, verification status, and source quality indicators.
- **Hierarchical Structure**: Represents individuals, families, events, and sources in a structured format.
- **Comprehensive Event Support**: Generic event system supporting all life events (birth, death, marriage, baptism, immigration, occupation, etc.).
- **Rich Metadata**: File provenance, creation info, and modification history.
- **Flexible & Extensible**: Can be expanded with additional attributes without breaking compatibility.
- **Supports Multimedia & Sources**: Includes references to images, documents, and research citations.
- **Encodes in UTF-8**: Ensures compatibility with international characters and datasets.

## File Structure

GEN-JSON is structured as a JSON object with the following primary sections:

- `version`: Specifies the format version.
- `metadata`: File-level information (creator, creation date, software, modification history).
- `individuals`: Contains all individuals with their details and relationships.
- `families`: Defines family relationships, including spouses and children.
- `events`: Stores all life events (birth, death, marriage, baptism, immigration, etc.).
- `sources`: Stores citation data for historical records and research materials.
- `repositories`: Archives, libraries, and institutions holding source materials.
- `media`: Links to multimedia objects such as images and documents.
- `places`: Structured location data with hierarchical information.
- `notes`: Annotations and research notes with attribution.

## Schema Definition

### Root Structure

```json
{
  "version": "2.0",
  "metadata": { ... },
  "individuals": { ... },
  "families": { ... },
  "events": { ... },
  "sources": { ... },
  "repositories": { ... },
  "media": { ... },
  "places": { ... },
  "notes": { ... }
}
```

### Metadata Section

File-level metadata for tracking provenance and changes.

```json
"metadata": {
  "created": "2025-01-15T10:30:00Z",
  "modified": "2025-01-20T14:45:00Z",
  "creator": {
    "name": "John Researcher",
    "email": "john@example.com",
    "software": "GEN-JSON Editor v2.0"
  },
  "description": "Smith Family Tree - New York Branch",
  "language": "en-US",
  "copyright": "CC-BY-4.0",
  "change_log": [
    {
      "date": "2025-01-20T14:45:00Z",
      "author": "John Researcher",
      "description": "Added immigration records for I1"
    }
  ]
}
```

### Individuals Section

Each individual is stored as an object with a unique ID. **Version 2.0** introduces structured names, enhanced gender representation, and direct event references.

```json
"individuals": {
  "I1": {
    "name": {
      "given_name": "John",
      "surname": "Doe",
      "suffix": "Jr.",
      "nickname": "Johnny",
      "name_type": "legal",
      "full_name": "John Doe Jr."
    },
    "alternate_names": [
      {
        "given_name": "Johann",
        "surname": "Doe",
        "name_type": "birth",
        "full_name": "Johann Doe"
      }
    ],
    "sex": "M",
    "gender": {
      "identity": "male",
      "note": "Identified as male throughout life"
    },
    "events": ["E1", "E2", "E10"],
    "parents": [
      {
        "individual_id": "I3",
        "relationship_type": "biological",
        "parent_type": "father"
      },
      {
        "individual_id": "I4",
        "relationship_type": "biological",
        "parent_type": "mother"
      }
    ],
    "spouses": [
      {
        "individual_id": "I2",
        "family_id": "F1"
      }
    ],
    "children": [
      {
        "individual_id": "I5",
        "relationship_type": "biological"
      }
    ],
    "confidence_level": "high",
    "sources": ["S3"],
    "notes": ["N1"]
  }
}
```

**New Fields Explained:**
- `name`: Structured object with separate fields for parsing
- `alternate_names`: Array for maiden names, aka names, birth names
- `gender`: Separate from biological sex for historical accuracy
- `events`: References to event IDs instead of inline birth/death
- `parents/children`: Include relationship type (biological/adoptive/step/foster)
- `confidence_level`: Data quality indicator (high/medium/low/unknown)

### Events Section

**New in v2.0:** Centralized event storage for all life events. This eliminates redundancy and supports unlimited event types.

```json
"events": {
  "E1": {
    "type": "birth",
    "individual_id": "I1",
    "date": {
      "value": "1900-01-01",
      "date_type": "exact",
      "original": "1 JAN 1900"
    },
    "place": {
      "place_id": "P1",
      "original": "New York, USA"
    },
    "confidence_level": "high",
    "sources": ["S1"],
    "notes": ["N2"]
  },
  "E2": {
    "type": "death",
    "individual_id": "I1",
    "date": {
      "value": "1985-03-15",
      "date_type": "exact"
    },
    "place": {
      "place_id": "P2",
      "original": "Los Angeles, USA"
    },
    "sources": ["S2"]
  },
  "E3": {
    "type": "marriage",
    "family_id": "F1",
    "participants": ["I1", "I2"],
    "date": {
      "value": "1925-06-10",
      "date_type": "exact"
    },
    "place": {
      "place_id": "P1"
    },
    "sources": ["S4"]
  },
  "E4": {
    "type": "immigration",
    "individual_id": "I1",
    "date": {
      "value": "1920",
      "date_type": "approximate",
      "circa": true
    },
    "place": {
      "original": "Ellis Island, New York, USA"
    },
    "details": {
      "arrival_port": "New York Harbor",
      "ship_name": "SS Bremen",
      "from_location": "Bremen, Germany"
    },
    "sources": ["S5"]
  },
  "E5": {
    "type": "occupation",
    "individual_id": "I1",
    "date": {
      "value": "1925",
      "date_type": "from",
      "end_date": "1960"
    },
    "details": {
      "occupation": "Carpenter",
      "employer": "Smith Construction Co."
    }
  }
}
```

**Supported Event Types:**
- `birth`, `death`, `baptism`, `christening`, `burial`, `cremation`
- `marriage`, `divorce`, `engagement`, `marriage_banns`
- `adoption`, `bar_mitzvah`, `bat_mitzvah`, `confirmation`, `first_communion`
- `immigration`, `emigration`, `naturalization`
- `census`, `residence`, `occupation`, `retirement`, `military_service`
- `education`, `graduation`, `probate`, `will`, `custom`

**Date Object Structure:**
- `value`: ISO 8601 date (required)
- `date_type`: exact/approximate/before/after/between/from/to/calculated
- `original`: Original text representation from source
- `circa`: Boolean for approximate dates
- `end_date`: For date ranges

### Families Section

Simplified to focus on family unit relationships. Events are now stored separately.

```json
"families": {
  "F1": {
    "partners": [
      {
        "individual_id": "I1",
        "role": "spouse"
      },
      {
        "individual_id": "I2",
        "role": "spouse"
      }
    ],
    "children": [
      {
        "individual_id": "I5",
        "relationship_type": "biological"
      }
    ],
    "family_type": "nuclear",
    "events": ["E3"]
  }
}
```

**Changes from v1.0:**
- `partners` array replaces `husband`/`wife` for inclusivity
- Marriage event moved to events section
- Added `family_type` (nuclear/extended/blended/adoptive/foster)

### Places Section

**New in v2.0:** Structured location data for better geocoding and AI parsing.

```json
"places": {
  "P1": {
    "name": "New York, New York, USA",
    "components": {
      "locality": "New York",
      "county": "New York County",
      "state": "New York",
      "country": "United States",
      "country_code": "US"
    },
    "coordinates": {
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "historical_names": ["New Amsterdam"],
    "time_period": "1900-present"
  },
  "P2": {
    "name": "Los Angeles, California, USA",
    "components": {
      "locality": "Los Angeles",
      "county": "Los Angeles County",
      "state": "California",
      "country": "United States",
      "country_code": "US"
    },
    "coordinates": {
      "latitude": 34.0522,
      "longitude": -118.2437
    }
  }
}
```

### Sources Section

**Enhanced in v2.0:** Rich citation metadata for source quality evaluation.

```json
"sources": {
  "S1": {
    "title": "1900 United States Federal Census",
    "type": "census",
    "author": "U.S. Census Bureau",
    "publication": {
      "publisher": "National Archives and Records Administration",
      "year": 1900,
      "place": "Washington, D.C."
    },
    "repository_id": "R1",
    "citation": "Year: 1900; Census Place: New York, New York, New York; Roll: 1067; Page: 12B",
    "url": "https://www.ancestry.com/imageviewer/collections/7602/images/12345",
    "access_date": "2025-01-15",
    "quality": "primary",
    "confidence_level": "high",
    "media": ["M1"],
    "notes": ["N3"]
  },
  "S2": {
    "title": "Death Certificate for John Doe",
    "type": "vital_record",
    "date": "1985-03-20",
    "author": "Los Angeles County Registrar",
    "repository_id": "R2",
    "citation": "California Death Index, Certificate No. 85-123456",
    "quality": "primary",
    "confidence_level": "high"
  },
  "S3": {
    "title": "Doe Family Bible",
    "type": "personal_record",
    "date": "1850-1950",
    "description": "Family Bible with handwritten genealogy records",
    "quality": "secondary",
    "confidence_level": "medium",
    "notes": ["Handwritten entries of varying legibility"]
  }
}
```

**Source Quality Levels:**
- `primary`: Original documents (birth certificates, census records, etc.)
- `secondary`: Published records or compilations
- `tertiary`: Family lore, unverified information

### Repositories Section

**New in v2.0:** Track physical and digital archives holding source materials.

```json
"repositories": {
  "R1": {
    "name": "National Archives and Records Administration",
    "type": "government_archive",
    "address": {
      "street": "8601 Adelphi Road",
      "city": "College Park",
      "state": "Maryland",
      "country": "USA",
      "postal_code": "20740"
    },
    "website": "https://www.archives.gov",
    "contact": "research@nara.gov"
  },
  "R2": {
    "name": "Los Angeles County Registrar-Recorder/County Clerk",
    "type": "vital_records_office",
    "website": "https://lavote.gov"
  }
}
```

### Media Section

**Enhanced in v2.0:** More detailed metadata for multimedia objects.

```json
"media": {
  "M1": {
    "type": "photo",
    "format": "image/jpeg",
    "url": "https://example.com/photo1.jpg",
    "file_path": "/media/wedding_1925.jpg",
    "title": "Wedding Photo",
    "description": "Wedding photo of John and Jane Doe, June 10, 1925",
    "date": "1925-06-10",
    "photographer": "Smith Photography Studio",
    "individuals": ["I1", "I2"],
    "events": ["E3"],
    "repository_id": "R3",
    "copyright": "Public Domain",
    "notes": ["Original photo damaged, digitally restored"]
  },
  "M2": {
    "type": "document",
    "format": "application/pdf",
    "file_path": "/media/census_1900.pdf",
    "title": "1900 Census Record Scan",
    "description": "Scanned census page showing John Doe household",
    "date": "1900-06-01",
    "source_id": "S1"
  }
}
```

**Media Types:**
- `photo`, `document`, `audio`, `video`, `headstone`, `newspaper_clipping`

### Notes Section

**New in v2.0:** Structured research notes with attribution and timestamps.

```json
"notes": {
  "N1": {
    "text": "Birth date confirmed through multiple sources including census and baptism record.",
    "author": "John Researcher",
    "date": "2025-01-15T14:30:00Z",
    "type": "research_note",
    "related_to": {
      "individuals": ["I1"],
      "events": ["E1"]
    }
  },
  "N2": {
    "text": "Place of birth listed as 'New York' in census but baptism record specifies 'Brooklyn, Kings County'",
    "author": "John Researcher",
    "date": "2025-01-18T10:15:00Z",
    "type": "conflict_note",
    "priority": "high"
  },
  "N3": {
    "text": "Image quality is poor but entry is legible with magnification",
    "type": "source_note",
    "related_to": {
      "sources": ["S1"],
      "media": ["M1"]
    }
  }
}
```

**Note Types:**
- `research_note`, `conflict_note`, `todo`, `hypothesis`, `source_note`, `transcription`

## AI/LLM Parsing Benefits

GEN-JSON v2.0 is specifically optimized for AI and machine learning applications:

### 1. **Structured Name Parsing**
- Separate fields for given_name, surname, suffix enable direct NLP feature extraction
- No need to parse "Robert Smith Jr." into components
- Alternate names support maiden names and name changes over time

### 2. **Explicit Date Uncertainty**
- `date_type` field distinguishes exact dates from approximations
- LLMs can reason about temporal relationships with confidence levels
- Original date format preserved for source verification

### 3. **Hierarchical Place Data**
- Structured components (locality, county, state, country) enable geocoding
- Coordinates support spatial analysis and mapping
- Historical names support temporal reasoning

### 4. **Rich Event Context**
- Unlimited event types with extensible details
- Events linked to individuals, families, sources, and media
- Enables timeline construction and life story generation

### 5. **Data Quality Indicators**
- Confidence levels on individuals, events, and sources
- Source quality ratings (primary/secondary/tertiary)
- Conflict notes highlight data discrepancies for resolution

### 6. **Graph-Ready Structure**
- Clear ID-based references suitable for graph databases
- Relationship types (biological/adoptive/step) support genetic vs social analysis
- Event participation enables multi-party event modeling

### 7. **Source Provenance**
- Rich citation metadata enables source quality evaluation
- Repository tracking links to physical/digital archives
- Access dates and URLs support verification workflows

## Comparison with GEDCOM and GEN-JSON v1.0

| Feature                     | GEN-JSON v2.0      | GEN-JSON v1.0 | GEDCOM 5.5.1 |
| --------------------------- | ------------------ | ------------- | ------------ |
| **Readability**             | ✅ High             | ✅ High        | ❌ Low        |
| **Structured Names**        | ✅ Yes              | ❌ No          | ❌ No         |
| **Date Uncertainty**        | ✅ Explicit         | ❌ Limited     | ⚠️ Partial    |
| **Hierarchical Places**     | ✅ Yes              | ❌ No          | ❌ No         |
| **Event Extensibility**     | ✅ Unlimited        | ⚠️ Limited     | ⚠️ Limited    |
| **Data Quality Tracking**   | ✅ Yes              | ❌ No          | ❌ No         |
| **Source Quality Ratings**  | ✅ Yes              | ❌ No          | ❌ No         |
| **Relationship Types**      | ✅ Detailed         | ❌ Generic     | ❌ Generic    |
| **Metadata/Provenance**     | ✅ Complete         | ❌ None        | ⚠️ Minimal    |
| **Multimedia Support**      | ✅ Rich             | ✅ Basic       | ❌ Limited    |
| **AI/LLM Optimized**        | ✅ Yes              | ⚠️ Partial     | ❌ No         |

## Backward Compatibility

GEN-JSON v2.0 maintains backward compatibility with v1.0:

- v1.0 files can be upgraded by:
  - Converting `full_name` strings to structured `name` objects
  - Moving birth/death to events section
  - Adding default confidence levels
  - Wrapping simple place strings in place objects

- v2.0 parsers can read v1.0 files with fallback logic
- Fields are optional to support gradual migration

## Implementation Considerations

### Required Fields
- `version`: Format version string
- `individuals`: At least one individual record
- Individual `name` or `full_name`: Some form of name identifier
- Unique IDs for all entities (I1, F1, E1, S1, etc.)

### Recommended Practices
- Use UTF-8 encoding for all files
- Store dates in ISO 8601 format in `date.value`
- Preserve original date formats in `date.original`
- Include confidence levels for all factual claims
- Link all facts to sources where possible
- Use structured place objects for new data
- Add metadata for file tracking and provenance

### ID Conventions
- Individuals: `I1`, `I2`, `I3`, ...
- Families: `F1`, `F2`, `F3`, ...
- Events: `E1`, `E2`, `E3`, ...
- Sources: `S1`, `S2`, `S3`, ...
- Repositories: `R1`, `R2`, `R3`, ...
- Media: `M1`, `M2`, `M3`, ...
- Places: `P1`, `P2`, `P3`, ...
- Notes: `N1`, `N2`, `N3`, ...

### AI/LLM Integration Examples

**Query: "When was John Doe born?"**
```
Parse: individuals[I1].events -> filter type=birth -> E1
Read: events[E1].date.value = "1900-01-01"
Read: events[E1].date.date_type = "exact"
Read: events[E1].confidence_level = "high"
Response: "John Doe was born on January 1, 1900 (high confidence, exact date)"
```

**Query: "What occupations did John Doe have?"**
```
Parse: individuals[I1].events -> filter type=occupation -> [E5, E6]
Read: events[E5].details.occupation = "Carpenter"
Read: events[E5].date = "1925 to 1960"
Response: "John Doe was a Carpenter from 1925 to 1960"
```

**Query: "Show me John Doe's family tree"**
```
Parse: individuals[I1].parents -> [I3, I4]
Parse: individuals[I1].spouses -> [I2]
Parse: individuals[I1].children -> [I5]
Build graph with relationship types
```

## Future Enhancements

- **DNA Integration**: Add genetic marker fields for DNA test results
- **Graph Database Native Format**: Neo4j/ArangoDB import/export tools
- **Blockchain Verification**: Cryptographic signatures for data integrity
- **FHIR Integration**: Link to medical/health records (Family History in HL7 FHIR)
- **Linked Open Data**: RDF/JSON-LD serialization for semantic web
- **Privacy Controls**: Field-level access controls and encryption
- **Collaborative Editing**: Conflict resolution and merge strategies
- **AI Assistants**: Native support for AI-generated content flagging

## Conclusion

GEN-JSON v2.0 is a modern genealogy data format designed for clarity, usability, and AI/ML interoperability. With structured data, explicit metadata, and comprehensive event support, it enables next-generation genealogy applications to parse, analyze, and reason about family history data with unprecedented accuracy and depth.

