import pytest
import os
import yaml
from modules.project_routes import repair_project_config


@pytest.fixture
def setup_yaml_file(tmpdir):
    """Fixture to set up a temporary project.yaml file for testing."""
    yaml_content = """
    dependencies:
      fastapi: "0.68.0"
    """
    yaml_file = tmpdir.join("project.yaml")
    yaml_file.write(yaml_content)
    yield str(yaml_file)


def test_repair_project_config_valid_yaml(setup_yaml_file):
    """Test the repair_project_config function with valid YAML."""
    os.chdir(os.path.dirname(setup_yaml_file))
    repair_project_config()

    with open('project.yaml', 'r') as file:
        config = yaml.safe_load(file)

    assert config['template_version'] == '1.0.0'
    assert 'dependencies' in config


def test_repair_project_config_missing_file():
    """Test the repair_project_config function when project.yaml is missing."""
    if os.path.exists('project.yaml'):
        os.remove('project.yaml')

    repair_project_config()  # This should create a new project.yaml with defaults

    with open('project.yaml', 'r') as file:
        config = yaml.safe_load(file)

    assert config['template_version'] == '1.0.0'
    assert 'dependencies' in config