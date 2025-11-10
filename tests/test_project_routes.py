import pytest
import os
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_creates_backup(tmp_path):
    """Test that a backup file is created before changes."""
    # Setup a sample project.yaml file
    project_yaml_path = tmp_path / "project.yaml"
    project_yaml_path.write_text("dependencies:\n  - fastapi\n")

    # Perform the repair
    repair_project_config(str(project_yaml_path))

    # Check that a backup file was created
    backup_files = list(tmp_path.glob("project.yaml.*.bak"))
    assert len(backup_files) == 1

def test_repair_project_config_fix_yaml(tmp_path):
    """Test that the function fixes YAML issues and adds missing fields."""
    project_yaml_path = tmp_path / "project.yaml"
    project_yaml_path.write_text("dependencies: \n  - fastapi\n")

    # Perform the repair
    repair_project_config(str(project_yaml_path))

    # Check the contents of the repaired file
    with open(project_yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    assert 'dependencies' in config
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'  # Default version