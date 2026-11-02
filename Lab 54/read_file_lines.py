print("=== Reading File Line by Line ===")

file = open("sample.txt", "r", encoding="utf-8")
line_number = 1

for line in file:
    print(f"Line {line_number}: {line.strip()}")
    line_number += 1

file.close()

print("\nLine-by-line reading completed!")
