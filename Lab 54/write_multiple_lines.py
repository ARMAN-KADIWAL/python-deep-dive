print("=== Writing Multiple Lines ===")

lines_to_write = [
    "First line of data\n",
    "Second line of data\n",
    "Third line of data\n",
    "Fourth line of data\n",
]

file = open("multiple_lines.txt", "w", encoding="utf-8")
file.writelines(lines_to_write)
file.close()

print("Multiple lines written using writelines()")

additional_data = [
    "Line 5: Additional data\n",
    "Line 6: More data\n",
]

file = open("multiple_lines.txt", "a", encoding="utf-8")
for line in additional_data:
    file.write(line)
file.close()

print("Additional lines appended using write() in loop")

print("\nFinal file content:")
file = open("multiple_lines.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()
