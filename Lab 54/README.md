# Lab 54: Reading and Writing Files - Basic File I/O

## Objectives
- Open and read text files using Python's built-in file operations.
- Write data to text files using write().
- Append data to existing files without overwriting existing content.
- Use with open() for automatic file closing.
- Build interactive programs that save user input to files.
- Handle common file-operation errors and exceptions.

## Requirements
Python 3.x. Standard library only.

## Programs

| Program | Purpose |
|---|---|
| sample.txt | Sample text file used by the read examples |
| read_file_basic.py | Read an entire text file |
| read_file_lines.py | Read a file line by line |
| write_file_basic.py | Write text and read it back |
| write_multiple_lines.py | Use writelines() and append mode |
| append_file.py | Append log entries without overwriting |
| timestamp_log.py | Append timestamped log entries |
| with_statement.py | Compare manual closing with the with statement |
| error_handling.py | Handle missing files and safe file operations |
| interactive_file.py | Collect information and save/view/add notes |
| file_manager.py | Create, read, append, list, and inspect text files |

## Run the programs

Run these commands from inside the Lab 54 folder:

    python3 read_file_basic.py
    python3 read_file_lines.py
    python3 write_file_basic.py
    python3 write_multiple_lines.py
    python3 append_file.py
    python3 timestamp_log.py
    python3 with_statement.py
    python3 error_handling.py
    python3 interactive_file.py
    python3 file_manager.py

The interactive programs require keyboard input. The scripts create their output files in the current working directory.

## File modes
- r: read mode; the file must exist.
- w: write mode; creates a file or overwrites an existing file.
- a: append mode; adds content to the end of a file.
- x: exclusive creation; fails if the file already exists.

## Important file methods
- read(): read the full file content.
- readline(): read one line.
- readlines(): read all lines into a list.
- write(): write a string.
- writelines(): write an iterable of strings.

## Best practices
- Prefer with open() so files close automatically.
- Specify encoding when working with text files.
- Use the appropriate file mode to avoid accidental overwrites.
- Handle FileNotFoundError and other expected I/O exceptions.
