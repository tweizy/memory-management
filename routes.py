from flask import Flask, render_template, request, redirect, url_for, jsonify
from memory_manager import MemoryManager

# Initialize Flask application with specified template and static directories
app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize MMU with default settings, modify later as needed
mmu = MemoryManager(total_memory=10000, strategy=1)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Route to handle the landing page and initialization of memory settings
    if request.method == 'POST':
        # Parse the total memory and strategy from the submitted form data
        total_memory = int(request.form['total_memory'])
        strategy = int(request.form['strategy'])

        # Re-initialize the MMU with the new settings
        global mmu
        mmu = MemoryManager(total_memory=total_memory, strategy=strategy)

        # Redirect to the manage_memory route to visualize the memory
        return redirect(url_for('manage_memory'))
    # Render the initial landing page
    return render_template('index.html')


@app.route('/manage_memory')
def manage_memory():
    # Route to display the current state of the memory
    return render_template('manage_memory.html', blocks=mmu.get_memory_blocks())


@app.route('/operation', methods=['POST'])
def operation():
    # Route to handle memory operations like create, delete, convert
    action = request.form['action']
    if action == 'create':
        size = int(request.form['size'])
        # Ensure memory size for creation is positive
        if size <= 0:
            return jsonify(success=False, message="Enter a positive size!")
        pid, base, limit = mmu.allocate_memory(size)
        if pid:
            # If the process is created successfully, return success response
            return jsonify(success=True, message=f'Process {pid} created.', pid=pid, base=base, limit=limit)
        # If memory is insufficient, inform the user
        return jsonify(success=False, message="Not enough memory")
    elif action == 'delete':
        pid = int(request.form['pid'])
        success = mmu.delete_process(pid)
        if success:
            # Confirm deletion success
            return jsonify(success=True, message=f"Process {pid} deleted.")
        # If the process ID is not found, notify the user
        return jsonify(success=False, message=f"Process ID {pid} not found.")
    elif action == 'convert':
        pid = int(request.form['pid'])
        virtual_address = int(request.form['virtual_address'])
        # Ensure virtual address is a positive integer
        if virtual_address <= 0:
            return jsonify(success=False, message="Virtual address must be positive integer!")
        result = mmu.convert_address(pid, virtual_address)
        if isinstance(result, str):
            # If there's an error in conversion, return the error message
            return jsonify(success=False, message=result)
        physical_address = result
        # Successfully converted virtual address to physical address
        return jsonify(success=True, message=f"Physical Address: {physical_address}", physical_address=physical_address)
    # Handle invalid actions gracefully
    return jsonify(success=False, message="Invalid action")


@app.route('/memory_blocks', methods=['GET'])
def memory_blocks():
    # Fetch and return all memory blocks along with the total memory
    blocks = mmu.get_memory_blocks()
    total_memory = mmu.total_memory  # Ensure this is updated on memory reinitialization
    return jsonify(blocks=blocks, total_memory=total_memory)


@app.route('/fetch_memory_map', methods=['GET'])
def fetch_memory_map():
    # Route to fetch and return the memory map as a list of dictionaries
    memory_map = mmu.get_memory_map_as_list()
    return jsonify(memory_map=memory_map)


# Entry point for running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
