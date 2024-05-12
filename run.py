from app.mmu import *

if __name__ == "__main__":
    print("Welcome to the Memory Management Unit Simulator")
    total_memory = int(input("Enter the total memory (KB): "))
    print("Select the memory allocation strategy:")
    print("1: First Fit\n2: Next Fit\n3: Best Fit\n4: Worst Fit")
    strategy = int(input("Enter the strategy number (1-4): "))
    mmu = MemoryManager(total_memory, strategy)

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
            pid, base, limit = mmu.allocate_memory(int(command[1]))
            if pid:
                print(f"Created process {pid} with Base={base} and Limit={limit - base}")
            else:
                print("Error: Not enough memory")
        elif cmd_type == "dl" and len(command) == 2:
            if mmu.delete_process(int(command[1])):
                print("Deleted process successfully")
            else:
                print("Error: Process not found")
        elif cmd_type == "cv" and len(command) == 3:
            pid = int(command[1])
            virtual_address = int(command[2])
            result = mmu.convert_address(pid, virtual_address)
            print(result)
        elif cmd_type == "pm":
            mmu.print_memory_map()
        else:
            print("Invalid command")