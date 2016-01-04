#!/usr/bin/python

import os
import sys
import shutil
import string
import Image
import re
import glob

IMG_FILE_NAME_PATTERN = "[Ss]lide[0-9]+.png$|[Ii]mg[0-9]+.[Pp][Nn][Gg]$"
HTML_EXT = ".html"
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


def get_src_img_names(src_dir, exp):
    if not os.path.exists(src_dir):
        print("no such directory: %s" % src_dir)
        sys.exit(1)

    m = re.compile(exp)
    res = [f for f in os.listdir(src_dir) if m.search(f)]
    res = map(lambda x: "%s/%s" % (src_dir, x,), res)
    return sorted(res, key=natural_keys)


def rename_files(src_slide, dest_dir):
    dest_file_list = []
    for slide in src_slide:
        shutil.copy2(slide, dest_dir)
        base_name = os.path.basename(slide)
        dest_file = dest_dir + "/" + base_name
        dest_file_list.append(dest_file)
        (name, ext) = os.path.splitext(dest_file)
        os.rename(dest_file, name + ext.lower())
    return dest_file_list


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

        first_page = "#" if is_first else files[0].replace(img_ext, HTML_EXT)
        first_img = "first-inactive.png" if is_first else "first.png"

        left_page = "#" if is_first else files[files.index(f) - 1].replace(img_ext, HTML_EXT)
        left_img = "left-inactive.png" if is_first else "left.png"

        last_page = "#" if is_last else files[-1].replace(img_ext, HTML_EXT)
        last_img = "last-inactive.png" if is_last else "last.png"

        right_page = "#" if is_last else files[files.index(f) + 1].replace(img_ext, HTML_EXT)
        right_img = "right-inactive.png" if is_last else "right.png"

        template = string.Template(TEMPLATE_TEXT)

        html_text = template.safe_substitute(slide=f,
                                             first_page=first_page,
                                             first_img=first_img,
                                             left_page=left_page,
                                             left_img=left_img,
                                             last_page=last_page,
                                             last_img=last_img,
                                             right_page=right_page,
                                             right_img=right_img,
                                             home_page=files[0].replace(img_ext, HTML_EXT))

        html_file_name = f.replace(img_ext, HTML_EXT)
        file_handle = open(dest_dir + "/" + html_file_name, "w")
        file_handle.write(html_text)
        file_handle.close()


def copy_template_dir(src, dest):
    for filename in glob.glob(os.path.join(src, '*.png')):
        shutil.copy(filename, dest)


def execute(src_dir, template_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    src_img_names = get_src_img_names(src_dir, IMG_FILE_NAME_PATTERN)

    dest_file_list = rename_files(src_img_names, dest_dir)

    resize_images(dest_file_list)

    base_file_list = [os.path.basename(x) for x in dest_file_list]

    create_html_files(base_file_list, dest_dir)

    copy_template_dir(template_dir, dest_dir)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('usage: {} <src img dir> <template img dir> <destination dir>'.format(sys.argv[0]))
        sys.exit(1)

    sys.exit(execute(sys.argv[1], sys.argv[2], sys.argv[3]))
