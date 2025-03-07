# GEN-JSON Integration Guide

## 📌 Overview
This guide explains how to integrate **GEN-JSON** into genealogy applications, databases, and APIs.

---
## **1️⃣ Using GEN-JSON in a Web Application**
### ✅ Load a GEN-JSON file in JavaScript
```javascript
fetch('data/family-tree.json')
  .then(response => response.json())
  .then(data => console.log('Family Tree:', data));
```

### ✅ Display Family Members in a Table
```javascript
function renderTable(genJson) {
    let table = '<table><tr><th>Name</th><th>Birth</th><th>Death</th></tr>';
    for (const id in genJson.individuals) {
        const person = genJson.individuals[id];
        table += `<tr><td>${person.full_name}</td><td>${person.birth?.date || 'N/A'}</td><td>${person.death?.date || 'N/A'}</td></tr>`;
    }
    table += '</table>';
    document.getElementById('output').innerHTML = table;
}
```

---
## **2️⃣ Storing GEN-JSON in a Database**
### ✅ Using MongoDB (NoSQL)
```javascript
const { MongoClient } = require('mongodb');
async function saveToMongo(genJson) {
    const client = await MongoClient.connect('mongodb://localhost:27017');
    const db = client.db('genealogy');
    await db.collection('familyTrees').insertOne(genJson);
    client.close();
}
```

### ✅ Using PostgreSQL (SQL)
```sql
CREATE TABLE individuals (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    birth_date DATE,
    death_date DATE
);
```

```javascript
async function saveToPostgres(genJson, client) {
    for (const id in genJson.individuals) {
        const person = genJson.individuals[id];
        await client.query('INSERT INTO individuals (full_name, birth_date, death_date) VALUES ($1, $2, $3)',
            [person.full_name, person.birth?.date, person.death?.date]);
    }
}
```

---
## **3️⃣ Converting GEN-JSON to Other Formats**
### ✅ Convert to CSV (Python)
```python
import json, csv

def convert_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Full Name", "Birth Date", "Death Date"])
        for person in data['individuals'].values():
            writer.writerow([person.get('full_name', ''), person.get('birth', {}).get('date', ''), person.get('death', {}).get('date', '')])

convert_to_csv('family-tree.json', 'output.csv')
```

---
## **4️⃣ Syncing with Cloud Storage**
### ✅ Save GEN-JSON to Firebase Firestore
```javascript
import { initializeApp } from 'firebase/app';
import { getFirestore, setDoc, doc } from 'firebase/firestore';

const firebaseConfig = { apiKey: 'your-api-key', projectId: 'your-project-id' };
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function uploadToFirestore(genJson) {
    await setDoc(doc(db, 'genealogy', 'tree1'), genJson);
}
```

---
## **5️⃣ API Endpoint for Serving GEN-JSON**
### ✅ Express.js API to Serve GEN-JSON
```javascript
const express = require('express');
const app = express();
app.get('/family-tree', (req, res) => {
    res.sendFile(__dirname + '/data/family-tree.json');
});
app.listen(3000, () => console.log('API running on port 3000'));
```

---
## **Conclusion**
GEN-JSON is **highly flexible** and can be integrated into genealogy software, APIs, and databases efficiently. 🚀