#!/usr/bin/env python3
"""
update_requirements.py

This script scans the current directory and its subdirectories for Python files,
extracts imported modules, identifies third-party modules (not in the standard library or local modules),
creates or updates a requirements.txt file with these modules and their versions,
and optionally installs the listed packages using pip.

Usage:
    python update_requirements.py            # Generates/updates requirements.txt
    python update_requirements.py --install   # Generates/updates requirements.txt and installs packages
    python update_requirements.py --help      # Displays help message
"""

import os
import sys
import ast
import sysconfig
import importlib.util
import subprocess
import argparse

# Attempt to import importlib.metadata (Python 3.8+), else use the backported importlib_metadata
try:
    import importlib.metadata as metadata
except ImportError:
    try:
        import importlib_metadata as metadata  # type: ignore
    except ImportError:
        metadata = None  # If importlib_metadata is not installed, proceed without version info

# Mapping of module names to package names (for modules where the import name differs from the package name)
MODULE_TO_PACKAGE_MAP = {
    'dotenv': 'python-dotenv',
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'bs4': 'beautifulsoup4',
    'yaml': 'PyYAML',
    'sklearn': 'scikit-learn',
    'torch': 'torch',
    'tensorflow': 'tensorflow',
    'requests': 'requests',
    'langchain_community': 'langchain-community',  # Example mapping; adjust as needed
    'youtube_transcript_api': 'youtube-transcript-api',
    'yt_dlp': 'yt-dlp',
    'hard_chunker': 'hard-chunker',  # Example; adjust based on actual package name
    'get_transcript': 'youtube-transcript-api',  # Assuming 'get_transcript' is from 'youtube-transcript-api'
    # Exclude local modules by setting them to None
    'parsing_utilities': None,
    'invocations': None,
    'interrogate_transcript': None,
    'api_key_manager': None,
    'settings': None,
    # Add other mappings as needed
}

# Set of common built-in modules that may not be correctly identified
COMMON_BUILTIN_MODULES = {
    'typing', 'dataclasses', 'enum', 'pathlib', 'asyncio', 'json',
    're', 'threading', 'ast', 'sys', 'os', 'math', 'time', 'logging',
    'functools', 'itertools', 'collections', 'subprocess', 'socket',
    'queue', 'datetime', 'random', 'http', 'urllib', 'email',
    'hashlib', 'hmac', 'pickle', 'copy', 'inspect', 'traceback',
    'uuid', 'argparse', 'bisect', 'codecs', 'contextlib', 'copyreg',
    'cProfile', 'fractions', 'glob', 'gzip', 'heapq',
    'io', 'ipaddress', 'locale', 'numbers', 'operator', 'pprint',
    'sched', 'shlex', 'statistics', 'string', 'struct', 'tempfile',
    'textwrap', 'trace', 'weakref',
    # Add any other standard modules you need
}

def find_python_files(root_dir):
    """
    Recursively find all .py files starting from root_dir.

    Args:
        root_dir (str): The root directory to start searching from.

    Returns:
        list: A list of paths to .py files.
    """
    python_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories and __pycache__
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                python_files.append(filepath)
    return python_files

def extract_imports_from_file(filepath):
    """
    Extract imported modules from a Python file.

    Args:
        filepath (str): Path to the Python file.

    Returns:
        set: A set of imported module names.
    """
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            node = ast.parse(file.read(), filename=filepath)
    except (SyntaxError, FileNotFoundError, PermissionError) as e:
        print(f"Error parsing {filepath}: {e}", file=sys.stderr)
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

def is_standard_library(module_name):
    """
    Check if a module is part of the standard library.

    Args:
        module_name (str): The name of the module to check.

    Returns:
        bool: True if it's a standard library module, False otherwise.
    """
    if module_name in sys.builtin_module_names:
        print(f"Standard library (built-in): {module_name}")
        return True
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"Module not found (not standard library): {module_name}")
            return False  # Not found; could be third-party
        stdlib_paths = [
            sysconfig.get_paths()['stdlib'],
            sysconfig.get_paths().get('platstdlib', ''),
        ]
        if spec.origin:
            is_std = any(spec.origin.startswith(path) for path in stdlib_paths if path)
            print(f"Module '{module_name}' standard library: {is_std}")
            return is_std
        return False
    except Exception as e:
        print(f"Error checking standard library for '{module_name}': {e}", file=sys.stderr)
        return False

def is_local_module(module_name, project_root):
    """
    Check if a module is a local module within the project.

    Args:
        module_name (str): The name of the module to check.
        project_root (str): The root directory of the project.

    Returns:
        bool: True if it's a local module, False otherwise.
    """
    for root, dirs, files in os.walk(project_root):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        if f"{module_name}.py" in files:
            print(f"Local module detected: {module_name}")
            return True
        if module_name in dirs:
            init_file = os.path.join(root, module_name, '__init__.py')
            if os.path.isfile(init_file):
                print(f"Local package detected: {module_name}")
                return True
    return False

def get_distribution_name_and_version(module_name):
    """
    Get the distribution name and version for a module.

    Args:
        module_name (str): The name of the module.

    Returns:
        tuple: (distribution_name, version) where version can be None if not found.
    """
    # Handle modules that should be skipped or have no corresponding package
    if MODULE_TO_PACKAGE_MAP.get(module_name) is None:
        return None, None

    # Map module name to package name if necessary
    dist_name = MODULE_TO_PACKAGE_MAP.get(module_name, module_name)
    version = None

    if metadata:
        try:
            version = metadata.version(dist_name)
            return dist_name, version
        except metadata.PackageNotFoundError:
            pass

        # If direct lookup failed, search through installed distributions
        try:
            for dist in metadata.distributions():
                # Check if module_name is among the top-level packages provided by the distribution
                try:
                    top_level_modules = dist.read_text('top_level.txt')
                except (FileNotFoundError, AttributeError):
                    top_level_modules = ""
                if top_level_modules:
                    modules = [line.strip() for line in top_level_modules.splitlines()]
                    if module_name in modules:
                        version = dist.version
                        return dist.metadata['Name'], version
        except Exception:
            pass

    # Fallback: Use the distribution name without version
    return dist_name, version

def install_requirements():
    """
    Install packages listed in requirements.txt using pip.
    """
    print("Installing packages from requirements.txt...\n")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("\nAll packages have been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred while installing packages: {e}", file=sys.stderr)
        sys.exit(1)

def update_requirements():
    """
    Update or create the requirements.txt file with third-party dependencies.
    Also, list third-party modules found and those requiring installation.
    """
    project_root = os.path.abspath('.')
    
    # Step 1: Find all Python files
    print("Scanning for Python files...")
    python_files = find_python_files(project_root)
    print(f"Found {len(python_files)} Python files.\n")

    if not python_files:
        print("No Python files found. Exiting.")
        sys.exit(0)

    # Step 2: Extract imports from all Python files
    print("Extracting imported modules...")
    imported_modules = set()
    for filepath in python_files:
        imports = extract_imports_from_file(filepath)
        if imports:
            print(f"{filepath}: {', '.join(sorted(imports))}")
        imported_modules.update(imports)
    print(f"\nTotal unique imported modules found: {len(imported_modules)}\n")

    if not imported_modules:
        print("No imported modules found. Exiting.")
        sys.exit(0)

    # Remove common built-in modules that may not be caught
    imported_modules -= COMMON_BUILTIN_MODULES

    # Step 3: Identify third-party modules
    print("Identifying third-party modules...")
    third_party_modules = set()
    for module_name in sorted(imported_modules):
        if module_name not in MODULE_TO_PACKAGE_MAP:
            # If module is not in the mapping, assume it's local or unknown; skip it
            print(f"Module '{module_name}' is not in MODULE_TO_PACKAGE_MAP. It will be skipped.", file=sys.stderr)
            continue
        if is_standard_library(module_name):
            continue  # Skip standard library modules
        elif is_local_module(module_name, project_root):
            continue  # Skip local modules
        else:
            third_party_modules.add(module_name)
    print(f"Third-party modules identified: {', '.join(sorted(third_party_modules))}\n")

    if not third_party_modules:
        print("No third-party modules identified. No requirements.txt update needed.")
        sys.exit(0)

    # Step 4: Get distribution names and versions, and prepare requirements
    print("Resolving package versions...\n")
    requirements = {}
    third_party_modules_found = []
    third_party_modules_missing = []

    for module_name in sorted(third_party_modules):
        dist_name, version = get_distribution_name_and_version(module_name)
        if dist_name is None:
            print(f"Skipping module '{module_name}' as it is set to be excluded.", file=sys.stderr)
            continue
        if dist_name in requirements:
            continue  # Avoid duplicates
        if version:
            requirements[dist_name] = version
            third_party_modules_found.append(f"{dist_name}=={version}")
            print(f" - {dist_name}=={version}")
        else:
            requirements[dist_name] = None
            third_party_modules_missing.append(dist_name)
            print(f" - {dist_name} (version not found)", file=sys.stderr)
    print()

    # Step 5: Write to requirements.txt
    print("Writing to requirements.txt...")
    try:
        with open('requirements.txt', 'w', encoding='utf-8') as req_file:
            for dist_name, version in sorted(requirements.items()):
                if version:
                    req_file.write(f"{dist_name}=={version}\n")
                else:
                    req_file.write(f"{dist_name}\n")
        print("requirements.txt has been successfully updated.\n")
    except (IOError, PermissionError) as e:
        print(f"Error writing to requirements.txt: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 6: Display Summary
    print("Summary:")
    print(f" - Total Python files scanned: {len(python_files)}")
    print(f" - Total unique imported modules: {len(imported_modules)}")
    print(f" - Third-party packages found: {len(third_party_modules_found)}")
    if third_party_modules_missing:
        print(f" - Third-party packages with unknown versions: {len(third_party_modules_missing)}")
    print()

    # Step 7: List third-party modules
    print("Third-party modules found:")
    for pkg in third_party_modules_found:
        print(pkg)
    if third_party_modules_missing:
        print("\nThird-party modules requiring manual version specification:")
        for pkg in third_party_modules_missing:
            print(pkg)
    print()

def main():
    """
    Main function to handle command-line arguments and execute appropriate actions.
    """
    parser = argparse.ArgumentParser(description="Update requirements.txt with third-party dependencies.")
    parser.add_argument('--install', '-i', action='store_true',
                        help='Install all third-party packages listed in requirements.txt after updating it.')

    args = parser.parse_args()

    update_requirements()

    if args.install:
        install_requirements()

if __name__ == '__main__':
    main()
