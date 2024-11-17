import os
import re
import subprocess
import sys

def find_python_files(directory='.'):
    """Recursively find all Python files in a directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports(file_path):
    """Extracts imported libraries from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Regex to find imports
    imports = re.findall(r'^\s*(?:import|from)\s+(\w+)', content, re.MULTILINE)
    return set(imports)


def filter_non_native_libraries(libraries):
    """Filters out native libraries, returns only non-native ones."""
    non_native = set()
    for library in libraries:
        result = subprocess.run(
            [sys.executable, '-c', f'import {library}'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        if result.returncode != 0:
            non_native.add(library)
    return non_native

def install_libraries(libraries):
    """Installs or updates libraries using pip."""
    for library in libraries:
        print(f"Installing/updating {library}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', library])

def pip_update_missing_dependencies():
    python_files = find_python_files()
    all_imports = set()

    for file_path in python_files:
        all_imports.update(extract_imports(file_path))

    non_native_libraries = filter_non_native_libraries(all_imports)

    if non_native_libraries:
        print("Installing missing libraries...")
        install_libraries(non_native_libraries)
        print("Dependencies updated.")
    else:
        print("No libraries missing.")

if __name__ == '__main__':
    pip_update_missing_dependencies()
