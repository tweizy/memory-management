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
                self.last_allocated += 1
                pid = self.last_allocated
                self.processes[pid] = Process(pid, size, base)
                new_base = base + size
                if new_base <= limit:
                    self.free_blocks[i] = (new_base, limit)
                else:
                    del self.free_blocks[i]
                return pid, base, new_base - 1
        return None, None, None

    def next_fit(self, size):
        if len(self.processes) == 0 or size > self.total_memory:
            self.last_allocated += 1
            pid = self.last_allocated
            base = 0
            new_base = base + size
            self.processes[pid] = Process(pid, size, base)
            self.free_blocks[0] = (new_base, self.total_memory - 1)
            return pid, base, new_base - 1
        elif size > self.total_memory:
            return None, None, None
        
        for i, (base, limit) in enumerate(self.free_blocks):
            if limit - base + 1 >= size:
                if limit >= self.processes[self.last_allocated].limit:
                    self.last_allocated += 1
                    pid = self.last_allocated
                    self.processes[pid] = Process(pid, size, base)
                    new_base = base + size
                    if new_base <= limit:
                        self.free_blocks[i] = (new_base, limit)
                    else:
                        del self.free_blocks[i]
                    return pid, base, new_base - 1
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
            self.last_allocated += 1
            pid = self.last_allocated
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
            self.last_allocated += 1
            pid = self.last_allocated
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
            print(f"Process {pid}: Base={process.base}, Limit={process.limit +1}")
        for base, limit in self.free_blocks:
            print(f"Free: Base={base}, Limit={limit +1}")

    def get_memory_blocks(self):
        blocks = []
        # Include all processes as allocated blocks
        for pid, process in self.processes.items():
            blocks.append({
                'pid': pid,
                'base': process.base,
                'limit': process.limit,
                'size': process.size,
                'type': 'allocated'
            })

        # Include all free blocks
        for base, limit in self.free_blocks:
            blocks.append({
                'pid': None,
                'base': base,
                'limit': limit,
                'size': limit - base + 1,
                'type': 'free'
            })

        # Sort blocks by the base address
        blocks.sort(key=lambda block: block['base'])
        return blocks

    def get_memory_map_as_list(self):
        memory_map = []
        for pid, process in self.processes.items():
            memory_map.append({
                'Type': 'Process',
                'PID': pid,
                'Base': process.base,
                'Limit': process.limit,
                'Size': process.size
            })
        for base, limit in self.free_blocks:
            memory_map.append({
                'Type': 'Free',
                'PID': 'None',
                'Base': base,
                'Limit': limit,
                'Size': limit - base + 1
            })
        return memory_map
