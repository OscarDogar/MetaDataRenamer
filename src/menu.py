from utils import checkValidPath


def mainMenu():
    """
    Displays the main menu and prompts the user to enter the folder path and new name.

    Returns:
        tuple: A tuple containing the folder path and the new name.
    """

    new_name = ""
    # ask if the user wants to change the name of the file or add the subtitle to the .mkv file
    while True:
        option = input(
            "What do you want to do?\n1. Change the medata info \n2. Add the subtitle to the .mkv file \n\nEnter the number of the option: "
        )
        if option == "1":
            new_name = input(
                "Enter the new name to replace the match keywords(if you leave blank or press enter, it will be replaced with a blank space): "
            )
            break
        elif option == "2":
            break
        else:
            print("\nInvalid option. Please enter 1 or 2.\n")
    dirPath = get_path()
    return dirPath, " " + new_name, option


def get_path():
    while True:
        dirPath = input(
            "Enter the full path of the folder where the episodes are located: "
        )
        # Check if the entered path is valid
        if checkValidPath(dirPath):
            break
        else:
            print("Invalid path. Please enter a valid folder path.")
    return dirPath
