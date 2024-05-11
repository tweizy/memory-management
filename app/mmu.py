class Process:
    def __init__(self, pid, size, base):
        self.pid = pid
        self.size = size
        self.base = base
        self.limit = base + size - 1

class MemoryManager:
    def __init__(self, total_memory, strategy):
        self.total_memory = total_memory
        self.strategy = strategy
        self.processes = {}
        self.free_blocks = [(0, total_memory - 1)]  # (base, limit)
        self.last_allocated = 0  # For Next Fit

    def allocate_memory(self, size):
        strategy_method = {
            1: self.first_fit,
            2: self.next_fit,
            3: self.best_fit,
            4: self.worst_fit
        }
        return strategy_method[self.strategy](size)

    def first_fit(self, size):
        for i, (base, limit) in enumerate(self.free_blocks):
            if limit - base + 1 >= size:
                pid = len(self.processes) + 1
                self.processes[pid] = Process(pid, size, base)
                new_base = base + size
                if new_base <= limit:
                    self.free_blocks[i] = (new_base, limit)
                else:
                    del self.free_blocks[i]
                return pid, base, new_base - 1
        return None, None, None

    def next_fit(self, size):
        start_index = 0
        searched = False
        while True:
            for i in range(start_index, len(self.free_blocks)):
                base, limit = self.free_blocks[i]
                if limit - base + 1 >= size:
                    pid = len(self.processes) + 1
                    self.processes[pid] = Process(pid, size, base)
                    new_base = base + size
                    if new_base <= limit:
                        self.free_blocks[i] = (new_base, limit)
                    else:
                        del self.free_blocks[i]
                    self.last_allocated = i
                    return pid, base, new_base - 1
            if searched:
                break
            start_index = 0
            searched = True
        return None, None, None

    def best_fit(self, size):
        best_index = None
        min_diff = float('inf')
        for i, (base, limit) in enumerate(self.free_blocks):
            if limit - base + 1 >= size and (limit - base + 1 - size) < min_diff:
                min_diff = limit - base + 1 - size
                best_index = i
        if best_index is not None:
            base, limit = self.free_blocks[best_index]
            pid = len(self.processes) + 1
            self.processes[pid] = Process(pid, size, base)
            new_base = base + size
            if new_base <= limit:
                self.free_blocks[best_index] = (new_base, limit)
            else:
                del self.free_blocks[best_index]
            return pid, base, new_base - 1
        return None, None, None

    def worst_fit(self, size):
        worst_index = None
        max_diff = -1
        for i, (base, limit) in enumerate(self.free_blocks):
            if limit - base + 1 >= size and (limit - base + 1 - size) > max_diff:
                max_diff = limit - base + 1 - size
                worst_index = i
        if worst_index is not None:
            base, limit = self.free_blocks[worst_index]
            pid = len(self.processes) + 1
            self.processes[pid] = Process(pid, size, base)
            new_base = base + size
            if new_base <= limit:
                self.free_blocks[worst_index] = (new_base, limit)
            else:
                del self.free_blocks[worst_index]
            return pid, base, new_base - 1
        return None, None, None

    def delete_process(self, pid):
        if pid in self.processes:
            process = self.processes.pop(pid)
            self.free_blocks.append((process.base, process.limit))
            self.free_blocks = sorted(self.free_blocks, key=lambda x: x[0])  # Keep sorted
            self.merge_free_blocks()
            return True
        return False

    def merge_free_blocks(self):
        merged_blocks = []
        last_base, last_limit = self.free_blocks[0]
        for base, limit in self.free_blocks[1:]:
            if base <= last_limit + 1:
                last_limit = max(last_limit, limit)
            else:
                merged_blocks.append((last_base, last_limit))
                last_base, last_limit = base, limit
        merged_blocks.append((last_base, last_limit))
        self.free_blocks = merged_blocks

    def convert_address(self, pid, virtual_address):
        if pid in self.processes:
            process = self.processes[pid]
            if 0 <= virtual_address < process.size:
                physical_address = process.base + virtual_address
                return f"Physical Address: {physical_address}"
            else:
                return "Error: Virtual address is outside the process's address space."
        else:
            return "Error: Process ID not found."

    def print_memory_map(self):
        print("Memory Map:")
        for pid, process in self.processes.items():
            print(f"Process {pid}: Base={process.base}, Limit={process.limit}")
        for base, limit in self.free_blocks:
            print(f"Free: Base={base}, Limit={limit}")