import subprocess
import sys
import os

def ensure_pipreqs_installed():
    """
    Ensures that pipreqs is installed. Installs it if not present.
    """
    try:
        # Check if pipreqs is installed by trying to get its version
        result = subprocess.run(['pipreqs', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise FileNotFoundError
    except FileNotFoundError:
        # pipreqs is not installed; install it
        print("pipreqs not found. Installing pipreqs...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipreqs"])
            print("pipreqs installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install pipreqs: {e}")
            sys.exit(1)

def generate_requirements(output_file='requirements.txt', ignore_dirs=None):
    """
    Generates a requirements.txt file with external dependencies using pipreqs.
    """
    ensure_pipreqs_installed()
    
    cmd = ['pipreqs', '.', '--force', f'--savepath={output_file}']
    
    if ignore_dirs:
        # pipreqs expects directories to ignore as a comma-separated string
        cmd.extend(['--ignore', ','.join(ignore_dirs)])
    
    try:
        print(f"Generating '{output_file}' using pipreqs...")
        subprocess.check_call(cmd)
        print(f"'{output_file}' has been generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating '{output_file}': {e}")
        sys.exit(1)

def install_missing_packages(requirements_file='requirements.txt'):
    """
    Installs packages listed in the specified requirements file.
    """
    if not os.path.isfile(requirements_file):
        print(f"Error: '{requirements_file}' not found.")
        sys.exit(1)
    
    try:
        # Upgrade pip to the latest version
        print("Upgrading pip to the latest version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install the required packages
        print(f"Installing packages from '{requirements_file}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        
        print(f"All packages from '{requirements_file}' have been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")
        sys.exit(1)

def main():
    # Define the requirements file name
    requirements_file = 'requirements.txt'
    
    # Optional: Define directories to ignore (e.g., tests, migrations)
    ignore_dirs = ['tests', 'migrations']  # Modify as needed
    
    # Step 1: Generate requirements.txt
    generate_requirements(output_file=requirements_file, ignore_dirs=ignore_dirs)
    
    # Step 2: Install missing packages
    install_missing_packages(requirements_file)

if __name__ == "__main__":
    main()
