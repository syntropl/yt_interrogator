# dependency_manager.py
import subprocess
import sys


from importlib.metadata import distributions, PackageNotFoundError

def is_installed(package):
    """
    Checks if a package is installed.

    Args:
        package (str): The package name to check.

    Returns:
        bool: True if installed, False otherwise.
    """
    try:
        # Normalize package name to lowercase as per PEP 503
        package_normalized = package.lower()
        for dist in distributions():
            if dist.metadata["Name"].lower() == package_normalized:
                return True
        return False
    except Exception as e:
        print(f"Error checking if package '{package}' is installed: {e}")
        return False

def download_dependencies(requirements_file='requirements.txt'):
    """
    Installs dependencies listed in the requirements file.

    Args:
        requirements_file (str): Path to the requirements file.
    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        print("All dependencies have been installed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
        sys.exit(1)

def ensure_dependencies():
    """
    Ensures that all dependencies are installed. If not, installs them.
    """
    try:
        with open('requirements.txt', 'r') as f:
            dependencies = f.read().splitlines()
    except FileNotFoundError:
        print("requirements.txt not found. Please run update_requirements.py first.")
        sys.exit(1)
    
    missing = []
    for pkg in dependencies:
        # Handle version specifiers, e.g., 'requests==2.25.1'
        pkg_name = pkg.split('==')[0].split('>=')[0].split('<=')[0].strip()
        if not is_installed(pkg_name):
            missing.append(pkg)
    
    if len(missing)>0:
        print("Installing missing dependencies...")
        download_dependencies()
    else:
        print("All requirements satisfied.")
