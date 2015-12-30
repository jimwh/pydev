#!/usr/bin/python

"""
Change extension
for file in *.PNG; do mv "$file" "${file%.PNG}.png"; done
Resize png files
for file in Slide*.png; do convert $file -resize 800x600 $file; done
"""

import os
import sys
import re
import glob
import shutil
import string
import Image

FILE_REGEX = "[Ss]lide*.[pP][nN][gG]"
HTML_EXTENSION = ".html"
TEMPLATE_FILE_PATH = "/home/gd2398/development/rascal/course_updates/templateFiles/"


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split('(\d+)', text)]


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)


def rename_files(path):
    slide_img = glob.glob(FILE_REGEX)
    if len(slide_img) == 0:
        print("no img files in the path: %s" % path)
        sys.exit(1)

    for slide in slide_img:
        (name, ext) = os.path.splitext(slide)
        os.rename(slide, name + ext.lower())


def resize_images():
    width = 800
    height = 600

    for imageName in glob.glob(FILE_REGEX):
        image = Image.open(imageName)
        image.resize((width, height), Image.ANTIALIAS)
        image.save(imageName)


def create_html_files():
    # load slides from current directory and sort numerically
    files = sorted(glob.glob(FILE_REGEX), key=natural_keys)

    for f in files:
        isFirst = files.index(f) == 0
        isLast = files[-1] == f
        imageName, imageExtension = os.path.splitext(f)

        firstPage = "#" if isFirst else files[0].replace(imageExtension, HTML_EXTENSION)
        firstImage = "first-inactive.png" if isFirst else "first.png"

        leftPage = "#" if isFirst else files[files.index(f) - 1].replace(imageExtension, HTML_EXTENSION)
        leftImage = "left-inactive.png" if isFirst else "left.png"

        lastPage = "#" if isLast else files[-1].replace(imageExtension, HTML_EXTENSION)
        lastImage = "last-inactive.png" if isLast else "last.png"

        rightPage = "#" if isLast else files[files.index(f) + 1].replace(imageExtension, HTML_EXTENSION)
        rightImage = "right-inactive.png" if isLast else "right.png"

        htmlText = string.Template("""
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
      "http://www.w3.org/TR/html4/transitional.dtd">
    <html>
    <head>
      <meta HTTP-EQUIV=CONTENT-TYPE CONTENT="text/html; charset=utf-8">
      <title>Slide 9</title>
    </head>
    <body text="#000000" bgcolor="#FFFFFF" link="#000080" vlink="#0000FF" alink="#808080">
    <center>
      <a href="$firstPage"><img src="$firstImage" border=0 alt="First page" /></a> 
      <a href="$leftPage"><img src="$leftImage" border=0 alt="Back"/></a> 
      <a href="$rightPage"><img src="$rightImage" border=0 alt="Continue"></a> 
      <a href="$lastPage"><img src="$lastImage" border=0 alt="Last page"/></a>
      <a href="$homePage"><img src="home.png" border=0 alt="Overview"/></a> 
    </center>
    <br>
    <center><img src="$slide" alt=""></center>
    </body>
    </html>
    """)
        html_text = htmlText.safe_substitute(slide=f,
                                            firstPage=firstPage,
                                            firstImage=firstImage,
                                            leftPage=leftPage,
                                            leftImage=leftImage,
                                            lastPage=lastPage,
                                            lastImage=lastImage,
                                            rightPage=rightPage,
                                            rightImage=rightImage,
                                            homePage=files[0].replace(imageExtension, HTML_EXTENSION))

        html_file_name = f.replace(imageExtension, HTML_EXTENSION)
        file_handle = open(html_file_name, "w")
        file_handle.write(html_text)
        file_handle.close()


def execute(path):
    rename_files(path)
    # resizeImages()
    #create_html_files()()
    #copytree(TEMPLATE_FILE_PATH, os.getcwd())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} <img file path>'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(execute(sys.argv[1]))
