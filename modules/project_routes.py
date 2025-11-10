import os
import shutil
import yaml
from datetime import datetime
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair project.yaml configuration issues."""
    project_yaml_path = "project.yaml"
    backup_path = f"project_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"

    # Step 1: Create a backup if project.yaml exists
    if os.path.exists(project_yaml_path):
        shutil.copyfile(project_yaml_path, backup_path)
        logger.info(f"Backup created at {backup_path}")
    else:
        logger.warning("project.yaml does not exist. Creating a new one.")

    # Step 2: Prepare default configuration
    default_config = {
        "entry_point": "main.py",
        "dependencies": {},
        "template_version": "1.0",
        "ports": {
            "http": 8000
        }
    }

    # Step 3: Validate existing project.yaml or create a new one
    try:
        if os.path.exists(project_yaml_path):
            with open(project_yaml_path, 'r') as file:
                config = yaml.safe_load(file) or {}
            # Merge with default config
            config = {**default_config, **config}
        else:
            config = default_config

        # Step 4: Validate and write back the project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.safe_dump(config, file)
        logger.info("project.yaml has been repaired/created successfully.")
    except Exception as e:
        # Restore from backup if there's an error
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, project_yaml_path)
            logger.error("Error occurred while repairing project.yaml. Restored from backup.")
        raise e