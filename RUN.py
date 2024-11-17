# main.py
import subprocess
import sys
import os

def list_dependencies():
    """List all dependencies from requirements.txt"""
    try:
        with open('requirements.txt', 'r') as f:
            dependencies = f.read().splitlines()
        return dependencies
    except FileNotFoundError:
        print("requirements.txt not found. Please ensure it exists.")
        sys.exit(1)

def is_installed(dependencies):
    """Check if all dependencies are installed"""
    try:
        import pkg_resources
        pkg_resources.working_set.resolve(pkg_resources.parse_requirements(dependencies))
        return True
    except pkg_resources.DistributionNotFound as e:
        print(f"Missing package: {e}")
        return False
    except pkg_resources.VersionConflict as e:
        print(f"Version conflict: {e}")
        return False

def install_dependencies():
    """Install dependencies using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

def run_program():
    """Run the main program.py"""
    try:
        subprocess.check_call([sys.executable, "program.py"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to run program.py: {e}")
        sys.exit(1)

def main():
    dependencies = list_dependencies()
    if not is_installed(dependencies):
        print("Installing dependencies...")
        install_dependencies()
    else:
        print("All dependencies are already installed.")
    run_program()

if __name__ == "__main__":
    main()
