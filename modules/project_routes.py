import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any

def repair_project_config() -> None:
    """Repair the project configuration by fixing YAML syntax and adding missing fields."""
    project_config_path = "project.yaml"
    backup_path = f"project_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml"
    
    # Create a backup of the original configuration if it exists
    if os.path.exists(project_config_path):
        shutil.copyfile(project_config_path, backup_path)

    # Default configuration
    default_config: Dict[str, Any] = {
        'entry_point': 'main.py',
        'dependencies': {},
        'template_version': '1.0.0',  # Default template version
        'name': 'project_name',
        'version': '0.1.0',
    }

    # Try to read the existing configuration
    try:
        with open(project_config_path, 'r') as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError:
        config = {}

    # Merge defaults with existing configuration
    config = {**default_config, **config}

    # Write the fixed configuration back to project.yaml
    with open(project_config_path, 'w') as file:
        yaml.dump(config, file)

    print("Configuration repaired and saved.")