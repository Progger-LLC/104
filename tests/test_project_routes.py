import pytest
import os
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_creates_file():
    """Test that repair_project_config creates project.yaml."""
    if os.path.exists('project.yaml'):
        os.remove('project.yaml')
    
    repair_project_config()

    assert os.path.exists('project.yaml'), "project.yaml should be created"
    
    # Validate the content of project.yaml
    with open('project.yaml', 'r') as file:
        content = yaml.safe_load(file)
        assert "entry_point" in content, "entry_point should be present"
        assert "dependencies" in content, "dependencies should be present"
        assert content["entry_point"] == "main.py", "entry_point should be main.py"

def test_repair_project_config_creates_backup():
    """Test that a backup is created when project.yaml exists."""
    with open('project.yaml', 'w') as file:
        file.write('dummy: value')

    repair_project_config()

    backup_files = [f for f in os.listdir() if f.startswith('project_backup_')]
    assert backup_files, "Backup file should be created"