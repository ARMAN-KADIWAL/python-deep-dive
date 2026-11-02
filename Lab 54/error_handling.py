print("=== Error Handling with 'with' Statement ===")

print("Example 1: Attempting to read non-existent file")

try:
    with open("nonexistent_file.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("Error: File not found!")
    print("Creating the file now...")
    with open("nonexistent_file.txt", "w", encoding="utf-8") as file:
        file.write("This file was created after handling the error\n")
    print("File created successfully")

print("\nExample 2: Safe file operations")

try:
    with open("safe_operations.txt", "w", encoding="utf-8") as file:
        file.write("Starting safe file operations\n")
        file.write("Writing multiple lines safely\n")
        for i in range(5):
            file.write(f"Processing item {i + 1}\n")
        file.write("All operations completed successfully\n")

    print("Safe operations completed")

    with open("safe_operations.txt", "r", encoding="utf-8") as file:
        print("\nFile contents:")
        print(file.read())

except OSError as error:
    print(f"An error occurred: {error}")

print("Error handling demonstration completed!")
