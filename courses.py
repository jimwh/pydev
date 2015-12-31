#!/usr/bin/python

import os
import sys
import shutil
import string
import Image
import re
import glob

IMG_FILE_NAME_PATTERN = "[Ss]lide[0-9]+.png$|[Ii]mg[0-9]+.[Pp][Nn][Gg]$"
HTML_EXTENSION = ".html"
DST_FILE_PATH = "/tmp/tc"
TEMPLATE_TEXT = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
      "http://www.w3.org/TR/html4/transitional.dtd">
    <html>
    <head>
      <meta HTTP-EQUIV=CONTENT-TYPE CONTENT="text/html; charset=utf-8">
      <title>Slide</title>
    </head>
    <body text="#000000" bgcolor="#FFFFFF" link="#000080" vlink="#0000FF" alink="#808080">
    <center>
      <a href="$first_page"><img src="$first_img" border=0 alt="First page" /></a>
      <a href="$left_page"><img src="$left_img" border=0 alt="Back"/></a>
      <a href="$right_page"><img src="$right_img" border=0 alt="Continue"></a>
      <a href="$last_page"><img src="$last_img" border=0 alt="Last page"/></a>
      <a href="$home_page"><img src="home.png" border=0 alt="Overview"/></a>
    </center>
    <br>
    <center><img src="$slide" alt=""></center>
    </body>
    </html>
    """


def natural_keys(s):
    return tuple(int(part) if re.match(r'[0-9]+$', part) else part
                 for part in re.split(r'([0-9]+)', s))


def get_img_file_name_list(path, exp):
    if not os.path.exists(path):
        print("no such directory: %s" % path)
        sys.exit(1)

    m = re.compile(exp)
    res = [f for f in os.listdir(path) if m.search(f)]
    res = map(lambda x: "%s/%s" % (path, x,), res)
    return sorted(res, key=natural_keys)
    # return res


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


def create_html_files(files, dest_dir):
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

        html_template_text = string.Template(TEMPLATE_TEXT)

        html_text = \
            html_template_text.safe_substitute(slide=os.path.basename(f),
                                               first_page=os.path.basename(first_page),
                                               first_img=os.path.basename(first_img),
                                               left_page=os.path.basename(left_page),
                                               left_img=os.path.basename(left_img),
                                               last_page=os.path.basename(last_page),
                                               last_img=os.path.basename(last_img),
                                               right_page=os.path.basename(right_page),
                                               right_img=os.path.basename(right_img),
                                               home_page=os.path.basename(files[0].replace(img_ext, HTML_EXTENSION)))

        html_file_name = f.replace(img_ext, HTML_EXTENSION)
        basename = os.path.basename(html_file_name)
        file_handle = open(dest_dir + "/" + basename, "w")
        file_handle.write(html_text)
        file_handle.close()


def copy_img_to_dest(file_list, dest):
    for file in file_list:
        shutil.copy2(file, dest)


def copy_template_dir(src, dest):
    for filename in glob.glob(os.path.join(src, '*.png')):
        shutil.copy(filename, dest)


def execute(src_img_path, template_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    file_names = get_img_file_name_list(src_img_path, IMG_FILE_NAME_PATTERN)
    rename_files(file_names)
    resize_images(file_names)
    create_html_files(file_names, dst_dir)
    copy_img_to_dest(file_names, dst_dir)
    copy_template_dir(template_dir, dst_dir)


"""
src img dir - img slides
template dir - pre defined png etc
dst - slides, html
"""

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('usage: {} <src img dir> <template img dir> <destination file dir>'.format(sys.argv[0]))
        sys.exit(1)

    sys.exit(execute(sys.argv[1], sys.argv[2], sys.argv[3]))
