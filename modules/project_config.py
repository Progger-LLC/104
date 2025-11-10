import os
import yaml
import shutil
import logging
from datetime import datetime
from modules.project_routes import repair_project_config

logger = logging.getLogger(__name__)

def fix_project_yaml(file_path: str) -> None:
    """Fix configuration issues in project.yaml.

    This function creates a backup of the project.yaml file, checks for 
    required fields, fixes any YAML syntax errors, and ensures that all 
    necessary fields are present.
    
    Args:
        file_path (str): The path to the project.yaml file.

    Raises:
        Exception: If the repair process fails.
    """
    # Step 1: Create a backup
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_path)
    logger.info(f"Backup of {file_path} created at {backup_path}.")
    
    try:
        # Step 2: Repair the project.yaml file
        repair_project_config(file_path)

        # Step 3: Load the modified YAML to check for missing fields
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)

        # Step 4: Add the template_version field if missing
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # Set a sensible default
            logger.info("Added missing 'template_version' field with default value.")

        # Step 5: Write back the updated configuration
        with open(file_path, 'w') as file:
            yaml.dump(config, file)

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copy(backup_path, file_path)
        logger.error("Repair failed, restoring from backup.")
        logger.exception(e)
        raise e