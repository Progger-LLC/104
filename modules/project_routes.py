import os
import shutil
import yaml
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_yaml_path = f'backup_{int(time.time())}_project.yaml'
    
    # Step 1: Create a timestamped backup of project.yaml
    shutil.copyfile(project_yaml_path, backup_yaml_path)
    logger.info(f'Backup created at {backup_yaml_path}')

    try:
        # Step 2: Load the existing project.yaml
        with open(project_yaml_path, 'r') as file:
            project_config = yaml.safe_load(file)

        # Step 3: Fix YAML syntax errors and add missing fields
        if 'dependencies' not in project_config:
            project_config['dependencies'] = {}
            logger.warning('No dependencies found. Added empty dependencies.')

        # Example of adding sensible defaults
        project_config.setdefault('template_version', '1.0.0')
        project_config.setdefault('project_name', 'My Project')

        # Step 4: Infer template_version from templates.json if available
        if os.path.exists('templates.json'):
            with open('templates.json', 'r') as templates_file:
                templates = json.load(templates_file)
                project_config['template_version'] = templates.get('template_version', project_config['template_version'])

        # Step 5: Write the modified configuration back to project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.dump(project_config, file)
        logger.info('project.yaml has been repaired successfully.')

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copyfile(backup_yaml_path, project_yaml_path)
        logger.error(f'Repair failed. Restored from backup. Error: {e}')
        raise