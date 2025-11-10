import os
import yaml
import shutil
from datetime import datetime
from typing import Dict, Any


def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    yaml_file_path = 'project.yaml'
    backup_file_path = f'project_backup_{datetime.now().strftime("%Y%m%d%H%M%S")}.yaml'
    
    # Step 1: Create a backup of project.yaml
    if os.path.exists(yaml_file_path):
        shutil.copy(yaml_file_path, backup_file_path)

    # Step 2: Attempt to read and fix the YAML file
    try:
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Fix YAML syntax errors and add missing fields
        config.setdefault('template_version', '1.0.0')  # default template version
        config.setdefault('dependencies', {})  # ensure dependencies are present

        # Additional required fields can be added here
        # Example: config.setdefault('name', 'MyProject')

        # Step 4: Save the corrected YAML back to the file
        with open(yaml_file_path, 'w') as file:
            yaml.dump(config, file)

    except Exception as error:
        # Step 5: Restore from backup if repair fails
        if os.path.exists(backup_file_path):
            shutil.copy(backup_file_path, yaml_file_path)
        raise RuntimeError(f"Repair failed: {error}")