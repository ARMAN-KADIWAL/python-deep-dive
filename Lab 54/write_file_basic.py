print("=== Basic File Writing ===")

file = open("output.txt", "w", encoding="utf-8")
file.write("This is our first line of written content.\n")
file.write("This is the second line.\n")
file.write("Python file writing is straightforward!\n")
file.close()

print("Content written to 'output.txt'")

print("\nReading back the written content:")
file = open("output.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()
