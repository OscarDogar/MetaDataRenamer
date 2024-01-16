import os
from menu import mainMenu
from decouple import config
from utils import create_env_file
from metaDataChanges import remove_attachment_by_name, replace_track_names


def process_directory(directory, keywords, new_name):
    """
    Process all MKV files in the specified directory by replacing track names.

    Args:
        directory (str): The directory path where the MKV files are located.
        keywords (list): A list of keywords to search for in the track names.
        new_name (str): The new name to replace the matched keywords in the track names.

    Returns:
        None
    """
    flag = True
    for filename in os.listdir(directory):
        if filename.endswith(".mkv"):
            flag = False
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, f"modified_{filename}")
            remove_attachment_by_name(input_file, words_to_remove)
            replace_track_names(input_file, output_file, keywords, new_name)
            print(f"--------------- Processed {filename} ---------------")
    if flag:
        print("No MKV files found in the specified directory.")


if __name__ == "__main__":
    try:
        create_env_file()
        words_to_remove = config("KEYWORDS")
        words_to_remove = words_to_remove.split(",")
        # check if the user has entered the keywords
        if " Word1" in words_to_remove:
            raise Exception("Please enter the keywords in the .env file")
        dirPath, new_name = mainMenu()
        process_directory(dirPath, words_to_remove, new_name)
    except Exception as e:
        if "'NoneType' object has no attribute 'split'" in str(e):
            print("Please change the .env configuration file")
        else:
            print(e)
    finally:
        input("Press Enter to exit...")
