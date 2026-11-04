#!/usr/bin/env python3
"""Create, parse, search, and safely access nested JSON data."""

import json


COMPLEX_DATA = {
    "api_response": {
        "status": "success",
        "timestamp": "2024-01-15T10:30:00Z",
        "data": {
            "users": [
                {
                    "id": 1,
                    "profile": {
                        "name": "Alice Johnson",
                        "email": "alice@example.com",
                        "preferences": {
                            "theme": "dark",
                            "notifications": {"email": True, "push": False, "sms": True},
                        },
                    },
                    "activity": {
                        "last_login": "2024-01-14T15:22:00Z",
                        "sessions": [
                            {"date": "2024-01-14", "duration": 45},
                            {"date": "2024-01-13", "duration": 32},
                            {"date": "2024-01-12", "duration": 67},
                        ],
                    },
                },
                {
                    "id": 2,
                    "profile": {
                        "name": "Bob Smith",
                        "email": "bob@example.com",
                        "preferences": {
                            "theme": "light",
                            "notifications": {"email": False, "push": True, "sms": False},
                        },
                    },
                    "activity": {
                        "last_login": "2024-01-15T09:15:00Z",
                        "sessions": [
                            {"date": "2024-01-15", "duration": 28},
                            {"date": "2024-01-14", "duration": 55},
                        ],
                    },
                },
            ],
            "metadata": {
                "total_users": 2,
                "active_users": 2,
                "server_info": {"version": "1.2.3", "region": "us-west-2", "load": 0.65},
            },
        },
    }
}


def create_complex_json_file(filename="complex_api_response.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(COMPLEX_DATA, file, indent=4)
    print(f"Complex JSON file created: {filename}")


def parse_nested_data(filename="complex_api_response.json"):
    print("\n=== Parsing Nested JSON Data ===")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        api_response = data["api_response"]
        print(f"API Status: {api_response['status']}")
        print(f"Timestamp: {api_response['timestamp']}")
        users_data = api_response["data"]["users"]
        print(f"\nTotal users in response: {len(users_data)}")
        for user in users_data:
            print(f"\n--- User ID: {user['id']} ---")
            profile = user["profile"]
            print(f"Name: {profile['name']}")
            print(f"Email: {profile['email']}")
            print(f"Theme: {profile['preferences']['theme']}")
            print("Notification Preferences:")
            for notification_type, enabled in profile["preferences"]["notifications"].items():
                status = "Enabled" if enabled else "Disabled"
                print(f"  {notification_type.capitalize()}: {status}")
            activity = user["activity"]
            print(f"Last Login: {activity['last_login']}")
            print(f"Total Sessions: {len(activity['sessions'])}")
            total_duration = sum(session["duration"] for session in activity["sessions"])
            print(f"Total Session Time: {total_duration} minutes")
        metadata = api_response["data"]["metadata"]
        print("\n--- Metadata ---")
        print(f"Total Users: {metadata['total_users']}")
        print(f"Active Users: {metadata['active_users']}")
        server_info = metadata["server_info"]
        print(f"Server Version: {server_info['version']}")
        print(f"Server Region: {server_info['region']}")
        print(f"Server Load: {server_info['load']:.2%}")
        return data
    except FileNotFoundError:
        print(f"Error: {filename} file not found!")
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Error parsing nested JSON: {error}")
    return None


def safe_json_access(filename="complex_api_response.json"):
    print("\n=== Safe JSON Data Access ===")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        api_response = data.get("api_response", {})
        print(f"API Status (safe): {api_response.get('status', 'unknown')}")
        users = api_response.get("data", {}).get("users", [])
        print(f"Number of users (safe): {len(users)}")
        if users:
            first_user = users[0]
            email_notifications = (
                first_user.get("profile", {})
                .get("preferences", {})
                .get("notifications", {})
                .get("email", False)
            )
            print(f"First user email notifications (safe): {email_notifications}")
        try:
            server_load = data["api_response"]["data"]["metadata"]["server_info"]["load"]
            print(f"Server load (direct access): {server_load:.2%}")
        except KeyError as error:
            print(f"Key not found: {error}")
        return data
    except (OSError, json.JSONDecodeError, AttributeError) as error:
        print(f"Error in safe JSON access: {error}")
        return None


def search_json_data(filename="complex_api_response.json"):
    print("\n=== Searching JSON Data ===")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        users = data["api_response"]["data"]["users"]
        dark_theme_users = [
            user["profile"]["name"]
            for user in users
            if user.get("profile", {}).get("preferences", {}).get("theme") == "dark"
        ]
        print(f"Users with dark theme: {dark_theme_users}")
        email_enabled_users = [
            user["profile"]["name"]
            for user in users
            if user.get("profile", {}).get("preferences", {}).get("notifications", {}).get("email", False)
        ]
        print(f"Users with email notifications: {email_enabled_users}")
        high_activity_users = []
        for user in users:
            sessions = user.get("activity", {}).get("sessions", [])
            total_time = sum(session.get("duration", 0) for session in sessions)
            if total_time > 60:
                high_activity_users.append({"name": user["profile"]["name"], "total_time": total_time})
        print("High activity users (>60 minutes):")
        for user in high_activity_users:
            print(f"  {user['name']}: {user['total_time']} minutes")
        return {
            "dark_theme_users": dark_theme_users,
            "email_enabled_users": email_enabled_users,
            "high_activity_users": high_activity_users,
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Error searching JSON data: {error}")
        return None


if __name__ == "__main__":
    create_complex_json_file()
    parse_nested_data()
    safe_json_access()
    search_json_data()
