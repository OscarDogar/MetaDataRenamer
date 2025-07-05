import os, re


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
            "OPTION": "1",
            "DIR_PATH": "",
        }
        with open(file_path, "w") as env_file:
            for key, value in env_variables.items():
                env_file.write(f"{key} = {value}\n")


def normalize_name(name):
    """
    Normalizes a given name by converting it to lowercase and removing all whitespace.

    Args:
        name (str): The name to be normalized.

    Returns:
        str: The normalized name with all whitespace removed and converted to lowercase.

    Example:
        >>> normalize_name("John Doe")
        'johndoe'
        >>> normalize_name("  Jane   Smith  ")
        'janesmith'
    """
    return ''.join(name.lower().split())

def checkName(track_name, keywords):
    """
    Check if any keyword in the given list is contained within the normalized track name.
    
    Args:
        track_name (str): The name of the track to check against keywords.
        keywords (list): A list of keyword strings to search for in the track name.
    
    Returns:
        bool: True if any keyword is found in the normalized track name, False otherwise.
    
    Note:
        Both the track name and keywords are normalized before comparison using the 
        normalize_name function.
    """
    norm_track = normalize_name(track_name)
    for keyword in keywords:
        if normalize_name(keyword) in norm_track:
            return True
    return False

def keyword_in_track(track_name, keyword):
    """
    Check if a keyword is present in a track name.

    This function checks if a normalized version of the keyword is contained within a normalized
    version of the track name. Normalization is done using the `normalize_name` function,
    which helps ensure consistent case and formatting during comparison.

    Parameters
    ----------
    track_name : str
        The name of the track to search in
    keyword : str
        The keyword to search for in the track name

    Returns
    -------
    bool
        True if the normalized keyword is found in the normalized track name, False otherwise

    Examples
    --------
    >>> keyword_in_track("Highway to Hell", "highway")
    True
    >>> keyword_in_track("Back in Black", "highway")
    False
    """
    return normalize_name(keyword) in normalize_name(track_name)

def remove_keyword_from_name(track_name, keyword):
    """
    Removes a keyword from a track name, handling both literal matches and versions with spaces between characters.
    This function works by creating two regex patterns:
    1. The literal keyword (escaped for regex safety)
    2. A pattern that allows arbitrary spaces between each letter of the keyword
    Both patterns are combined and used to remove all instances of the keyword from the track name.
    Args:
        track_name (str): The name of the track to be cleaned
        keyword (str): The keyword to be removed from the track name
    Returns:
        str: The track name with all instances of the keyword removed and extra spaces cleaned up
    Example:
        >>> remove_keyword_from_name("Summer Hit [GDR]", "GDR")
        'Summer Hit'
        >>> remove_keyword_from_name("Summer Hit G D R", "GDR")
        'Summer Hit'
    """
    escaped_letters = [re.escape(char) for char in keyword]
    spaced_pattern = r'\s*'.join(escaped_letters)
    raw_keyword = re.escape(keyword)
    pattern = rf'({raw_keyword}|{spaced_pattern})'
    cleaned = re.sub(pattern, '', track_name, flags=re.IGNORECASE).strip()
    return re.sub(r'\s{2,}', ' ', cleaned)


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


def checkValidPath(path):
    """
    Check if the given path exists and is a directory.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists and is a directory, False otherwise.
    """
    return os.path.exists(path) and os.path.isdir(path)


def check_mkv_toolnix_installed():
    """
    Check if mkvtoolnix is installed on the system.

    Returns:
        bool: True if mkvtoolnix is installed, False otherwise.
    """
    return os.system("mkvmerge -V") == 0
