from utils import checkValidPath


def mainMenu():
    """
    Displays the main menu and prompts the user to enter the folder path and new name.

    Returns:
        tuple: A tuple containing the folder path and the new name.
    """
    
    #TODO: Make a menu to select if change the name of the file or add the subtitle to the .mkv file
    
    while True:
        dirPath = input(
            "Enter the full path of the folder where the episodes are located: "
        )
        # Check if the entered path is valid
        if checkValidPath(dirPath):
            break
        else:
            print("Invalid path. Please enter a valid folder path.")
    new_name = input(
        "Enter the new name to replace the match keywords(if you leave blank or press enter, it will be replaced with a blank space): "
    )
    return dirPath, " " + new_name
