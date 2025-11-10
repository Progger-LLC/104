import os
import shutil
import time
import yaml
from typing import Optional, Dict

def repair_project_config() -> None:
    """Repair the project.yaml configuration file by creating a backup, fixing syntax errors,
    and adding missing required fields."""
    
    project_file = "project.yaml"
    backup_file = f"{project_file}.{int(time.time())}.bak"
    
    # Step 1: Create a backup
    shutil.copyfile(project_file, backup_file)
    
    try:
        with open(project_file, 'r') as file:
            config = yaml.safe_load(file)
        
        # Step 2: Fix issues and ensure all required fields are present
        if config is None:
            config = {}

        # Step 3: Set default values
        required_fields = {
            'template_version': '1.0.0',  # default value
            'dependencies': {}
        }
        
        # Add missing fields with defaults
        for field, default in required_fields.items():
            if field not in config:
                config[field] = default
        
        # Step 4: Validate dependencies formatting
        if 'dependencies' not in config or not isinstance(config['dependencies'], dict):
            config['dependencies'] = {}
        
        # Step 5: Write the updated config back to the file
        with open(project_file, 'w') as file:
            yaml.dump(config, file)
    
    except Exception as e:
        # Restore from backup if repair fails
        shutil.copyfile(backup_file, project_file)
        raise e