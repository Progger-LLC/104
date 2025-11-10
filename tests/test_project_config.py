import os
import pytest
import shutil
from modules.project_config import fix_project_yaml

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Setup a temporary project.yaml file for testing."""
    yaml_content = """
    dependencies:
      - fastapi
      - pydantic
    """
    yaml_file = tmp_path / "project.yaml"
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    return yaml_file

def test_fix_project_yaml(setup_yaml_file):
    """Test the fix_project_yaml function."""
    original_file = setup_yaml_file
    fix_project_yaml(original_file)

    # Check if the template_version field is added
    with open(original_file, 'r') as f:
        content = f.read()
        assert 'template_version: 1.0.0' in content

    # Check if backup is created
    backup_file = f"{original_file}.bak"
    assert os.path.exists(backup_file)

    # Clean up
    os.remove(backup_file)