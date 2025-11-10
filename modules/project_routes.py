import os
import shutil
import yaml
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = "project.yaml"
    backup_path = f"{project_yaml_path}.{int(time.time())}.bak"

    # Step 1: Create a timestamped backup of project.yaml
    shutil.copyfile(project_yaml_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        # Step 2: Load the existing YAML file
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Add missing required fields with sensible defaults
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # default value
            logger.info("Added missing 'template_version' field.")

        # Additional validation and fixing could be added here

        # Step 4: Validate the dependencies format
        if 'dependencies' in config:
            # Ensure dependencies are properly formatted (list or dict)
            if not isinstance(config['dependencies'], dict):
                raise ValueError("Dependencies must be a dictionary.")

        # Step 5: Write the fixed configuration back to project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.safe_dump(config, file)
        logger.info("project.yaml updated successfully.")

    except Exception as e:
        logger.error(f"Error repairing project.yaml: {e}")
        # Step 6: Restore from backup if repair fails
        shutil.copyfile(backup_path, project_yaml_path)
        logger.info("Restored project.yaml from backup.")
    finally:
        # Clean up backup file if not needed
        if os.path.exists(backup_path):
            os.remove(backup_path)