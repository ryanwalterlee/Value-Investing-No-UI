RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
BOLD = "\033[1m"
BOLD_RED = "\033[1;31m"
RESET = "\033[0m"

def add_colour(value, lower_value, upper_value, mode):
    """
    Returns colour of text based on provided lower and upper value thresholds.

    Arguments:
        value (int): actual value
        lower_value (int): lower threshold for value
        upper_value (int): upper threshold for value
        mode (0 or 1): 0 if the higher the value, the better (green) and lower the value, the worse (red) else 1
    
    Returns:
        string: returns value in the correct colour
    """
    colour = None
    if value < lower_value:
        colour = RED if mode == 0 else GREEN
    elif value >= upper_value:
        colour = GREEN if mode == 0 else RED
    else:
        colour = YELLOW

    return "{}{}{}".format(colour, round(value, 2), RESET)

def bold_text(text):
    return "{}{}{}".format(BOLD, text, RESET)

def bold_red_text(text):
    return "{}{}{}".format(BOLD_RED, text, RESET)