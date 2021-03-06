#!/usr/bin/env python3
# By Infected
# 2016

###########################################
#                  COLORS                 #
###########################################

CODE = '\x1b['
colors = {
    "BOLD": 1,
    "D": 0,
    "BLACK": 30,
    "RED": 31,
    "GREEN": 32,
    "YELLOW": 33,
    "BLUE": 34,
    "MAGENTA": 35,
    "CYAN": 36,
    "WHITE": 37
    }
effects = {
    "UNDERLINE": 4,
    "BLINK": 5,
    "INVERT": 7,
    "STRIP": 9
}


def color(text='', fg="D", bold=True, bg=None, fx=None) -> str:
    fg = fg.upper() if type(fg) == str else "D"
    bg = bg.upper() if type(bg) == str else None
    fx = fx.upper() if type(fx) == str else None

    string = CODE
    # Bold
    if bold:
        string += str(colors["BOLD"])
    else:
        string += str(colors["D"])

    # Color part
    string += ";"
    string += str(colors[fg])

    # Fx part
    if fx is not None:
        string += ";"
        string += str(effects[fx])

    # Bg part
    if bg is not None:
        string += ";"
        string += str(colors[bg] + 10)

    # Text part
    string += 'm'
    string += str(text)

    # End part
    string += CODE
    string += str(colors["D"])
    string += "m"  # End

    return string


STATUS = color('⚑', 'GREEN')
WARNING = color('⚑', 'YELLOW')
ERROR = color('⚑', 'RED')
FATAL = color('⌁', 'RED', False, None, 'INVERT')


def msg(message, priority=0, function=None, *data):
    if priority <= 0:
        # status
        mode = STATUS
        message = color(message, 'GREEN')
    if priority == 1:
        # Warning
        mode = WARNING
        message = color(message, 'YELLOW')
    if priority == 2:
        # Error
        mode = ERROR
        message = color(message, 'RED')
    if priority >= 3:
        # Fatal
        mode = FATAL
        message = color(message, 'RED', False, None, 'invert')

    print(mode, end=" ")

    if function is not None:
        function_color = 'BLUE'
        function += ": "
        print(color(function, function_color), end="")

    print(message, end="")
    if data is not ():
        print("\t" + color("|", 'YELLOW'), end="")
        print(color(" " + str(list(data)), "MAGENTA"))
    else:
        print()
