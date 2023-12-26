import subprocess
import os, re
from decouple import config


def checkName(name, keywords):
    """
    Check if the name contains any of the specified keywords.

    Args:
        name (str): The name of the video file.
        keywords (list): A list of keywords to search for in the name.

    Returns:
        bool: True if the name contains any of the specified keywords, False otherwise.
    """
    for keyword in keywords:
        if keyword in name or keyword.strip() in name:
            return True
    return False


import subprocess
import re


def remove_attachment_by_name(input_file, keywords):
    """
    Removes attachments from a Matroska (MKV) file based on the attachment name.

    Args:
        input_file (str): The path to the input MKV file.
        keywords (list): A list of keywords to match against the attachment names.

    Returns:
        None
    """
    cmd = ["mkvmerge", "--identify", input_file]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        # check if the command was successful
        if result.returncode != 0:
            print("Error identifying tracks info")
            return
        # check if result.stdout includes "Attachment ID"
        check = (
            "Attachment ID" in result.stdout
            or "ID del archivo adjunto" in result.stdout
        )
        if not check:
            return
        lines = result.stdout.splitlines()
        attachment_id = None
        for line in lines:
            if ("Attachment ID") in line or ("ID del archivo adjunto") in line:
                # save the attachment id
                attachment_id = int(re.search(r"\d+", line).group())
                pattern = r"file name '([^']+)'"
                pattern2 = r"nombre de archivo '([^']+)'"
                match = re.search(pattern, line)
                match2 = re.search(pattern2, line)
                file_name = None
                if match:
                    file_name = match.group(1)
                elif match2:
                    file_name = match2.group(1)
                if file_name:
                    if checkName(file_name, keywords):
                        print(f"Removing attachment {attachment_id}...")
                        # Remove the attachment
                        mkvpropedit_command = [
                            "mkvpropedit",
                            input_file,
                            "--delete-attachment",
                            f"{attachment_id}",
                        ]
                        subprocess.run(mkvpropedit_command)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def replace_track_names(input_file, output_file, keywords, new_name):
    """
    Replaces track names in an MKV file based on specified keywords.

    Args:
        input_file (str): Path to the input MKV file.
        output_file (str): Path to the output MKV file with modified track names.
        keywords (list): List of keywords to search for in track names.
        new_name (str): The new name to replace the keywords with.

    Returns:
        None
    """
    # Get track info using mkvinfo
    mkvinfo_command = ["mkvinfo", input_file]
    result = subprocess.run(
        mkvinfo_command, capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        print("Error identifying tracks. Check if mkvinfo is installed.")
        return

    # Parse track info
    tracks = []
    lines = result.stdout.splitlines()
    track_id = None
    original_title = None
    for line in lines:
        if ("track number:") in line or ("Número de pista:") in line:
            # get the first number on the left in string using regex
            track_id = int(re.search(r"\d+", line).group())
        elif ("Name:") in line or ("Nombre:") in line:
            track_name = line.split(":")[1].strip()
            if checkName(track_name, keywords):
                tracks.append((track_id, track_name))
        elif ("Title:") in line or ("Título:") in line:
            if checkName(line.split(":")[1].strip(), keywords):
                original_title = line.split(":")[1].strip()
    if not tracks and not original_title:
        print("No changes needed.")
        return
    elif original_title:
        print(f"Changing title...")
        changeTitle(input_file, new_name, keywords, original_title)

    # Replace track names if any of the specified keywords are present
    for track_id, track_name in tracks:
        for keyword in keywords:
            a = keyword.strip()
            if keyword in track_name or keyword.strip() in track_name:
                new_track_name = track_name.replace(keyword, new_name)
                if new_track_name == track_name:
                    new_track_name = track_name.replace(keyword.strip(), new_name)
                mkvpropedit_command = [
                    "mkvpropedit",
                    input_file,
                    "--edit",
                    f"track:{track_id}",
                    "--set",
                    f"name={new_track_name}",
                ]
                subprocess.run(mkvpropedit_command)
                # print(f"Track {track_id} renamed to {new_track_name}")
                break


def changeTitle(input_file, new_name, keywords, original_title):
    """
    Change the title of a video file by replacing specified keywords in the original title with a new name.

    Args:
        input_file (str): The path to the input video file.
        new_name (str): The new name to replace the keywords in the original title.
        keywords (list): A list of keywords to search for in the original title.
        original_title (str): The original title of the video file.

    Returns:
        None
    """
    for keyword in keywords:
        if keyword in original_title or keyword.strip() in original_title:
            original_title = original_title.replace(keyword, new_name)
            if original_title == original_title:
                original_title = original_title.replace(keyword.strip(), new_name)
            mkvpropedit_command = [
                "mkvpropedit",
                input_file,
                "--edit",
                "info",
                "--set",
                f"title={original_title}",
            ]
            subprocess.run(mkvpropedit_command)
            break


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


def checkFileExists(file_path):
    """
    Check if a file exists at the given file path.

    Args:
        file_path (str): The path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    fullPath = os.getcwd() + file_path
    return os.path.isfile(fullPath) or os.path.exists(file_path)


def create_env_file():
    """
    Creates a new .env file if it doesn't already exist and writes the environment variables to it.

    The function checks if the .env file exists. If it doesn't, it creates a new .env file and writes
    the environment variables to it. The environment variables are defined in the `env_variables` dictionary.

    Args:
        None

    Returns:
        None
    """
    file_path = ".env"
    if not checkFileExists(file_path):
        env_variables = {
            "KEYWORDS": '" Word1, Word2, Word3, Word4"',
        }
        with open(file_path, "w") as env_file:
            for key, value in env_variables.items():
                env_file.write(f"{key} = {value}\n")


if __name__ == "__main__":
    try:
        create_env_file()
        words_to_remove = config("KEYWORDS")
        words_to_remove = words_to_remove.split(",")
        # check if the user has entered the keywords
        if " Word1" in words_to_remove:
            raise Exception("Please enter the keywords in the .env file")
        while True:
            dirPath = input(
                "Enter the full path of the folder where the episodes are located: "
            )
            # Check if the entered path is valid
            if os.path.exists(dirPath) and os.path.isdir(dirPath):
                break
            else:
                print("Invalid path. Please enter a valid folder path.")
        new_name = ""
        process_directory(dirPath, words_to_remove, new_name)
    except Exception as e:
        if "'NoneType' object has no attribute 'split'" in str(e):
            print("Please change the .env configuration file")
        else:
            print(e)
    finally:
        input("Press Enter to exit...")
