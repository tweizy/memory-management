import sys
from app.memory_manager import *

def main():
    if len(sys.argv) != 3:
        print("Usage: python mmu.py <total_memory_in_KB> <strategy_number>")
        print("Strategy Numbers: 1: First Fit, 2: Next Fit, 3: Best Fit, 4: Worst Fit")
        sys.exit(1)

    try:
        total_memory = int(sys.argv[1])
        if total_memory <= 0:
            raise ValueError("Total memory must be a positive integer.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        strategy = int(sys.argv[2])
        if strategy not in [1, 2, 3, 4]:
            raise ValueError("Invalid strategy number. Choose between 1 and 4.")
    except ValueError as e:
        print(f"Error: {e}")
        print("1: First Fit\n2: Next Fit\n3: Best Fit\n4: Worst Fit")
        sys.exit(1)

    mmu = MemoryManager(total_memory, strategy)
    print(f"Initialized MMU with {total_memory} KB using strategy {strategy}")
    print("Memory Management Unit initialized.")
    print("Enter commands to manage memory:")
    print("Commands:")
    print("  cr [AMOUNT] - Create a process requesting [AMOUNT] of memory")
    print("  dl [PROCESS_ID] - Delete the process with [PROCESS_ID]")
    print("  cv [PROCESS_ID] [VIRTUAL_ADDRESS] - Convert virtual address for a process")
    print("  pm - Print the memory map")

    while True:
        command = input("> ").strip().split()
        if not command:
            continue
        cmd_type = command[0]
        if cmd_type == "cr" and len(command) == 2:
            try:
                amount = int(command[1])
                if amount <= 0:
                    raise ValueError("Requested memory amount must be strictly positive.")
                pid, base, limit = mmu.allocate_memory(amount)
                if pid:
                    print(f"Created process {pid} with Base={base} and Limit(size)={limit - base + 1}")
                else:
                    print("Error: Not enough memory")
            except ValueError as e:
                print(f"Error: {e}")
        elif cmd_type == "dl" and len(command) == 2:
            try:
                pid = int(command[1])
                if mmu.delete_process(pid):
                    print("Deleted process successfully")
                else:
                    print("Error: Process not found")
            except ValueError:
                print("Error: Process ID must be an integer.")
        elif cmd_type == "cv" and len(command) == 3:
            try:
                pid = int(command[1])
                virtual_address = int(command[2])
                if virtual_address < 0:
                    raise ValueError("Virtual address must be non-negative.")
                result = mmu.convert_address(pid, virtual_address)
                print(result)
            except ValueError as e:
                print(f"Error: {e}")
        elif cmd_type == "pm":
            mmu.print_memory_map()
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
