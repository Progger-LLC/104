import pytest
import os
import shutil
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_temp_yaml(tmp_path):
    """Fixture to set up a temporary project.yaml for testing."""
    yaml_file = tmp_path / "project.yaml"
    yaml_file.write_text("entry_point: old_entry.py")
    yield yaml_file
    os.remove(yaml_file)

def test_repair_project_yaml_creates_file(setup_temp_yaml):
    """Test that repair_project_config creates or repairs project.yaml."""
    repair_project_config()
    assert os.path.exists("project.yaml")
    with open("project.yaml", 'r') as file:
        content = file.read()
    assert "entry_point: old_entry.py" in content  # Should keep existing entry_point
    assert "template_version: 1.0" in content  # Should add default version

def test_backup_creation(setup_temp_yaml):
    """Test that a backup is created before changes are made."""
    repair_project_config()
    assert os.path.exists("project_backup_*.yaml")  # Check for backup creation