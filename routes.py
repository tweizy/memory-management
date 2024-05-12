from flask import Flask, render_template, request, redirect, url_for, jsonify
from app.mmu import MemoryManager

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
        pid, base, limit = mmu.allocate_memory(size)
        if pid:
            return jsonify(success=True, message=f'Process {pid} created.', pid=pid, base=base, limit=limit)
        else:
            return jsonify(success=False, message="Not enough memory")
    # Implement additional actions with similar structure
    return jsonify(success=False, message="Invalid action")


@app.route('/memory_blocks', methods=['GET'])
def memory_blocks():
    return jsonify(blocks=mmu.get_memory_blocks())



if __name__ == '__main__':
    app.run(debug=True)
