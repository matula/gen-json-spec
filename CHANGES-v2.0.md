# GEN-JSON v2.0 Changes Summary

## Overview

Version 2.0 represents a major enhancement to GEN-JSON, specifically optimized for AI/LLM parsing and modern genealogical research workflows. The changes address key limitations in v1.0 that made machine parsing difficult.

## Critical Improvements for AI/LLM Parsing

### 1. **Structured Names** (Was: Single String)
**v1.0 Problem:** `"full_name": "Robert Smith Jr."` required NLP parsing to extract components.

**v2.0 Solution:**
```json
"name": {
  "given_name": "Robert",
  "surname": "Smith",
  "suffix": "Jr.",
  "nickname": "Bob",
  "name_type": "legal"
}
```

**AI Benefit:** Direct field access, no parsing required. Supports alternate names for maiden names, name changes.

### 2. **Enhanced Date Representation** (Was: Simple ISO Strings)
**v1.0 Problem:** `"date": "1900-01-01"` didn't distinguish exact dates from approximations.

**v2.0 Solution:**
```json
"date": {
  "value": "1900-01-01",
  "date_type": "exact",
  "original": "1 JAN 1900",
  "circa": false
}
```

**AI Benefit:** Explicit uncertainty tracking enables temporal reasoning with confidence levels.

### 3. **Hierarchical Place Data** (Was: Free Text)
**v1.0 Problem:** `"place": "Chicago, USA"` required geocoding and parsing.

**v2.0 Solution:**
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
    "historical_names": ["New Amsterdam"]
  }
}
```

**AI Benefit:** Location-based queries, geocoding, historical name resolution.

### 4. **Centralized Event System** (Was: Inline Birth/Death)
**v1.0 Problem:** Limited to birth/death in individuals, marriage in families. No extensibility.

**v2.0 Solution:**
```json
"events": {
  "E1": {
    "type": "birth",
    "individual_id": "I1",
    "date": { ... },
    "place": { ... },
    "confidence_level": "high",
    "sources": ["S1"]
  },
  "E4": {
    "type": "immigration",
    "individual_id": "I1",
    "details": {
      "ship_name": "SS Bremen",
      "arrival_port": "New York Harbor"
    }
  }
}
```

**AI Benefit:** Unlimited event types (birth, death, marriage, immigration, occupation, military service, etc.). Consistent structure for timeline generation.

### 5. **Data Quality Indicators** (Was: None)
**v1.0 Problem:** No way to track confidence or source quality.

**v2.0 Solution:**
- `confidence_level`: "high", "medium", "low", "unknown" on individuals, events, sources
- `quality`: "primary", "secondary", "tertiary" on sources
- Structured `notes` with conflict tracking

**AI Benefit:** LLMs can weight conflicting information and prioritize reliable sources.

### 6. **Typed Relationships** (Was: Generic Arrays)
**v1.0 Problem:** `"parents": ["I3", "I4"]` didn't distinguish biological vs. adoptive.

**v2.0 Solution:**
```json
"parents": [
  {
    "individual_id": "I3",
    "relationship_type": "biological",
    "parent_type": "father"
  },
  {
    "individual_id": "I4",
    "relationship_type": "adoptive",
    "parent_type": "mother"
  }
]
```

**AI Benefit:** Genetic vs. social relationship analysis for medical history and inheritance research.

### 7. **Rich Source Metadata** (Was: Basic Title/URL)
**v1.0 Problem:** Minimal citation information.

**v2.0 Solution:**
```json
"sources": {
  "S1": {
    "title": "1900 United States Federal Census",
    "type": "census",
    "author": "U.S. Census Bureau",
    "publication": {
      "publisher": "NARA",
      "year": 1900
    },
    "repository_id": "R1",
    "citation": "Year: 1900; Roll: 1067; Page: 12B",
    "quality": "primary",
    "confidence_level": "high"
  }
}
```

**AI Benefit:** Source evaluation, citation network analysis, authority assessment.

### 8. **File Metadata & Provenance** (Was: None)
**v2.0 Addition:**
```json
"metadata": {
  "created": "2025-01-15T10:30:00Z",
  "creator": { "name": "Jane Researcher", "software": "GEN-JSON Editor v2.0" },
  "change_log": [ ... ]
}
```

**AI Benefit:** Data lineage tracking, version control, collaborative research workflows.

### 9. **Repositories Section** (Was: None)
**v2.0 Addition:** Track physical and digital archives holding source materials.

**AI Benefit:** Research planning, source discovery, archive linking.

### 10. **Notes Section** (Was: Simple String Arrays)
**v2.0 Solution:**
```json
"notes": {
  "N1": {
    "text": "Birth date confirmed through multiple sources",
    "author": "Jane Researcher",
    "date": "2025-01-15T14:30:00Z",
    "type": "research_note",
    "related_to": {
      "individuals": ["I1"],
      "events": ["E1"]
    }
  }
}
```

**AI Benefit:** Research context, conflict resolution, hypothesis tracking.

## Backward Compatibility

v2.0 maintains backward compatibility with v1.0:
- JSON Schema validates both versions
- v1.0 fields still supported (full_name, birth/death inline)
- Migration path documented for upgrading v1.0 to v2.0
- Tools can read both formats with fallback logic

## Files Updated

1. **SPECIFICATION.md** - Completely rewritten for v2.0 with AI/LLM focus
2. **schemas/gen-json-schema.json** - Extended to validate v2.0 features while maintaining v1.0 support
3. **examples/example-v2-comprehensive.json** - New comprehensive example demonstrating all v2.0 features
4. **CLAUDE.md** - Updated with v2.0 architecture and migration guidance

## Tools That Need Updating

1. **tools/gedcom-to-genjson.py** - Currently outputs v1.0; needs v2.0 support
2. **www/** (Web Viewer) - Currently parses v1.0; needs v2.0 support
3. **tools/gen-json-validator.js** - Should work with updated schema

## AI/LLM Query Examples

**v1.0 Query Challenge:**
```
User: "When did John immigrate to America?"
Problem: Immigration data not in standard format, requires parsing notes/descriptions
```

**v2.0 Query Solution:**
```javascript
// Parse events array
const immigrationEvents = events.filter(e =>
  e.type === "immigration" &&
  e.individual_id === "I1"
);

// Extract date with uncertainty
const event = immigrationEvents[0];
const date = event.date.value; // "1920"
const dateType = event.date.date_type; // "approximate"
const confidence = event.confidence_level; // "high"

// Response: "John immigrated to America around 1920 (approximate date, high confidence)"
```

## Benefits Summary

| Capability | v1.0 | v2.0 |
|------------|------|------|
| Name parsing | Manual NLP | Direct field access |
| Date uncertainty | Not captured | Explicit date_type |
| Location hierarchy | Parse strings | Structured components |
| Event types | 2-3 fixed | Unlimited extensible |
| Data quality | Not tracked | Confidence + quality levels |
| Relationship types | Generic | Typed (biological/adoptive/etc) |
| Source evaluation | Basic | Rich citation metadata |
| Timeline generation | Limited | Event-centric model |
| Conflict resolution | No support | Notes + confidence levels |
| Geocoding | Manual | Built-in coordinates |
| AI/LLM queries | Difficult | Optimized |

## Recommendation

**For new projects:** Use v2.0 for maximum AI/LLM compatibility and research capability.

**For existing v1.0 data:** Migrate gradually using documented migration path. v2.0 parsers can read v1.0 with fallback.

**For GEDCOM conversion:** Update converter to output v2.0 format to fully leverage modern genealogy research tools.
