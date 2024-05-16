from flask import Flask, render_template, request, redirect, url_for, jsonify # type: ignore
from memory_manager import MemoryManager

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize with default settings, modify later
mmu = MemoryManager(total_memory=10000, strategy=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        total_memory = int(request.form['total_memory'])
        strategy = int(request.form['strategy'])
        global mmu
        mmu = MemoryManager(total_memory=total_memory, strategy=strategy)
        return redirect(url_for('manage_memory'))
    return render_template('index.html')

@app.route('/manage_memory')
def manage_memory():
    # Pass the current state of the memory to the template for initial visualization
    return render_template('manage_memory.html', blocks=mmu.get_memory_blocks())

@app.route('/operation', methods=['POST'])
def operation():
    action = request.form['action']
    if action == 'create':
        size = int(request.form['size'])
        if size <= 0:
            return jsonify(success = False, message = "Enter positive size!")
        pid, base, limit = mmu.allocate_memory(size)
        if pid:
            return jsonify(success=True, message=f'Process {pid} created.', pid=pid, base=base, limit=limit)
        return jsonify(success=False, message="Not enough memory")
    elif action == 'delete':
        pid = int(request.form['pid'])
        success = mmu.delete_process(pid)
        if success:
            return jsonify(success=True, message=f"Process {pid} deleted.")
        return jsonify(success=False, message=f"Process ID {pid} not found.")
    elif action == 'convert':
        pid = int(request.form['pid'])
        virtual_address = int(request.form['virtual_address'])
        if virtual_address<=0:
            return jsonify(success=False, message="Virtual address must be positive integer!")
        result = mmu.convert_address(pid, virtual_address)
        if isinstance(result, str):  # Checking if the result is an error message
            return jsonify(success=False, message=result)
        physical_address = result
        return jsonify(success=True, message=f"Physical Address: {physical_address}", physical_address=physical_address)
    return jsonify(success=False, message="Invalid action")




@app.route('/memory_blocks', methods=['GET'])
def memory_blocks():
    blocks = mmu.get_memory_blocks()
    total_memory = mmu.total_memory  # Ensure this is updated on memory reinitialization
    return jsonify(blocks=blocks, total_memory=total_memory)

@app.route('/fetch_memory_map', methods=['GET'])
def fetch_memory_map():
    memory_map = mmu.get_memory_map_as_list()  # Assume this method returns list of dicts
    return jsonify(memory_map=memory_map)





if __name__ == '__main__':
    app.run(debug=True)