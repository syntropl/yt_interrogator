# main.py
import sys
import os
from dependency_manager import ensure_dependencies

def main():
    """
    Entry point of the application. Ensures dependencies are installed and runs the main program.
    """
    # Ensure dependencies are installed
    ensure_dependencies()
    
    # Execute the main program
    try:
        import program
        program.run()  # Assuming you have a run() function in program.py
    except Exception as e:
        print(f"Failed to run the program: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
