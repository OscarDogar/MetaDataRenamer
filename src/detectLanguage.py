from langdetect import detect
import os
import subprocess

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
    srt_files = [f for f in os.listdir(directory) if f.endswith(".srt")]
    if not srt_files:
        return
    for file in srt_files:
        fileWithoutExtension = os.path.splitext(file)[0]
        # check if have another .extension in the finals positions of the file
        if "." in fileWithoutExtension[-4:]:
            # find the last . and remove the extension
            fileWithoutExtension = fileWithoutExtension[
                : fileWithoutExtension.rfind(".")
            ]
        srtFile = os.path.join(directory, file)
        with open(srtFile, "r") as f:
            # get the first 30 lines of the file and join them into a single string
            content = "".join(f.readlines()[:30])
            language = detect_language(content)
            if language != "Unknown":
                # check if the language is in availables
                if language not in available_languages:
                    print(f"Language {language} is not available for {file}.")
                    continue
                execute_mkvmerge(fileWithoutExtension, file, directory, language)
                print(f"Subtitle {file} added to {fileWithoutExtension}.mkv file.")
            else:
                print(f"Could not detect language for {file}.")


def execute_mkvmerge(
    input_file,
    subtitle_file,
    directory,
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
    output_file = "temp.mkv"
    command = f'cd {directory} && mkvmerge -o {output_file} "{input_file}.mkv" --language 0:{available_languages[language]} "{subtitle_file}" && move /Y {output_file} "{input_file}.mkv"'
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
