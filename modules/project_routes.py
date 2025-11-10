import os
import yaml
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_path = create_backup(project_yaml_path)
    
    try:
        with open(project_yaml_path, 'r') as file:
            project_config = yaml.safe_load(file) or {}

        # Fixing required fields
        if 'template_version' not in project_config:
            project_config['template_version'] = infer_template_version()

        # Validate and fix syntax errors
        validate_dependencies(project_config)

        # Write back the updated configuration
        with open(project_yaml_path, 'w') as file:
            yaml.dump(project_config, file)

    except Exception as e:
        logger.error(f"Failed to repair project.yaml: {e}. Restoring backup.")
        restore_backup(backup_path, project_yaml_path)
        raise

def create_backup(file_path: str) -> str:
    """Create a timestamped backup of the specified file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{file_path}.{timestamp}.bak"
    os.rename(file_path, backup_path)
    logger.info(f"Backup created: {backup_path}")
    return backup_path

def restore_backup(backup_path: str, original_path: str) -> None:
    """Restore the original file from backup."""
    os.rename(backup_path, original_path)
    logger.info(f"Restored backup from {backup_path} to {original_path}")

def infer_template_version() -> str:
    """Infer the template version from templates.json if available."""
    try:
        with open('templates.json', 'r') as file:
            templates = json.load(file)
            return templates.get('default_template_version', '1.0.0')  # Default version
    except FileNotFoundError:
        logger.warning("templates.json not found, using default version.")
        return '1.0.0'  # Default version if file is not found

def validate_dependencies(config: Dict[str, Any]) -> None:
    """Validate dependencies format in the project configuration."""
    if 'dependencies' in config and not isinstance(config['dependencies'], dict):
        logger.error("Dependencies must be formatted as a dictionary.")
        raise ValueError("Invalid format for dependencies.")