import os
import shutil
import yaml
from datetime import datetime
from typing import Any, Dict, Optional

def repair_project_config() -> None:
    """Repair the project.yaml configuration file.

    This function will create a backup of the project.yaml file, fix 
    any issues with the YAML syntax, add missing fields, and restore 
    from backup if repairs fail.
    """
    project_yaml_path = "project.yaml"
    backup_path = f"project.yaml.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Step 1: Create a backup of project.yaml
    shutil.copyfile(project_yaml_path, backup_path)

    try:
        # Step 2: Load the YAML file
        with open(project_yaml_path, 'r') as f:
            config: Dict[str, Any] = yaml.safe_load(f) or {}

        # Step 3: Fix issues and add required fields
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # Default version

        # Validate and reformat dependencies
        if 'dependencies' in config and isinstance(config['dependencies'], dict):
            config['dependencies'] = {k: str(v) for k, v in config['dependencies'].items()}

        # Step 4: Write the updated config back to the YAML file
        with open(project_yaml_path, 'w') as f:
            yaml.dump(config, f)

    except Exception as e:
        # Step 5: Restore from backup if repair fails
        shutil.copyfile(backup_path, project_yaml_path)
        raise e  # Raise the original exception

    finally:
        # Cleanup backup file
        if os.path.exists(backup_path):
            os.remove(backup_path)