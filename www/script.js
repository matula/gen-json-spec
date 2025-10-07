// Global variables
let familyData = null;
let selectedPersonId = null;

// DOM elements
const fileInput = document.getElementById('jsonFileInput');
const loadExampleBtn = document.getElementById('loadExampleBtn');
const familyTreeContainer = document.getElementById('familyTree');
const personDetailsContainer = document.getElementById('personDetails');

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    fileInput.addEventListener('change', handleFileUpload);
    loadExampleBtn.addEventListener('click', loadExampleData);
});

// File handling functions
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    try {
        const fileContent = await readFileAsText(file);
        const jsonData = JSON.parse(fileContent);
        processData(jsonData);
    } catch (error) {
        showError('Error loading file: ' + error.message);
    }
}

function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = event => resolve(event.target.result);
        reader.onerror = error => reject(error);
        reader.readAsText(file);
    });
}

async function loadExampleData() {
    try {
        const response = await fetch('../examples/example1.json');
        if (!response.ok) {
            throw new Error('Failed to load example data');
        }
        const jsonData = await response.json();
        processData(jsonData);
    } catch (error) {
        showError('Error loading example: ' + error.message);
    }
}

// Data processing
function processData(data) {
    if (!validateData(data)) {
        showError('Invalid gen-json format');
        return;
    }

    familyData = data;
    renderFamilyTree();
    clearPersonDetails();
}

function validateData(data) {
    // Basic validation to ensure it's a gen-json file
    return data && data.individuals && typeof data.individuals === 'object';
}

// Tree rendering
function renderFamilyTree() {
    familyTreeContainer.innerHTML = '';

    if (!familyData || !familyData.individuals) {
        familyTreeContainer.innerHTML = '<p>No family data loaded</p>';
        return;
    }

    // Find root individuals (those without parents or with unknown parents)
    const rootIndividuals = findRootIndividuals();

    if (rootIndividuals.length === 0) {
        // If no clear roots, just show all individuals
        const treeFragment = document.createDocumentFragment();
        Object.keys(familyData.individuals).forEach(id => {
            const person = familyData.individuals[id];
            const personNode = createPersonNode(id, person, 0);
            treeFragment.appendChild(personNode);
        });
        familyTreeContainer.appendChild(treeFragment);
    } else {
        // Create tree starting with root individuals
        const treeFragment = document.createDocumentFragment();
        rootIndividuals.forEach(id => {
            const person = familyData.individuals[id];
            const personNode = createPersonNode(id, person, 0);
            const childrenContainer = renderChildren(id, 1, []);
            if (childrenContainer) {
                personNode.appendChild(childrenContainer);
            }
            treeFragment.appendChild(personNode);
        });
        familyTreeContainer.appendChild(treeFragment);
    }
}

function findRootIndividuals() {
    const roots = [];

    for (const id in familyData.individuals) {
        const person = familyData.individuals[id];
        if (!person.parents || person.parents.length === 0) {
            roots.push(id);
        }
    }

    return roots;
}

function renderChildren(parentId, depth, visitedIds) {
    if (depth > 10 || visitedIds.includes(parentId)) {
        // Prevent infinite recursion due to circular relationships
        return null;
    }

    // Add this person to visited list
    visitedIds = [...visitedIds, parentId];

    const parent = familyData.individuals[parentId];
    if (!parent || !parent.children || parent.children.length === 0) {
        return null;
    }

    const childrenContainer = document.createElement('div');
    childrenContainer.className = 'tree-line';

    parent.children.forEach(childId => {
        if (familyData.individuals[childId]) {
            const child = familyData.individuals[childId];
            const childNode = createPersonNode(childId, child, depth);

            // Recursively add this child's children
            const grandchildrenContainer = renderChildren(childId, depth + 1, visitedIds);
            if (grandchildrenContainer) {
                childNode.appendChild(grandchildrenContainer);
            }

            childrenContainer.appendChild(childNode);
        }
    });

    return childrenContainer;
}

function createPersonNode(id, person, depth) {
    const nodeDiv = document.createElement('div');
    nodeDiv.className = 'tree-node';
    nodeDiv.dataset.id = id;

    // Add selection class if this is the selected person
    if (id === selectedPersonId) {
        nodeDiv.classList.add('selected');
    }

    // Create person display with name and dates
    const nameSpan = document.createElement('div');
    nameSpan.className = 'name';
    nameSpan.textContent = person.full_name || 'Unknown';

    const datesSpan = document.createElement('div');
    datesSpan.className = 'dates';

    // Format birth-death years
    let dateText = '';
    if (person.birth && person.birth.date) {
        dateText += extractYear(person.birth.date);
    } else {
        dateText += '?';
    }

    dateText += ' - ';

    if (person.death && person.death.date) {
        dateText += extractYear(person.death.date);
    } else if (Object.keys(person.death || {}).length === 0) {
        dateText += 'present';
    } else {
        dateText += '?';
    }

    datesSpan.textContent = dateText;

    nodeDiv.appendChild(nameSpan);
    nodeDiv.appendChild(datesSpan);

    // Add click event to show person details
    nodeDiv.addEventListener('click', (event) => {
        event.stopPropagation();
        selectPerson(id);
    });

    return nodeDiv;
}

function extractYear(dateString) {
    // Extract year from ISO date or other formats
    if (!dateString) return '?';

    // Try ISO format first (YYYY-MM-DD)
    const isoMatch = dateString.match(/^(\d{4})-\d{2}-\d{2}$/);
    if (isoMatch) return isoMatch[1];

    // Try to extract any 4-digit year
    const yearMatch = dateString.match(/\b(\d{4})\b/);
    if (yearMatch) return yearMatch[1];

    return dateString;
}

// Person details
function selectPerson(id) {
    // Update selected state
    const previousSelected = document.querySelector('.tree-node.selected');
    if (previousSelected) {
        previousSelected.classList.remove('selected');
    }

    const newSelected = document.querySelector(`.tree-node[data-id="${id}"]`);
    if (newSelected) {
        newSelected.classList.add('selected');
        // Scroll to the selected person
        newSelected.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    selectedPersonId = id;
    renderPersonDetails(id);
}

function renderPersonDetails(id) {
    personDetailsContainer.innerHTML = '';

    if (!familyData || !familyData.individuals || !familyData.individuals[id]) {
        personDetailsContainer.innerHTML = '<p class="select-person-message">Person not found</p>';
        return;
    }

    const person = familyData.individuals[id];

    // Create details container
    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'person-details';

    // Name
    addDetailItem(detailsDiv, 'Name', person.full_name || 'Unknown');

    // Sex
    if (person.sex) {
        addDetailItem(detailsDiv, 'Sex', person.sex === 'M' ? 'Male' : person.sex === 'F' ? 'Female' : person.sex);
    }

    // Birth
    if (person.birth) {
        let birthInfo = '';
        if (person.birth.date) birthInfo += person.birth.date;
        if (person.birth.date && person.birth.place) birthInfo += ', ';
        if (person.birth.place) birthInfo += person.birth.place;

        if (birthInfo) {
            addDetailItem(detailsDiv, 'Birth', birthInfo);
        }
    }

    // Death
    if (person.death && (person.death.date || person.death.place)) {
        let deathInfo = '';
        if (person.death.date) deathInfo += person.death.date;
        if (person.death.date && person.death.place) deathInfo += ', ';
        if (person.death.place) deathInfo += person.death.place;

        if (deathInfo) {
            addDetailItem(detailsDiv, 'Death', deathInfo);
        }
    }

    // Parents
    if (person.parents && person.parents.length > 0) {
        const parentsDiv = document.createElement('div');
        parentsDiv.className = 'person-detail-item';

        const parentsLabel = document.createElement('div');
        parentsLabel.className = 'person-detail-label';
        parentsLabel.textContent = 'Parents';

        const parentsContent = document.createElement('div');
        parentsContent.className = 'person-relatives';

        person.parents.forEach(parentId => {
            if (familyData.individuals[parentId]) {
                const parent = familyData.individuals[parentId];
                addRelativeLink(parentsContent, parentId, parent.full_name || 'Unknown');
            }
        });

        parentsDiv.appendChild(parentsLabel);
        parentsDiv.appendChild(parentsContent);
        detailsDiv.appendChild(parentsDiv);
    }

    // Spouses
    if (person.spouses && person.spouses.length > 0) {
        const spousesDiv = document.createElement('div');
        spousesDiv.className = 'person-detail-item';

        const spousesLabel = document.createElement('div');
        spousesLabel.className = 'person-detail-label';
        spousesLabel.textContent = 'Spouses';

        const spousesContent = document.createElement('div');
        spousesContent.className = 'person-relatives';

        person.spouses.forEach(spouseId => {
            if (familyData.individuals[spouseId]) {
                const spouse = familyData.individuals[spouseId];
                addRelativeLink(spousesContent, spouseId, spouse.full_name || 'Unknown');
            }
        });

        spousesDiv.appendChild(spousesLabel);
        spousesDiv.appendChild(spousesContent);
        detailsDiv.appendChild(spousesDiv);
    }

    // Children
    if (person.children && person.children.length > 0) {
        const childrenDiv = document.createElement('div');
        childrenDiv.className = 'person-detail-item';

        const childrenLabel = document.createElement('div');
        childrenLabel.className = 'person-detail-label';
        childrenLabel.textContent = 'Children';

        const childrenContent = document.createElement('div');
        childrenContent.className = 'person-relatives';

        person.children.forEach(childId => {
            if (familyData.individuals[childId]) {
                const child = familyData.individuals[childId];
                addRelativeLink(childrenContent, childId, child.full_name || 'Unknown');
            }
        });

        childrenDiv.appendChild(childrenLabel);
        childrenDiv.appendChild(childrenContent);
        detailsDiv.appendChild(childrenDiv);
    }

    personDetailsContainer.appendChild(detailsDiv);
}

function addDetailItem(container, label, value) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'person-detail-item';

    const labelDiv = document.createElement('div');
    labelDiv.className = 'person-detail-label';
    labelDiv.textContent = label;

    const valueDiv = document.createElement('div');
    valueDiv.textContent = value;

    itemDiv.appendChild(labelDiv);
    itemDiv.appendChild(valueDiv);
    container.appendChild(itemDiv);
}

function addRelativeLink(container, id, name) {
    const link = document.createElement('span');
    link.className = 'person-relative';
    link.textContent = name;
    link.dataset.id = id;
    link.addEventListener('click', () => selectPerson(id));
    container.appendChild(link);
}

function clearPersonDetails() {
    personDetailsContainer.innerHTML = '<p class="select-person-message">Select a person from the tree to view their details</p>';
    selectedPersonId = null;
}

// Utility functions
function showError(message) {
    alert(message);
}
