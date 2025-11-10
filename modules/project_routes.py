import os
import yaml
import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_path = f'project_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yaml'
    
    # Create a backup
    if os.path.exists(project_yaml_path):
        os.rename(project_yaml_path, backup_path)
        logger.info(f'Backup created at {backup_path}')
    
    # Default configuration
    default_config = {
        "entry_point": "main.py",
        "dependencies": {
            "fastapi": "0.104.1",
            "uvicorn": "0.24.0",
            "pydantic": "2.5.0",
            "sqlalchemy": "2.0.23",
            "pytest": "7.4.3"
        },
        "template_version": "1.0.0"  # Example version, adjust as necessary
    }

    # Write the new config
    try:
        with open(project_yaml_path, 'w') as file:
            yaml.dump(default_config, file)
            logger.info(f'project.yaml created with default settings.')
    except Exception as e:
        logger.error(f'Error writing to project.yaml: {e}')
        # Restore from backup if writing fails
        if os.path.exists(backup_path):
            os.rename(backup_path, project_yaml_path)
            logger.info('Restored project.yaml from backup.')
        raise

    # Validate the created YAML
    try:
        with open(project_yaml_path, 'r') as file:
            content = yaml.safe_load(file)
            if not isinstance(content, dict):
                raise ValueError("YAML content is not valid")
    except Exception as e:
        logger.error(f'Error validating project.yaml: {e}')
        if os.path.exists(backup_path):
            os.rename(backup_path, project_yaml_path)
            logger.info('Restored project.yaml from backup.')
        raise