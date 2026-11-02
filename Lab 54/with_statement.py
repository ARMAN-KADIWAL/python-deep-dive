print("=== Using 'with' Statement for File Handling ===")

print("Traditional approach:")
file = open("traditional.txt", "w", encoding="utf-8")
file.write("This file was created using traditional method\n")
file.write("Remember to always close the file manually\n")
file.close()
print("File created and closed manually")

print("\nUsing 'with' statement:")
with open("with_method.txt", "w", encoding="utf-8") as file:
    file.write("This file was created using 'with' statement\n")
    file.write("File will be automatically closed\n")
    file.write("Even if an error occurs!\n")

print("File created and automatically closed")

print("\nReading files using 'with' statement:")
with open("with_method.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print("Content read:")
    print(content)

print("Demonstration completed!")
