import os
import yaml
import datetime
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair project.yaml configuration issues by validating and fixing the configuration."""
    
    config_file = "project.yaml"
    backup_file = create_backup(config_file)

    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        # Ensure all required fields are present
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # Default version could be different

        # Here we can add more checks for the required fields
        if 'dependencies' not in config:
            config['dependencies'] = {}

        # Validate and fix dependencies format
        if not isinstance(config['dependencies'], dict):
            logger.error("Dependencies should be a dictionary.")
            raise ValueError("Invalid dependencies format.")

        # Write the fixed config back to project.yaml
        with open(config_file, 'w') as file:
            yaml.dump(config, file)

        logger.info(f"Successfully repaired {config_file}.")
    
    except Exception as e:
        logger.error(f"Repair failed: {e}. Restoring from backup.")
        restore_backup(backup_file, config_file)
        raise e

def create_backup(file_path: str) -> str:
    """Create a timestamped backup of the given file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{file_path}.{timestamp}.bak"
    os.rename(file_path, backup_file)
    logger.info(f"Backup created: {backup_file}")
    return backup_file

def restore_backup(backup_file: str, original_file: str) -> None:
    """Restore the original file from backup."""
    if os.path.exists(backup_file):
        os.rename(backup_file, original_file)
        logger.info(f"Restored {original_file} from {backup_file}.")
    else:
        logger.error(f"Backup file {backup_file} does not exist.")