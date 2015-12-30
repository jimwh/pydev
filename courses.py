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


def natural_keys(s):
    return tuple(int(part) if re.match(r'[0-9]+$', part) else part
                 for part in re.split(r'([0-9]+)', s))


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


def rename_files(slide_img):
    for slide in slide_img:
        (name, ext) = os.path.splitext(slide)
        os.rename(slide, name + ext.lower())


def resize_images(files):
    width = 800
    height = 600

    for img_name in files:
        image = Image.open(img_name)
        new_img = image.resize((width, height), Image.ANTIALIAS)
        new_img.save(img_name)


def create_html_files(files):
    for f in files:
        is_first = files.index(f) == 0
        is_last = files[-1] == f
        img_name, img_ext = os.path.splitext(f)

        first_page = "#" if is_first else files[0].replace(img_ext, HTML_EXTENSION)
        first_img = "first-inactive.png" if is_first else "first.png"

        left_page = "#" if is_first else files[files.index(f) - 1].replace(img_ext, HTML_EXTENSION)
        left_img = "left-inactive.png" if is_first else "left.png"

        last_page = "#" if is_last else files[-1].replace(img_ext, HTML_EXTENSION)
        last_img = "last-inactive.png" if is_last else "last.png"

        right_page = "#" if is_last else files[files.index(f) + 1].replace(img_ext, HTML_EXTENSION)
        right_img = "right-inactive.png" if is_last else "right.png"

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
                                             first_page=first_page,
                                             first_img=first_img,
                                             left_page=left_page,
                                             left_img=left_img,
                                             last_page=last_page,
                                             last_img=last_img,
                                             right_page=right_page,
                                             right_img=right_img,
                                             home_page=files[0].replace(img_ext, HTML_EXTENSION))

        html_file_name = f.replace(img_ext, HTML_EXTENSION)
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
    res = map(lambda x: "%s/%s" % (path, x,), res)
    return res


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} <src img file path>'.format(sys.argv[0]))
        sys.exit(1)

    sys.exit(execute(sys.argv[1]))
