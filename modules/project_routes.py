import os
import shutil
import yaml
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repairs the project.yaml configuration issues."""
    project_yaml_path = "project.yaml"
    backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    
    # Step 1: Create a backup of project.yaml
    shutil.copyfile(project_yaml_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        # Step 2: Load and fix YAML
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Fix malformed dependencies and add defaults
        if 'dependencies' not in config:
            config['dependencies'] = {}
        
        # Ensure required fields are present
        required_fields = ['entry_point', 'dependencies', 'template_version']
        for field in required_fields:
            if field not in config:
                config[field] = "default_value" if field != 'template_version' else "v1.0.0"

        # Step 4: Infer template_version from templates.json if available
        if os.path.exists("templates.json"):
            with open("templates.json", 'r') as json_file:
                template_config = json.load(json_file)
                config['template_version'] = template_config.get('version', config['template_version'])

        # Step 5: Save the corrected YAML back to project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.safe_dump(config, file)

        logger.info("Successfully repaired project.yaml.")
        
    except Exception as e:
        logger.error(f"Error repairing project.yaml: {str(e)}")
        # Restore from backup if repair fails
        shutil.copyfile(backup_path, project_yaml_path)
        logger.info(f"Restored project.yaml from backup: {backup_path}")