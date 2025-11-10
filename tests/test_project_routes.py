import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_yaml_file(tmpdir):
    """Fixture to setup a test project.yaml file."""
    test_yaml_path = tmpdir.join("project.yaml")
    with open(test_yaml_path, 'w') as file:
        yaml.dump({"project_name": "Test Project"}, file)
    return str(test_yaml_path)

def test_repair_project_config(setup_yaml_file):
    """Test the repair_project_config function."""
    # Arrange
    orig_yaml_path = setup_yaml_file
    os.rename(orig_yaml_path, 'project.yaml')

    # Act
    repair_project_config()

    # Assert
    with open('project.yaml', 'r') as file:
        data = yaml.safe_load(file)
        assert data['project_name'] == "Test Project"
        assert 'dependencies' in data
        assert 'template_version' in data