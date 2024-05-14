document.addEventListener('DOMContentLoaded', function() {
    const createForm = document.getElementById('createForm');
    const deleteForm = document.getElementById('deleteForm');
    const convertForm = document.getElementById('convertForm');

    if (createForm) {
        createForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitOperationForm('create');
        });
    }

    if (deleteForm) {
        deleteForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitOperationForm('delete');
        });
    }

    if (convertForm) {
        convertForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitOperationForm('convert');
        });
    }

    fetchMemoryMap();
});

function submitOperationForm(action) {
    const form = document.getElementById(action + 'Form');
    if (!form) {
        console.error(action + 'Form not found');
        return;
    }

    const formData = new FormData(form);
    formData.append('action', action);  // Ensure this is necessary on your server-side handling.

    fetch('/operation', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        if (data.success) {
            fetchMemoryMap();
        }
    })
    .catch(error => {
        console.error('Error processing operation:', error);
        alert('Error processing operation: ' + error.message);
    });
}


function fetchMemoryMap() {
    fetch('/memory_blocks')
    .then(response => response.json())
    .then(data => {
        updateMemoryVisualization(data.blocks);
        updateMemoryTable(data.blocks);
    })
    .catch(error => {
        console.error('Error fetching memory map:', error);
        alert('Error fetching memory map: ' + error.message);
    });
}

function updateMemoryVisualization(blocks) {
    const visualization = document.getElementById('memoryVisualization');
    if (visualization) {
        visualization.innerHTML = '';
        blocks.forEach(block => {
            const blockDiv = document.createElement('div');
            blockDiv.className = 'memory-block ' + (block.pid ? 'allocated' : 'free');
            blockDiv.textContent = `${block.pid ? `PID ${block.pid}` : 'Free'}: ${block.size}KB`;
            visualization.appendChild(blockDiv);
        });
    }
}

function updateMemoryTable(blocks) {
    const table = document.getElementById('memoryMapTable');
    if (table) {
        table.innerHTML = '<tr><th>Process ID</th><th>Size (K)</th><th>Status</th></tr>';
        blocks.forEach(block => {
            const row = table.insertRow(-1);
            row.insertCell(0).textContent = block.pid ? `PID ${block.pid}` : 'Free';
            row.insertCell(1).textContent = `${block.size} KB`;
            row.insertCell(2).textContent = block.pid ? 'Allocated' : 'Free';
        });
    }
}

function displayConversionResult(data) {
    const resultBox = document.getElementById('conversionResult');
    if (resultBox) {
        resultBox.textContent = data.message;
    }
}
