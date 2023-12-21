import subprocess
import os, re


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
    for line in lines:
        if ("track number:") in line or ("Número de pista:") in line:
            # get the first number on the left in string using regex
            track_id = int(re.search(r"\d+", line).group())
        elif ("Name:") in line or ("Nombre:") in line:
            track_name = line.split(":")[1].strip()
            tracks.append((track_id, track_name))
        elif ("Title:") in line or ("Título:") in line:
            original_title = line.split(":")[1].strip()
    if original_title:
        changeTitle(input_file, new_name, keywords, original_title)
    # Replace track names if any of the specified keywords are present
    for track_id, track_name in tracks:
        for keyword in keywords:
            if keyword in track_name:
                new_track_name = track_name.replace(keyword, new_name)
                mkvpropedit_command = [
                    "mkvpropedit",
                    input_file,
                    "--edit",
                    f"track:{track_id}",
                    "--set",
                    f"name={new_track_name}",
                ]
                subprocess.run(mkvpropedit_command)
                print(f"Track {track_id} renamed to {new_track_name}")
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
        if keyword in original_title:
            original_title = original_title.replace(keyword, new_name)
    mkvpropedit_command = [
        "mkvpropedit",
        input_file,
        "--edit",
        "info",
        "--set",
        f"title={original_title}",
    ]
    subprocess.run(mkvpropedit_command)


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
    for filename in os.listdir(directory):
        if filename.endswith(".mkv"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, f"modified_{filename}")
            replace_track_names(input_file, output_file, keywords, new_name)
            print(f"--------------- Processed {input_file} ---------------")


def checkFileExists(file_path):
    fullPath = os.getcwd() + file_path
    return os.path.isfile(fullPath) or os.path.exists(file_path)


def create_env_file():
    file_path = ".env"
    if not checkFileExists(file_path):
        env_variables = {
            "KEYWORDS": '" Word1, Word2, Word3, Word4"',
        }
        with open(file_path, "w") as env_file:
            for key, value in env_variables.items():
                env_file.write(f"{key} = {value}\n")


if __name__ == "__main__":
    directory_path = "videos"
    create_env_file()
    words_to_remove = os.environ.get("KEYWORDS")
    words_to_remove = words_to_remove.split(",")
    new_name = ""
    process_directory(directory_path, words_to_remove, new_name)