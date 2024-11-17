# update_requirements.py
import pkg_resources

def update_requirements():
    # Get the list of installed packages in the current environment
    installed_packages = pkg_resources.working_set
    with open('requirements.txt', 'w') as f:
        for pkg in installed_packages:
            f.write(f"{pkg.project_name}=={pkg.version}\n")
    print("requirements.txt has been updated.")

if __name__ == "__main__":
    update_requirements()
