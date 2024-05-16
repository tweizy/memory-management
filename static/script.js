document.addEventListener('DOMContentLoaded', function() {
    setupFormEventListeners();
    fetchMemoryMap();
});

function setupFormEventListeners() {
    const forms = ['createForm', 'deleteForm', 'convertForm'];
    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                const action = formId.replace('Form', '');
                submitOperationForm(action);
            });
        }
    });
}

function submitOperationForm(action) {
    const form = document.getElementById(action + 'Form');
    const formData = new FormData(form);
    formData.append('action', action);

    fetch('/operation', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error, status = ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        displayMessage(data.message);
        if (data.success) {
            fetchMemoryMap();
        }
    })
    .catch(error => {
        console.error('Error processing operation:', error);
        displayMessage('Error processing operation: ' + error.message);
    });
}

function fetchMemoryMap() {
    fetch('/memory_blocks')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error, status = ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        updateMemoryVisualization(data.blocks);
        updateMemoryTable(data.blocks);
    })
    .catch(error => {
        console.error('Error fetching memory map:', error);
        displayMessage('Error fetching memory map: ' + error.message);
    });
}

function updateMemoryVisualization(blocks) {
    const visualization = document.getElementById('memoryVisualization');
    visualization.innerHTML = ''; // Clear existing visualization
    blocks.forEach(block => {
        const blockDiv = document.createElement('div');
        blockDiv.className = `memory-block ${block.pid ? 'allocated' : 'free'}`;
        blockDiv.textContent = `${block.pid ? `PID ${block.pid}: ${block.size}KB , Base : ${block.base}, Size : ${block.size}` : `Free: ${block.size} KB`}`;
        visualization.appendChild(blockDiv);
    });
}


function updateMemoryTable(blocks) {
    const table = document.getElementById('processTable');
    if (table) {
        table.innerHTML = '<tr><th>Process ID</th><th>Size (K)</th><th>Status</th><th>Base</th></tr>';
        blocks.forEach(block => {
            const row = table.insertRow(-1);
            row.insertCell(0).textContent = block.pid ? `PID ${block.pid}` : 'Free';
            row.insertCell(1).textContent = `${block.size} KB`;
            row.insertCell(2).textContent = block.pid ? 'Allocated' : 'Free';
            row.insertCell(3).textContent = `${block.base}`;

        });
    } else {
        console.error('MemoryMapTable element not found');
    }
}

function displayMessage(message) {
    const messageDisplay = document.getElementById('messageDisplay');
    messageDisplay.textContent = message;
}
