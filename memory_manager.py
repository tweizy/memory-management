class Process:
    """
    Represents a single process in memory, containing details about its ID, size, and memory location.
    """
    def __init__(self, pid, size, base):
        self.pid = pid          # Process ID
        self.size = size        # Size of the process in KB
        self.base = base        # Base address of the process in memory
        self.limit = base + size - 1  # Limit address of the process in memory

class MemoryManager:
    """
    Manages the allocation and deallocation of memory using different strategies.
    """
    def __init__(self, total_memory, strategy):
        self.total_memory = total_memory  # Total size of the memory in KB
        self.strategy = strategy          # Allocation strategy (1-4)
        self.processes = {}               # Dictionary to store process information, keyed by PID
        self.free_blocks = [(0, total_memory - 1)]  # List of tuples representing free memory blocks
        self.last_allocated = 0           # Keeps track of the last allocated position for Next Fit

    def allocate_memory(self, size):
        """
        Delegates the memory allocation to the appropriate method based on the selected strategy.
        """
        strategy_method = {
            1: self.first_fit,
            2: self.next_fit,
            3: self.best_fit,
            4: self.worst_fit
        }
        return strategy_method[self.strategy](size)

    def first_fit(self, size):
        """
        Allocates memory using the First Fit strategy: searches for the first free block that fits the size.
        """
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
        """
        Allocates memory using the Next Fit strategy: starts from the last allocated block's position,
        wraps around if necessary, and allocates the first fitting block.
        """
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
        to_check = []
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
                else:
                    to_check.append(self.free_blocks[i])
        for i, (base, limit) in enumerate(to_check):
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


    def best_fit(self, size):
        """
        Allocates memory using the Best Fit strategy: finds the smallest block that fits the size.
        """
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
        """
        Allocates memory using the Worst Fit strategy: selects the largest available block.
        """
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
        """
        Deletes a process and frees its memory, then merges adjacent free memory blocks.
        """
        if pid in self.processes:
            process = self.processes.pop(pid)
            self.free_blocks.append((process.base, process.limit))
            self.free_blocks = sorted(self.free_blocks, key=lambda x: x[0]) 
            self.merge_free_blocks()
            self.last_allocated = 0
            for i in self.processes:
                self.last_allocated = max(self.last_allocated, i)
            return True
        return False

    def merge_free_blocks(self):
        """
        Merges adjacent or overlapping free memory blocks into a single block.
        """
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
        """
        Converts a virtual address to a physical address for a given process.
        """
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
        """
        Prints a visual representation of the current memory map showing all memory blocks
        (allocated and free) sorted by their base address.
        """
        print("Memory Map:")

        # Create a combined list of all memory blocks, both allocated and free.
        memory_blocks = []

        # Add process blocks to the list
        for pid, process in self.processes.items():
            memory_blocks.append({
                'type': 'Process',
                'pid': pid,
                'base': process.base,
                'limit': process.limit,
                'size': process.size
            })

        # Add free blocks to the list
        for base, limit in self.free_blocks:
            memory_blocks.append({
                'type': 'Free',
                'pid': 'None',
                'base': base,
                'limit': limit,
                'size': limit - base + 1
            })

        # Sort the combined list by base address
        memory_blocks.sort(key=lambda block: block['base'])

        # Print each block in the sorted list
        for block in memory_blocks:
            if block['type'] == 'Process':
                print(
                    f"Process {block['pid']}: Base={block['base']}, Limit={block['limit'] + 1}, Size={block['size']}KB")
            else:
                print(f"Free: Base={block['base']}, Limit={block['limit'] + 1}, Size={block['size']}KB")

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
