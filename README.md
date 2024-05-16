# Memory Management Unit Simulator

## Project Overview

The Memory Management Unit (MMU) Simulator is a command-line application designed to simulate different memory allocation strategies in a controlled environment. This tool allows users to experiment with various memory management techniques, providing insights into how different strategies handle memory allocation and deallocation, which is crucial for understanding performance and efficiency in operating systems.

## Features

- **Multiple Allocation Strategies**: Supports four different memory allocation strategies:
  - **First Fit**: Allocates the first block of memory that is large enough.
  - **Next Fit**: Continues from the last allocation point and allocates the next suitable block.
  - **Best Fit**: Chooses the smallest block that is adequate to minimize wasted space.
  - **Worst Fit**: Allocates the largest available block to potentially leave the largest remaining segment.

- **Interactive Command-Line Interface**: Users can interact with the MMU via a command-line interface (CLI) to allocate and deallocate memory, simulate process requests, and view the current state of memory.

- **Web Application Interface**: A user-friendly web interface that allows visual interaction with memory allocation and deallocation, enhancing understanding through visual aids.

- **Dynamic Memory Operations**: Create, delete, and convert virtual to physical addresses dynamically, with immediate feedback on the state of memory.

- **Visualization of Memory State**: Provides a textual representation of the memory allocation state, helping users visualize how memory is utilized and fragmented over time.

- **Real-time Visualization**: Both the CLI and web interface provide ways to view the state of memory, helping users visualize and understand memory allocation dynamics.


## Installation

The MMU Simulator is a Python-based application, requiring Python 3.x. To set up the project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tweizy/memory-management.git
   cd memory-management
   ```

2. **Install dependencies**:
   ```bash
   pip install flask
   ```

## Usage

To run the MMU Simulator, you need to pass the total memory size (in KB) and the desired allocation strategy when starting the application. Here is how you can run the application from the command line:

```bash
python mmu.py <total_memory_in_KB> <strategy_number>
```

To run the web interface of the project, type in the following command:

```bash
python routes.py
```
Then you can access the web interface at: http://localhost:5000

### Command-Line Arguments:
- `<total_memory_in_KB>`: The total size of the memory to manage (in kilobytes).
- `<strategy_number>`: The number representing the memory allocation strategy:
  - `1`: First Fit
  - `2`: Next Fit
  - `3`: Best Fit
  - `4`: Worst Fit

### Example:

To initialize the memory management unit with 50000 KB of memory using the Best Fit strategy, you would run:

```bash
python mmu.py 50000 3
```

### Commands:
Once the application is running, you can use the following commands within the CLI:
- `cr [AMOUNT]`: Create a process requesting `[AMOUNT]` of memory.
- `dl [PROCESS_ID]`: Delete the process with `[PROCESS_ID]`.
- `cv [PROCESS_ID] [VIRTUAL_ADDRESS]`: Convert a virtual address for a process.
- `pm`: Print the current memory map.

## Documentation

For more detailed information about the implementation and each memory management strategy, refer to the detailed report of the project.
