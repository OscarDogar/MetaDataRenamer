import os


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
