"""Generate the final Lab 59 database report (Task 5.4)."""

import argparse
from pathlib import Path
from user_management import UserManager


def generate_report(manager):
    """Return a readable summary generated from live SQL aggregation queries."""
    with manager.connection() as conn:
        count, min_age, max_age, avg_age = conn.execute(
            "SELECT COUNT(*), MIN(age), MAX(age), AVG(age) FROM users"
        ).fetchone()
        cities = conn.execute(
            "SELECT city, COUNT(*) FROM users GROUP BY city ORDER BY COUNT(*) DESC, city"
        ).fetchall()
        recent = conn.execute(
            "SELECT user_id, username, created_date FROM users "
            "ORDER BY created_date DESC, user_id DESC LIMIT 5"
        ).fetchall()
    lines = ["LAB 59 - USER DATABASE REPORT", "=" * 40,
             f"Total registered users: {count}"]
    if count:
        lines.extend([f"Age range: {min_age}-{max_age}",
                      f"Average age: {avg_age:.1f}"])
    else:
        lines.append("Age statistics: no registered users")
    lines.append("\nUsers per city:")
    lines.extend(f"  {city}: {total}" for city, total in cities)
    if not cities:
        lines.append("  (none)")
    lines.append("\nFive most recently created users:")
    lines.extend(f"  #{user_id} {username} - {date}" for user_id, username, date in recent)
    if not recent:
        lines.append("  (none)")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Lab 59 SQLite report")
    parser.add_argument("--output", default=None,
                        help="Optional file path for saving the report")
    args = parser.parse_args()
    report = generate_report(UserManager())
    print(report, end="")
    if args.output:
        output = Path(args.output)
        output.write_text(report, encoding="utf-8")
        print(f"Saved report to {output}")
