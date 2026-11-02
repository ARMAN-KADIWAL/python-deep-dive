import datetime


print("=== Timestamp Logging ===")


def log_entry(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("activity_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

    print(f"Logged: [{timestamp}] {message}")


def main():
    log_entry("System startup initiated")
    log_entry("Loading configuration files")
    log_entry("Database connection established")
    log_entry("Web server started on port 8080")
    log_entry("Application ready to serve requests")

    print("\nComplete log file content:")
    with open("activity_log.txt", "r", encoding="utf-8") as log_read:
        print(log_read.read())


if __name__ == "__main__":
    main()
