#!/usr/bin/python

import os
import sys
import shutil
import string
import Image
import re


IMG_FILE_NAME_PATTERN = "[Ss]lide[0-9]+.png$|[Ii]mg[0-9]+.[Pp][Nn][Gg]$"
HTML_EXTENSION = ".html"
DST_FILE_PATH = "/tmp/tc"


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
    print(dst)
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


def rename_files(slide_img):
    for slide in slide_img:
        (name, ext) = os.path.splitext(slide)
        os.rename(slide, name + ext.lower())


def resize_images(files):
    width = 800
    height = 600

    for img_name in files:
        print(img_name)
        image = Image.open(img_name)
        new_img = image.resize((width, height), Image.ANTIALIAS)
        new_img.save(img_name)


def create_html_files(files):

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
    results = get_img_file_name_list(path, IMG_FILE_NAME_PATTERN)
    files = sorted(results, key=natural_keys)
    rename_files(files)
    resize_images(files)
    create_html_files(files)
    copytree(path, DST_FILE_PATH)


def get_img_file_name_list(path, exp):
    m = re.compile(exp)
    res = [f for f in os.listdir(path) if m.search(f)]
    res = map(lambda x: "%s/%s" % (path, x, ), res)
    return res

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} <src img file path>'.format(sys.argv[0]))
        sys.exit(1)

    sys.exit(execute(sys.argv[1]))
