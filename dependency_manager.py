# dependency_manager.py
import subprocess
import sys
import pkg_resources

def is_installed(package):
    """
    Checks if a package is installed.

    Args:
        package (str): The package name to check.

    Returns:
        bool: True if installed, False otherwise.
    """
    try:
        pkg_resources.get_distribution(package)
        return True
    except pkg_resources.DistributionNotFound:
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
    
    missing = [pkg.split('==')[0] for pkg in dependencies if not is_installed(pkg.split('==')[0])]
    
    if missing:
        print("Installing missing dependencies...")
        download_dependencies()
    else:
        print("All dependencies are already installed.")
