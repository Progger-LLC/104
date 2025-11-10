import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Set up a temporary project.yaml for testing."""
    project_yaml_path = tmp_path / "project.yaml"
    with open(project_yaml_path, 'w') as f:
        yaml.dump({'dependencies': {'fastapi': '0.68.0'}}, f)
    return project_yaml_path

def test_repair_project_config_valid_yaml(setup_project_yaml):
    """Test that repair_project_config adds missing fields correctly."""
    repair_project_config()
    
    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)
    
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'
    assert isinstance(config['dependencies'], dict)

def test_repair_project_config_backup_created(setup_project_yaml):
    """Test that backup file is created before changes."""
    initial_backup_count = len(list(setup_project_yaml.parent.glob("*.bak")))
    
    repair_project_config()
    
    new_backup_count = len(list(setup_project_yaml.parent.glob("*.bak")))
    assert new_backup_count == initial_backup_count + 1