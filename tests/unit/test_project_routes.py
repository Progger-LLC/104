import pytest
import os
import shutil
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmpdir):
    """Set up a temporary project.yaml for testing."""
    project_yaml = tmpdir.join("project.yaml")
    project_yaml.write(yaml.dump({"dependencies": {"fastapi": "0.104.1"}}))
    return str(project_yaml)

def test_repair_project_config(setup_project_yaml):
    """Test the repair_project_config function."""
    original_yaml = setup_project_yaml

    # Simulate the repair process
    repair_project_config()

    # Load the repaired YAML
    with open(original_yaml, 'r') as file:
        config = yaml.safe_load(file)

    # Check if template_version was added
    assert 'template_version' in config
    assert config['template_version'] == "1.0.0"
    assert isinstance(config['dependencies'], dict)

def test_invalid_dependencies_format(setup_project_yaml):
    """Test handling of invalid dependencies format."""
    original_yaml = setup_project_yaml

    # Write invalid dependencies format
    with open(original_yaml, 'w') as file:
        file.write(yaml.dump({"dependencies": ["fastapi", "uvicorn"]}))

    # Run repair and expect it to restore from backup
    repair_project_config()

    # Load the repaired YAML
    with open(original_yaml, 'r') as file:
        config = yaml.safe_load(file)

    # Check if it restored the original format
    assert 'template_version' not in config