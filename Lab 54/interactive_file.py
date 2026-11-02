print("=== Interactive File Operations ===")
print("This program will collect your input and save it to a file")


def get_user_data():
    print("\nPlease provide the following information:")

    name = input("Enter your name: ").strip()
    age = input("Enter your age: ").strip()
    city = input("Enter your city: ").strip()
    hobby = input("Enter your favorite hobby: ").strip()

    return {
        "name": name,
        "age": age,
        "city": city,
        "hobby": hobby,
    }


def save_to_file(user_data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("=== User Information ===\n")
            file.write(f"Name: {user_data['name']}\n")
            file.write(f"Age: {user_data['age']}\n")
            file.write(f"City: {user_data['city']}\n")
            file.write(f"Favorite Hobby: {user_data['hobby']}\n")
            file.write("=== End of Information ===\n")
        return True
    except OSError as error:
        print(f"Error saving file: {error}")
        return False


def read_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found!"
    except OSError as error:
        return f"Error reading file: {error}"


def main():
    filename = "user_info.txt"

    while True:
        print("\n=== Menu ===")
        print("1. Enter new information")
        print("2. View saved information")
        print("3. Add additional notes")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            user_data = get_user_data()
            if save_to_file(user_data, filename):
                print(f"Information saved successfully to {filename}")
            else:
                print("Failed to save information")

        elif choice == "2":
            print(f"\nContents of {filename}:")
            print("-" * 30)
            print(read_from_file(filename))

        elif choice == "3":
            note = input("Enter additional note: ").strip()
            try:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(f"Additional Note: {note}\n")
                print("Note added successfully")
            except OSError as error:
                print(f"Error adding note: {error}")

        elif choice == "4":
            print("Thank you for using the interactive file program!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
