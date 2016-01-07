#!/usr/bin/python

import re


IMG_FILE_NAME_PATTERN = '''
[Ss]lide     # Slide or slide
[0-9]+        # follow by digit
.[Pp][Nn][Gg]$        # png or PNG
|                            # or
[Ii]mg[0-9]+.[Pp][Nn][Gg]$   #
|                            # or
[Ii]mg[0-9]+.[Jj][Pp][Gg]$   #
'''


def test_pattern():
    if re.search(IMG_FILE_NAME_PATTERN, 'img0.png', re.VERBOSE):
        print("found")
    else:
        print("not found")


if __name__ == '__main__':
    test_pattern()

