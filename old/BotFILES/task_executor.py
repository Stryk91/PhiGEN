#!/usr/bin/env python3
"""
Task Executor Module
Handles different types of task execution for JC Autonomous Worker
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List


class TaskExecutor:
    """Executes various types of development tasks"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(r'E:\PythonProjects\PhiGEN')

    def execute(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution router - determines task type and executes accordingly

        Returns:
            Dict with: success (bool), message (str), files_modified (list), details (dict)
        """
        task_desc = task_details.get('task', '').lower()

        # Check if explicit file lists are provided (highest priority)
        if task_details.get('files_to_create'):
            return self.handle_file_creation(task_details)

        if task_details.get('files_to_modify'):
            return self.handle_file_edit(task_details)

        if task_details.get('files_to_delete'):
            return self.handle_file_deletion(task_details)

        # Determine task type from description
        # Check for file creation BEFORE checking for "test" keyword
        if 'create file' in task_desc or 'new file' in task_desc or 'create' in task_desc and '.' in task_desc:
            return self.handle_file_creation(task_details)

        elif 'edit' in task_desc or 'modify' in task_desc or 'update' in task_desc:
            return self.handle_file_edit(task_details)

        elif 'delete' in task_desc or 'remove' in task_desc:
            return self.handle_file_deletion(task_details)

        elif 'function' in task_desc or 'add' in task_desc:
            return self.handle_code_addition(task_details)

        elif 'run test' in task_desc or 'execute test' in task_desc:
            return self.handle_test_task(task_details)

        else:
            # Generic task - log but don't execute
            return {
                'success': True,
                'message': f'Task acknowledged but requires manual execution: {task_details.get("task")}',
                'files_modified': [],
                'details': {'requires_manual_execution': True}
            }

    def handle_file_creation(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new file based on task description"""
        try:
            # Extract filename from task or details
            files_to_create = task_details.get('files_to_create', [])

            if not files_to_create:
                # Try to parse filename from task description
                task_desc = task_details.get('task', '')
                # Simple regex to find file patterns (e.g., "create example.py")
                file_match = re.search(r'(?:create|add|new)\s+([a-zA-Z0-9_\-\.]+\.[a-z]+)', task_desc, re.IGNORECASE)
                if file_match:
                    files_to_create = [file_match.group(1)]

            if not files_to_create:
                return {
                    'success': False,
                    'message': 'Could not determine which file to create',
                    'files_modified': [],
                    'details': {}
                }

            created_files = []
            for filename in files_to_create:
                file_path = self.project_root / filename

                # Create parent directories if needed
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Create basic template based on file type
                content = self.generate_file_template(filename, task_details)

                file_path.write_text(content, encoding='utf-8')
                created_files.append(str(file_path))

            return {
                'success': True,
                'message': f'Created {len(created_files)} file(s)',
                'files_modified': created_files,
                'details': {'action': 'file_creation'}
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating file: {str(e)}',
                'files_modified': [],
                'details': {'error': str(e)}
            }

    def handle_file_edit(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Edit an existing file"""
        try:
            files_to_modify = task_details.get('files_to_modify', [])

            if not files_to_modify:
                return {
                    'success': False,
                    'message': 'No files specified for modification',
                    'files_modified': [],
                    'details': {}
                }

            modified_files = []
            for filename in files_to_modify:
                file_path = self.project_root / filename

                if not file_path.exists():
                    continue

                # For now, just add a comment indicating JC was here
                # In a full implementation, this would parse requirements and make actual changes
                content = file_path.read_text(encoding='utf-8')

                # Add a JC signature comment at the top
                signature = "# Modified by JC Autonomous Worker\n"
                if not content.startswith(signature):
                    content = signature + content
                    file_path.write_text(content, encoding='utf-8')
                    modified_files.append(str(file_path))

            return {
                'success': True,
                'message': f'Modified {len(modified_files)} file(s)',
                'files_modified': modified_files,
                'details': {'action': 'file_edit', 'note': 'Basic modification applied'}
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error editing file: {str(e)}',
                'files_modified': [],
                'details': {'error': str(e)}
            }

    def handle_file_deletion(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Delete files (with safety checks)"""
        try:
            files_to_delete = task_details.get('files_to_delete', [])

            if not files_to_delete:
                return {
                    'success': False,
                    'message': 'No files specified for deletion',
                    'files_modified': [],
                    'details': {}
                }

            # Safety check: Don't delete critical files
            critical_patterns = ['__init__.py', 'main.py', 'config', '.env']

            deleted_files = []
            for filename in files_to_delete:
                # Safety check
                if any(pattern in filename.lower() for pattern in critical_patterns):
                    continue

                file_path = self.project_root / filename

                if file_path.exists() and file_path.is_file():
                    file_path.unlink()
                    deleted_files.append(str(file_path))

            return {
                'success': True,
                'message': f'Deleted {len(deleted_files)} file(s)',
                'files_modified': deleted_files,
                'details': {'action': 'file_deletion'}
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting file: {str(e)}',
                'files_modified': [],
                'details': {'error': str(e)}
            }

    def handle_code_addition(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Add code to existing files"""
        # This is a placeholder - full implementation would require code parsing
        return {
            'success': True,
            'message': 'Code addition task acknowledged - requires manual implementation',
            'files_modified': [],
            'details': {
                'action': 'code_addition',
                'requires_manual_execution': True,
                'reason': 'Complex code modifications need AI reasoning'
            }
        }

    def handle_test_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Run tests"""
        # This is a placeholder - full implementation would run pytest/unittest
        return {
            'success': True,
            'message': 'Test task acknowledged - requires manual execution',
            'files_modified': [],
            'details': {
                'action': 'test_execution',
                'requires_manual_execution': True,
                'reason': 'Test execution requires environment setup'
            }
        }

    def generate_file_template(self, filename: str, task_details: Dict[str, Any]) -> str:
        """Generate a basic file template based on file extension"""
        ext = Path(filename).suffix.lower()

        if ext == '.py':
            return self.python_template(filename, task_details)
        elif ext == '.md':
            return self.markdown_template(filename, task_details)
        elif ext == '.txt':
            return self.text_template(filename, task_details)
        else:
            return f"# File created by JC Autonomous Worker\n# {task_details.get('task', '')}\n"

    def python_template(self, filename: str, task_details: Dict[str, Any]) -> str:
        """Generate Python file template"""
        task_desc = task_details.get('task', 'No description')

        return f'''#!/usr/bin/env python3
"""
{Path(filename).stem}
Created by JC Autonomous Worker

Task: {task_desc}
"""


def main():
    """Main entry point"""
    pass


if __name__ == '__main__':
    main()
'''

    def markdown_template(self, filename: str, task_details: Dict[str, Any]) -> str:
        """Generate Markdown file template"""
        task_desc = task_details.get('task', 'No description')

        return f'''# {Path(filename).stem}

Created by JC Autonomous Worker

## Task Description

{task_desc}

## Details

*This file was automatically generated.*
'''

    def text_template(self, filename: str, task_details: Dict[str, Any]) -> str:
        """Generate text file template"""
        task_desc = task_details.get('task', 'No description')

        return f'''File: {filename}
Created by JC Autonomous Worker

Task: {task_desc}

---
Auto-generated file
'''
