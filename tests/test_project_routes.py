import os
import pytest
from modules.project_routes import repair_project_config

def test_repair_project_config_creates_backup():
    """Test that repairing the project config creates a backup."""
    # Create a dummy project.yaml for testing
    test_yaml_path = "project.yaml"
    with open(test_yaml_path, 'w') as file:
        file.write("name: test_project\n")

    # Call the repair function
    repair_project_config()

    # Check for backup file
    backup_file = [f for f in os.listdir() if f.startswith('project_backup_')]
    assert len(backup_file) == 1  # Ensure a single backup file is created

    # Cleanup
    os.remove(test_yaml_path)
    os.remove(backup_file[0])

def test_repair_project_config_creates_default_yaml():
    """Test that default values are set in project.yaml."""
    test_yaml_path = "project.yaml"

    # Call the repair function
    repair_project_config()

    # Check if the project.yaml is created with defaults
    with open(test_yaml_path, 'r') as file:
        content = file.read()
    
    assert "entry_point: main.py" in content
    assert "name: project_name" in content
    assert "version: 0.1.0" in content

    # Cleanup
    os.remove(test_yaml_path)