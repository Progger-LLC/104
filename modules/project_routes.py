import os
import yaml
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def repair_project_config(file_path: str) -> None:
    """Repair the project.yaml configuration file.

    This function creates a backup of the project.yaml file, attempts to fix any
    configuration issues, and restores from backup if necessary.

    Args:
        file_path (str): The path to the project.yaml file.
    """
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    try:
        # Step 1: Create a timestamped backup
        os.rename(file_path, backup_path)
        logger.info(f"Backup created at {backup_path}")

        # Step 2: Read and fix the YAML file
        with open(backup_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Fix YAML syntax errors and add missing fields
        if 'dependencies' not in config:
            config['dependencies'] = {}

        # Add sensible defaults for missing fields
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # Example default version

        # Step 4: Infer template_version from templates.json if available
        if os.path.exists('templates.json'):
            with open('templates.json', 'r') as templates_file:
                templates = json.load(templates_file)
                config['template_version'] = templates.get('version', config['template_version'])

        # Step 5: Write the fixed config back to the file
        with open(file_path, 'w') as file:
            yaml.safe_dump(config, file)

        logger.info("project.yaml has been successfully repaired.")

    except Exception as e:
        logger.error(f"Failed to repair project.yaml: {e}")
        # Restore from backup if repair fails
        if os.path.exists(backup_path):
            os.rename(backup_path, file_path)
            logger.info("Restored project.yaml from backup.")