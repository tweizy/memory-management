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
        const totalMemory = data.total_memory;
        const usedMemory = data.blocks.reduce((acc, block) => block.type === 'allocated' ? acc + block.size : acc, 0);
        const freeMemory = totalMemory - usedMemory;
        renderMemoryChart(usedMemory, freeMemory);
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
let memoryChart = null;

function renderMemoryChart(usedMemory, freeMemory) {
    const ctx = document.getElementById('memoryChart').getContext('2d');

    // Destroy existing chart instance if it exists
    if (memoryChart) {
        memoryChart.destroy();
    }

    // Calculate percentages for the legend
    const totalMemory = usedMemory + freeMemory;
    const usedPercentage = ((usedMemory / totalMemory) * 100).toFixed(1);
    const freePercentage = ((freeMemory / totalMemory) * 100).toFixed(1);

    // Create a new chart instance
    memoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Used Memory', 'Free Memory'],
            datasets: [{
                label: 'Memory Usage',
                data: [usedMemory, freeMemory],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            let label = tooltipItem.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += `${tooltipItem.raw} KB (${tooltipItem.dataset.data[tooltipItem.dataIndex] === usedMemory ? usedPercentage : freePercentage}%)`;
                            return label;
                        }
                    }
                }
            }
        }
    });
}

