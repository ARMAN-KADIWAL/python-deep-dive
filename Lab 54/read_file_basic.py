print("=== Basic File Reading ===")

file = open("sample.txt", "r", encoding="utf-8")
content = file.read()
print("File contents:")
print(content)
file.close()

print("File reading completed!")
