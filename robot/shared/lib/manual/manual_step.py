
def manual_text_input(description):
    """
    Displays a text box for the user to manually input information into.

    Example:
        manual_text_input("What is your name")
        > user enters name
        returns "Bob"

    :param description: str: The text to show to the user
    :return: str: The user input
    """
    # placeholder return values for now
    return "Bob"


def manual_instruction(description):
    """
    Displays an instruction/action that the user must complete

    Upon completing the instruction, the user must confirm that they have completed the instruction

    :param description: str: The instruction to display to the user
    :return: bool: Whether the user confirmed the action was completed
    """
    return True
