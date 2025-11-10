import pytest
import os
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Setup a temporary project.yaml for testing."""
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies: { package_a: '1.0.0' }\n")
    return project_yaml

def test_repair_project_config(setup_project_yaml):
    """Test the repair_project_config function."""
    os.chdir(setup_project_yaml.parent)
    
    # Run the repair function
    repair_project_config()
    
    # Check if the template_version is added
    with open(setup_project_yaml.name, 'r') as file:
        data = file.read()
    assert "template_version: '1.0.0'" in data  # Check for default version
    assert "dependencies:" in data  # Ensure dependencies are intact