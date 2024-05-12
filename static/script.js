document.addEventListener('DOMContentLoaded', function() {
    const initForm = document.getElementById('initForm');
    initForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(() => fetchMemoryBlocks()); // Update memory blocks after initialization
    });

    function fetchMemoryBlocks() {
    fetch('/memory_blocks')
    .then(response => response.json())
    .then(data => {
        const memoryMap = document.getElementById('memoryMap');
        memoryMap.innerHTML = ''; // Clear previous content
        data.blocks.forEach(block => {
            const blockDiv = document.createElement('div');
            blockDiv.className = 'memory-block';
            blockDiv.textContent = `${block.pid} : Base ${block.base} - Limit ${block.limit}`;
            blockDiv.style.width = `${block.size}px`; // Example: Adjust width proportionally or set a constant value
            blockDiv.style.backgroundColor = 'lightblue'; // Visual cue
            blockDiv.style.margin = '5px'; // Spacing
            memoryMap.appendChild(blockDiv);
        });
    });
}

});

document.addEventListener('DOMContentLoaded', function() {
    fetchMemoryMap();  // Load initial memory visualization
});

function submitOperationForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    fetch('/operation', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || 'Operation successful');
            fetchMemoryMap();  // Update visualization after operation
        } else {
            alert(data.message || 'Operation failed');
        }
    })
    .catch(error => alert('Error processing operation'));
}

function fetchMemoryMap() {
    fetch('/memory_blocks')
    .then(response => response.json())
    .then(data => {
        const visualization = document.getElementById('memoryVisualization');
        visualization.innerHTML = '';  // Clear existing visualization
        data.blocks.forEach(block => {
            const blockDiv = document.createElement('div');
            blockDiv.className = 'memory-block';
            blockDiv.classList.add(block.pid ? 'allocated' : 'free');
            blockDiv.style.width = `${block.size * 5}px`;  // Adjust size for better visibility
            blockDiv.textContent = block.pid ? `PID ${block.pid}: ${block.size}KB` : `Free: ${block.size}KB`;
            visualization.appendChild(blockDiv);
        });
    })
    .catch(error => console.error('Error fetching memory map:', error));
}

