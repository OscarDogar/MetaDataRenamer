import subprocess, re
from utils import checkName


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
        #TODO check if mkvmerge is installed
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
            track_name = line.split(":", 1)[1].strip()
            if checkName(track_name, keywords):
                tracks.append((track_id, track_name))
        elif ("Title:") in line or ("Título:") in line:
            if checkName(line.split(":", 1)[1].strip(), keywords):
                original_title = line.split(":", 1)[1].strip()
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
