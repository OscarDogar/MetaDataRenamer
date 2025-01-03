from langdetect import detect
import os
import subprocess
from utils import checkFileExists

# available_languages = {
#     "en": "eng",
#     "es": "spa",
# }


def detect_language(text):
    """
    Detects the language of the given text using a language detection library.

    Parameters:
    text (str): The text to be analyzed for language detection.

    Returns:
    str: The detected language of the text, or "Unknown" if the language cannot be determined.
    """
    try:
        language = detect(text)
        return language
    except:
        return "Unknown"


def read_srt_files(directory):
    """
    Read all the SRT files in the current directory and return the content as a list of strings.

    Returns:
        list: A list of strings where each string represents the content of an SRT file.
    """
    # TODO: check if the file is already in the mkv file
    # want to delete the file after the process
    while True:
        deleteSubs = input(
            "Do you want to delete the subtitle files after the process? (Y/N): "
        )
        if deleteSubs.lower() == "y" or deleteSubs.lower() == "n":
            break
        elif deleteSubs == "":
            deleteSubs = "y"
            break
        else:
            print("Invalid option. Please enter Y or N.")
    # check if subs folder exists
    subsFolder = os.path.exists(os.path.join(directory, "subs"))
    available_subs_extensions = [".srt", ".vtt", ".idx"]
    if subsFolder:
        srt_files = [
            f
            for f in os.listdir(os.path.join(directory, "subs"))
            if f.endswith(tuple(available_subs_extensions))
        ]

    else:
        srt_files = [
            f
            for f in os.listdir(directory)
            if f.endswith(tuple(available_subs_extensions))
        ]
    if not srt_files:
        return
    index_duplicate_files = {}
    i = 0
    while i < len(srt_files):
        fileName = srt_files[i]
        fileWithoutExtension = os.path.splitext(fileName)[0]
        # check if have another .extension in the finals positions of the file
        if "." in fileWithoutExtension[-4:]:
            # find the last . and remove the extension
            fileWithoutExtension = fileWithoutExtension[
                : fileWithoutExtension.rfind(".")
            ]
        # find the index of the duplicate files using the fileWithoutExtension
        index_duplicate_files[fileWithoutExtension] = [
            (i, x)
            for i, x in enumerate(srt_files)
            if x.startswith(fileWithoutExtension)
        ]
        fileExtension = get_video_extension(directory, fileWithoutExtension)
        if fileExtension == "":
            print(
                f"Could not find a video file for the subtitle {fileName}. Skipping this file."
            )
            continue
        languages = get_languages_codes(
            index_duplicate_files[fileWithoutExtension], directory, subsFolder
        )
        # delete the subtitle file
        result = execute_mkvmerge(
            subsFolder,
            fileWithoutExtension,
            directory,
            languages,
            index_duplicate_files[fileWithoutExtension],
            fileExtension,
        )
        if result:
            if deleteSubs.lower() == "y":
                if subsFolder:
                    for deletedFile in index_duplicate_files[fileWithoutExtension]:
                        os.remove(os.path.join(directory, "subs", deletedFile[1]))
                else:
                    for deletedFile in index_duplicate_files[fileWithoutExtension]:
                        os.remove(os.path.join(directory, deletedFile[1]))
            print(
                f"Subtitles {fileName} added to {fileWithoutExtension}{fileExtension} file."
            )
        print("-" * 50)
        i += len(index_duplicate_files[fileWithoutExtension])
    if subsFolder and deleteSubs.lower() == "y":
        # check if the folder is empty
        if not os.listdir(os.path.join(directory, "subs")):
            os.rmdir(os.path.join(directory, "subs"))
        else:
            print("The subs folder is not empty. Could not delete it.")


def get_languages_codes(files, directory, subsFolder):
    """
    Get the language codes for a list of files.

    Args:
        files (list): A list of files.
        directory (str): The directory path.
        subsFolder (bool): Flag indicating whether the files are in a subfolder.

    Returns:
        list: A list of language codes.

    """
    languages = []
    if subsFolder:
        srtFile = os.path.join(directory, "subs")
    else:
        srtFile = directory
    for file in files:
        with open(
            os.path.join(srtFile, file[1]), "r", encoding="utf-8", errors="ignore"
        ) as f:
            # get the first 30 lines of the file and join them into a single string
            content = "".join(f.readlines()[:30])
            language = detect_language(content)
            if language != "Unknown":
                languages.append(language)
            else:
                print(f"Could not detect language for {file}.")
    return languages


def get_video_extension(directory, file):
    """
    Get the video file extension for a given directory and file name.

    Args:
        directory (str): The directory where the file is located.
        file (str): The name of the file (without extension).

    Returns:
        str: The video file extension (e.g., ".mkv", ".mp4", ".avi").

    """
    videoExtensions = [".mkv", ".mp4", ".avi"]
    fileExtension = ""
    # get the video file extension
    for extension in videoExtensions:
        if checkFileExists(os.path.join(directory, file + extension)):
            fileExtension += extension
            return fileExtension
    return fileExtension


def execute_mkvmerge(
    subsFolder,
    input_file,
    directory,
    languages,
    subs,
    extension=".mkv",
):
    """
    Execute the mkvmerge command to merge the input file with the subtitle file.

    Args:
        input_file (str): The path of the input video file.
        subtitle_file (str): The path of the subtitle file.

    Returns:
        bool: True if the command execution was successful, False otherwise.
    """
    output_file = f"temp{extension}"
    languagesCommand = ""
    default = ""
    for i, language in enumerate(languages):
        if language == "es":
            default = f' --default-track 0:yes --track-name 0:"Español"'
        else:
            default = ""
        if subsFolder:
            languagesCommand += (
                f' {default} --language 0:{language} subs/"{subs[i][1]}"'
            )
        else:
            languagesCommand += f' {default} --language 0:{language} "{subs[i][1]}"'

    command = f'cd {directory} && mkvmerge -o {output_file} "{input_file}{extension}" {languagesCommand}'
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        # Read and process the output line by line
        for line in process.stdout:
            # Process the output to extract progress information
            if "progreso" in line.lower() or "progress" in line.lower():
                # print in the same line
                print(f"\r{line.strip()}", end="")
            elif (
                "el multiplexado tard" in line.lower() or "muxing took" in line.lower()
            ):
                print("")
                print(line.strip())
        # Wait for the process to finish
        process.wait()
        # Check the return code
        # if process.returncode != 0:
        #     print(f"Error executing the command: {command}")
        #     return False
        changeName = (
            f'cd {directory} && move /Y {output_file} "{input_file}{extension}"'
        )
        subprocess.run(
            changeName, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Error executing the command: {command}")
        return False
