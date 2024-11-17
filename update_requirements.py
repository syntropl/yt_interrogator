#!/usr/bin/env python3
"""
update_requirements.py

This script scans the current directory and its subdirectories for Python files,
extracts imported modules, identifies third-party modules (not in the standard library or local modules),
and creates or updates a requirements.txt file with these modules and their versions.

After running this script, you can install all required dependencies by executing:
pip install -r requirements.txt
"""

import os
import sys
import ast
import sysconfig
import importlib.util

# Try to import importlib.metadata for Python 3.8+, else set to None
try:
    from importlib import metadata
except ImportError:
    metadata = None

def find_python_files(root_dir):
    """Recursively find all .py files starting from root_dir."""
    python_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip directories like __pycache__
        dirnames[:] = [d for d in dirnames if d != '__pycache__']
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                python_files.append(filepath)
    return python_files

def extract_imports_from_file(filepath):
    """Extract imported modules from a Python file."""
    imports = set()
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            node = ast.parse(file.read(), filename=filepath)
        except SyntaxError as e:
            print(f"Syntax error in {filepath}: {e}", file=sys.stderr)
            return imports
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                module_name = alias.name.split('.')[0]
                if module_name:
                    imports.add(module_name)
        elif isinstance(n, ast.ImportFrom):
            if n.level == 0 and n.module:
                module_name = n.module.split('.')[0]
                if module_name:
                    imports.add(module_name)
    return imports

import importlib.util
import sys

def is_standard_library(module_name):
    """Check if a module is part of the standard library."""
    if module_name in sys.builtin_module_names:
        return True
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False
        module_path = spec.origin
        if module_path is None:
            return True  # Built-in module
        # Standard library modules are typically located in these directories
        std_lib_dir = os.path.dirname(sys.executable)
        return module_path.startswith(std_lib_dir)
    except Exception:
        return False


def is_local_module(module_name, project_root):
    """Check if a module is a local module within the project."""
    for root, dirs, files in os.walk(project_root):
        # Skip directories like __pycache__
        dirs[:] = [d for d in dirs if d != '__pycache__']
        if module_name + '.py' in files:
            return True
        if module_name in dirs and '__init__.py' in os.listdir(os.path.join(root, module_name)):
            return True
    return False

def get_module_version(module_name):
    """Get the version of a module, if possible."""
    if metadata:
        try:
            return metadata.version(module_name)
        except metadata.PackageNotFoundError:
            pass
    # Try to import the module and get __version__
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', None)
        if version is None:
            return None
        else:
            return str(version)
    except ImportError:
        return None

def update_requirements():
    """Function to update requirements.txt."""
    project_root = os.path.abspath('.')
    # Step 1: Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files(project_root)
    print(f"Found {len(python_files)} Python files.")

    # Step 2: Extract imports from all Python files
    print("Extracting imported modules...")
    imported_modules = set()
    for filepath in python_files:
        print(f"Processing file: {filepath}")
        imports = extract_imports_from_file(filepath)
        print(f"Imports found in {filepath}: {imports}")
        imported_modules.update(imports)
    print(f"Total imported modules found: {len(imported_modules)}")
    print(f"Imported modules: {imported_modules}")
    

    # Step 3: Identify third-party modules
    print("Identifying third-party modules...")
    third_party_modules = set()
    for module_name in sorted(imported_modules):
        if is_standard_library(module_name):
            print(f"Module '{module_name}' is a standard library module.")
            continue  # Skip standard library modules
        elif is_local_module(module_name, project_root):
            print(f"Module '{module_name}' is a local module.")
            continue  # Skip local modules
        else:
            print(f"Module '{module_name}' is a third-party module.")
            third_party_modules.add(module_name)
    print(f"Third-party modules: {third_party_modules}")

    # Step 4: Get versions and update requirements.txt
    print("Resolving module versions...")
    requirements = {}
    for module_name in sorted(third_party_modules):
        version = get_module_version(module_name)
        if version:
            requirements[module_name] = version
            print(f"Module '{module_name}' version '{version}'")
        else:
            requirements[module_name] = None
            print(f"Could not determine version for {module_name}", file=sys.stderr)

    # Write to requirements.txt
    print("Updating requirements.txt...")
    with open('requirements.txt', 'w') as req_file:
        for module_name, version in requirements.items():
            if version:
                req_file.write(f"{module_name}=={version}\n")
            else:
                req_file.write(f"{module_name}\n")

    print("requirements.txt has been updated.")

if __name__ == '__main__':
    update_requirements()
