import os
import re
from pathlib import Path
from parsing_utilities import serialize_session


def save_interrogation(interrogation_list_of_lists):

    sessions_folder = get_or_create_sessions_folder()
    string_to_save = serialize_session(interrogation_list_of_lists)
    print(string_to_save)
   
    video_title = interrogation_list_of_lists[0][0]['title']
    file_name = generate_file_name(video_title, sessions_folder)
    file_path = os.path.join(sessions_folder, file_name)
    
    print(f"\nSaving as {file_name} in {sessions_folder}...")
    
    try:
        # Step 6: Open the file in write mode and save the serialized string
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(string_to_save)
        print(f"file saved successfully")
    except Exception as e:
        # Handle any exceptions that occur during file operations
        print(f"Failed to save interrogation: {e}")


def sanitize_title(title):
    """
    Sanitize the title to make it safe for use as a filename.
    Removes or replaces characters that are invalid in filenames.
    """
    # Replace spaces with underscores
    sanitized = title.replace(' ', '_')
    # Remove any character that is not alphanumeric, underscore, or hyphen
    sanitized = re.sub(r'[^\w\-]', '', sanitized)
    return sanitized


def generate_file_name(video_title, folder_full_path):
    """
    Generates a unique filename based on the video title.
    If a file with the candidate name exists, appends '_retried' before the extension.
    
    :param metadata_dict: Dictionary containing metadata, must include 'title' key.
    :param folder_full_path: The directory path where the file will be saved.
    :return: A unique filename as a string.
    """

    sanitized_title = sanitize_title(video_title)
    filename_candidate = f"{sanitized_title}.txt"
    full_path = os.path.join(folder_full_path, filename_candidate)
    
    while os.path.exists(full_path):
        name, ext = os.path.splitext(filename_candidate)
        name += "_retried"
        filename_candidate = f"{name}{ext}"
        full_path = os.path.join(folder_full_path, filename_candidate)
    return filename_candidate


from pathlib import Path
import sys

def find_program_root(target_folder_name="yt_interrogator"):
    """
    Traverses upwards from the current script's directory to find the program's root folder.

    :param target_folder_name: Name of the root folder to locate.
    :return: Absolute Path object of the root folder.
    :raises FileNotFoundError: If the root folder is not found in the path hierarchy.
    """
    # Determine the starting path
    try:
        # If the script is being run normally
        current_path = Path(__file__).resolve()
    except NameError:
        # If __file__ is not defined (e.g., interactive environment)
        try:
            current_path = Path(sys.argv[0]).resolve()
        except IndexError:
            # Fallback to current working directory
            current_path = Path.cwd()

    # If the program is frozen (e.g., packaged by PyInstaller)
    if getattr(sys, 'frozen', False):
        current_path = Path(sys.executable).resolve()

    # Traverse upwards to find the target folder
    for parent in current_path.parents:
        if parent.name == target_folder_name:
            return parent

    # If the target folder is not found, raise an error
    raise FileNotFoundError(
        f"Could not find the root folder '{target_folder_name}' in the directory hierarchy."
    )


def get_or_create_sessions_folder(target_folder_name="yt_interrogator", sessions_folder_name="SAVED_SESSIONS"):
    """
    Locates the 'SAVED_SESSIONS' folder within the program's root directory.
    If the folder does not exist, it creates it.

    :param target_folder_name: Name of the root folder to locate (default: "yt_interrogator").
    :param sessions_folder_name: Name of the sessions folder to check/create (default: "SAVED_SESSIONS").
    :return: Absolute Path object of the 'SAVED_SESSIONS' folder.
    :raises FileNotFoundError: If the root folder is not found.
    :raises PermissionError: If the folder cannot be created due to permission issues.
    """
    try:
        root_path = find_program_root(target_folder_name)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit the program or handle as needed

    sessions_path = root_path / sessions_folder_name

    if not sessions_path.exists():
        try:
            # Create the 'SAVED_SESSIONS' folder
            sessions_path.mkdir(parents=True, exist_ok=True)
            return sessions_path
        except PermissionError as e:
            print(f"Permission Error: Cannot create folder '{sessions_path}'. {e}")
            sys.exit(1)  # Exit the program or handle as needed
        except Exception as e:
            print(f"An unexpected error occurred while creating '{sessions_path}': {e}")
            sys.exit(1)  # Exit the program or handle as needed
    else:
        return sessions_path