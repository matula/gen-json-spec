// GEN-JSON Validator Script
// Validates GEN-JSON files against the schema using AJV

const fs = require('fs');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

// Load Schema
const schema = JSON.parse(fs.readFileSync('schemas/gen-json-schema.json', 'utf-8'));
const validate = ajv.compile(schema);

// Load and Validate GEN-JSON File
function validateGenJson(filePath) {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    const valid = validate(data);

    if (!valid) {
        console.error('Validation Errors:', validate.errors);
    } else {
        console.log('GEN-JSON file is valid!');
    }
}

// Run Validation
const filePath = process.argv[2];
if (!filePath) {
    console.error('Usage: node genjson-validator.js <file.json>');
    process.exit(1);
}

validateGenJson(filePath);
