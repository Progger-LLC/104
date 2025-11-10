import os
import pytest
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_creates_backup():
    """Test that repair_project_config creates a backup of project.yaml."""
    # Setup: Create a sample project.yaml file
    original_yaml = """
    dependencies:
      fastapi: 0.104.1
    """
    with open("project.yaml", "w") as f:
        f.write(original_yaml)

    # Execute: Call the repair function
    repair_project_config()

    # Verify: Ensure backup exists
    assert os.path.exists("project.yaml.bak.")

    # Cleanup
    os.remove("project.yaml")
    os.remove("project.yaml.bak.")

def test_repair_project_config_adds_template_version():
    """Test that repair_project_config adds template_version when missing."""
    # Setup: Create a sample project.yaml without template_version
    original_yaml = """
    dependencies:
      fastapi: 0.104.1
    """
    with open("project.yaml", "w") as f:
        f.write(original_yaml)

    # Execute: Call the repair function
    repair_project_config()

    # Verify: Ensure template_version is added
    with open("project.yaml", "r") as f:
        config = yaml.safe_load(f)
        assert "template_version" in config

    # Cleanup
    os.remove("project.yaml")

def test_repair_project_config_valid_yaml():
    """Test that project.yaml remains valid YAML after repair."""
    # Setup: Create a sample project.yaml with invalid structure
    original_yaml = """
    dependencies:
      fastapi: 0.104.1
    """
    with open("project.yaml", "w") as f:
        f.write(original_yaml)

    # Execute: Call the repair function
    repair_project_config()

    # Verify: Ensure the YAML is valid
    with open("project.yaml", "r") as f:
        config = yaml.safe_load(f)
        assert isinstance(config, dict)

    # Cleanup
    os.remove("project.yaml")