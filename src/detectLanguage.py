from langdetect import detect
import os
import subprocess
from utils import checkFileExists

available_languages = {
    "en": "eng",
    "es": "spa",
}


def detect_language(text):
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
    # TODO: check if there is multiple srt files in the directory with the same name to avoid reprocessing the same file
    # TODO: check if the file is already in the mkv file
    #want to delete the file after the process
    while True:
        deleteSubs = input(
            "Do you want to delete the subtitle files after the process? (Y/N): "
        )
        if deleteSubs.lower() == "y" or deleteSubs.lower() == "n":
            break
        else:
            print("Invalid option. Please enter Y or N.")
    # check if subs folder exists
    subsFolder = os.path.exists(os.path.join(directory, "subs"))
    if subsFolder:
        srt_files = [
            f
            for f in os.listdir(os.path.join(directory, "subs"))
            if (f.endswith(".srt") or f.endswith(".vtt"))
        ]

    else:
        srt_files = [
            f
            for f in os.listdir(directory)
            if (f.endswith(".srt") or f.endswith(".vtt"))
        ]
    if not srt_files:
        return
    for file in srt_files:

        fileWithoutExtension = os.path.splitext(file)[0]
        videoExtensions = [".mkv", ".mp4", ".avi"]
        fileExtension = ""
        # check if have another .extension in the finals positions of the file
        if "." in fileWithoutExtension[-4:]:
            # find the last . and remove the extension
            fileWithoutExtension = fileWithoutExtension[
                : fileWithoutExtension.rfind(".")
            ]
        # get the video file extension
        for extension in videoExtensions:
            if checkFileExists(
                os.path.join(directory, fileWithoutExtension + extension)
            ):
                fileExtension += extension
                break
        if fileExtension == "":
            print(
                f"Could not find a video file for the subtitle {file}. Skipping this file."
            )
            continue
        if subsFolder:
            file = "subs/" + file
            srtFile = os.path.join(directory, file)
        else:
            srtFile = os.path.join(directory, file)

        with open(srtFile, "r", encoding="utf-8") as f:
            # get the first 30 lines of the file and join them into a single string
            content = "".join(f.readlines()[:30])
            language = detect_language(content)
            if language != "Unknown":
                # check if the language is in availables
                if language not in available_languages:
                    print(f"Language {language} is not available for {file}.")
                    continue
            else:
                print(f"Could not detect language for {file}.")
        # delete the subtitle file
        result = execute_mkvmerge(
            fileWithoutExtension, file, directory, fileExtension, language
        )
        if result:
            if deleteSubs.lower() == "y":
                os.remove(os.path.join(directory, file))
            print(
                f"Subtitle {file} added to {fileWithoutExtension}{fileExtension} file."
            )
    if subsFolder and deleteSubs.lower() == "y":
        os.rmdir(os.path.join(directory, "subs"))


def execute_mkvmerge(
    input_file,
    subtitle_file,
    directory,
    extension=".mkv",
    language="es",
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
    command = f'cd {directory} && mkvmerge -o {output_file} "{input_file}{extension}" --language 0:{available_languages[language]} "{subtitle_file}" && move /Y {output_file} "{input_file}{extension}"'
    try:
        subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False
