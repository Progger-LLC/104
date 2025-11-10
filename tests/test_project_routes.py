import pytest
import os
import shutil
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Fixture to set up a temporary project.yaml for testing."""
    project_yaml = tmp_path / "project.yaml"
    with open(project_yaml, 'w') as file:
        yaml.dump({'dependencies': {'fastapi': '0.104.1'}}, file)
    yield project_yaml
    os.remove(project_yaml)

def test_repair_project_yaml_valid(setup_project_yaml):
    """Test that repair_project_config fixes a valid project.yaml."""
    # Modifying the file to introduce an error
    with open(setup_project_yaml, 'a') as file:
        file.write("malformed_yaml: [")

    repair_project_config()
    
    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)

    assert 'dependencies' in config
    assert config['template_version'] == "v1.0.0"  # Check for default value

def test_backup_creation(setup_project_yaml):
    """Test that a backup is created before changes."""
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    repair_project_config()
    
    assert os.path.exists(backup_file)
    os.remove(backup_file)