# literal_types.py
from typing import Literal, Union

# Define literal types for specific values
Status = Literal["pending", "approved", "rejected"]
Priority = Literal["low", "medium", "high", "critical"]
Environment = Literal["development", "staging", "production"]

def update_task_status(task_id: int, status: Status) -> str:
    """Update task status with only allowed values."""
    valid_statuses = ["pending", "approved", "rejected"]
    
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}")
    
    return f"Task {task_id} status updated to: {status}"

def set_priority(item: str, priority: Priority) -> str:
    """Set priority level for an item."""
    priority_levels = {
        "low": 1,
        "medium": 2, 
        "high": 3,
        "critical": 4
    }
    
    level = priority_levels[priority]
    return f"Item '{item}' set to {priority} priority (level {level})"

def deploy_application(env: Environment, version: str) -> str:
    """Deploy application to specific environment."""
    deployment_configs = {
        "development": "dev-server.local",
        "staging": "staging.company.com",
        "production": "prod.company.com"
    }
    
    server = deployment_configs[env]
    return f"Deploying version {version} to {env} environment at {server}"

# Function with multiple literal parameters
def configure_database(
    db_type: Literal["mysql", "postgresql", "sqlite"],
    mode: Literal["read", "write", "read-write"]
) -> str:
    """Configure database connection."""
    return f"Configuring {db_type} database in {mode} mode"

# Example usage
if __name__ == "__main__":
    # Valid usage
    print(update_task_status(123, "approved"))
    print(set_priority("Bug Fix", "high"))
    print(deploy_application("staging", "v2.1.0"))
    print(configure_database("postgresql", "read-write"))
    
    # These would cause type checker warnings (but still run)
    # print(update_task_status(123, "invalid_status"))  # Type error
    # print(set_priority("Feature", "super_high"))      # Type error
