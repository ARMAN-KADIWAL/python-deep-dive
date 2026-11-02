import os
from datetime import datetime


print("=== File Management Utility ===")


def ensure_text_extension(filename):
    filename = filename.strip()
    if not filename.lower().endswith(".txt"):
        filename += ".txt"
    return filename


def create_file():
    filename = ensure_text_extension(input("Enter filename to create: "))

    print("Enter content (type 'END' on a new line to finish):")
    content_lines = []

    while True:
        line = input()
        if line.upper() == "END":
            break
        content_lines.append(line + "\n")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(content_lines)
        print(f"File '{filename}' created successfully!")
        return filename
    except OSError as error:
        print(f"Error creating file: {error}")
        return None


def read_file():
    filename = ensure_text_extension(input("Enter filename to read: "))

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        print(f"\n=== Contents of {filename} ===")
        print(content)
        print("=== End of File ===")
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
    except OSError as error:
        print(f"Error reading file: {error}")


def append_to_file():
    filename = ensure_text_extension(input("Enter filename to append to: "))

    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist!")
        create_new = input("Would you like to create it? (y/n): ").strip().lower()
        if create_new != "y":
            return

    print("Enter content to append (type 'END' on a new line to finish):")
    content_lines = []

    while True:
        line = input()
        if line.upper() == "END":
            break
        content_lines.append(line + "\n")

    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(
                f"\n--- Appended on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
            )
            file.writelines(content_lines)
        print(f"Content appended to '{filename}' successfully!")
    except OSError as error:
        print(f"Error appending to file: {error}")


def list_files():
    try:
        txt_files = sorted(
            filename for filename in os.listdir(".")
            if filename.lower().endswith(".txt") and os.path.isfile(filename)
        )

        if txt_files:
            print("\nText files in current directory:")
            for index, filename in enumerate(txt_files, 1):
                file_size = os.path.getsize(filename)
                print(f"{index}. {filename} ({file_size} bytes)")
        else:
            print("No text files found in current directory.")
    except OSError as error:
        print(f"Error listing files: {error}")


def file_info():
    filename = ensure_text_extension(input("Enter filename for info: "))

    try:
        if not os.path.isfile(filename):
            print(f"File '{filename}' does not exist!")
            return

        stat = os.stat(filename)
        print(f"\n=== File Information for {filename} ===")
        print(f"Size: {stat.st_size} bytes")
        print(f"Created: {datetime.fromtimestamp(stat.st_ctime)}")
        print(f"Modified: {datetime.fromtimestamp(stat.st_mtime)}")

        line_count = 0
        character_count = 0
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line_count += 1
                character_count += len(line)

        print(f"Lines: {line_count}")
        print(f"Characters: {character_count}")
    except OSError as error:
        print(f"Error getting file info: {error}")


def main_menu():
    while True:
        print("\n=== File Management Utility ===")
        print("1. Create new file")
        print("2. Read file")
        print("3. Append to file")
        print("4. List all text files")
        print("5. File information")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            create_file()
        elif choice == "2":
            read_file()
        elif choice == "3":
            append_to_file()
        elif choice == "4":
            list_files()
        elif choice == "5":
            file_info()
        elif choice == "6":
            print("Thank you for using File Management Utility!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
