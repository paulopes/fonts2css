#!/usr/bin/env python
# -*- coding: utf8 -*-

""" fonts2css module
"""

import os
import sys
import errno
import base64


def make_sure_path_exists(dest_path):
    """ Used to create the destination folder for a file, if that folder doesn't exist yet.
    """
    if not os.path.isfile(dest_path):
        dest_folder = os.path.dirname(dest_path)

        if dest_folder and not os.path.exists(dest_folder):
            try:
                os.makedirs(dest_folder)
            except OSError as e: # Guard against race condition
                if e.errno != errno.EEXIST:
                    raise
        return False
    else:
        return True


def main():
    if len(sys.argv) > 1:

        font_name = sys.argv[1]

        if len(sys.argv) > 2:
            folder_path = sys.argv[2]
        else:
            folder_path = '.'

        font_name_lower = font_name.lower()
        css_filename = font_name + '.css'
        make_sure_path_exists(css_filename)

        if os.path.isdir(folder_path):
            fonts = {
                'eot': ('embedded-opentype', 'application/vnd.ms-fontobject'),
                'woff': ('woff', 'application/font-woff'),
                'woff2': ('woff2', 'application/font-woff2'),
                'ttf': ('truetype', 'application/x-font-truetype'),
                'otf': ('opentype', 'application/x-font-opentype'),
                'svg': ('svg', 'image/svg+xml'),
            }
            font_dict = dict()
            for path, dirs, file_list in os.walk(folder_path):
                for filename in file_list:
                    last_dot = filename.rfind('.')
                    if last_dot > 0:  # File not hidden and has extension
                        begin = filename[:last_dot].lstrip().lower()
                        extension = filename[last_dot + 1:].rstrip()
                        if begin == font_name_lower and extension in fonts:
                            font_dict[extension] = os.path.join(path, filename)
            css_text = """\
@font-face {
  font-family: '""" + font_name + """';
  font-weight: normal;
  font-style: normal;"""
            font_list = list()
            for extension in ('eot', 'woff', 'woff2', 'ttf', 'otf', 'svg'):
                if extension in font_dict:
                    path_to_file = font_dict[extension]
                    with open(path_to_file, 'rb') as f:
                        content = f.read()
                        encoded = base64.b64encode(content).decode('utf-8')
                    font_format = fonts[extension][0]
                    mime_type = fonts[extension][1]
                    font_list.append(
                        "url(data:" + mime_type +
                        ";base64," + encoded +
                        ") format('" + font_format + "')"
                    )
            if font_list:
                css_text += '''
  src: ''' + ', '.join(font_list) + ''';
}'''
            with open(css_filename, 'w') as f:
                f.write(css_text)
            print('''
The file {} has been created!
'''.format(css_filename))
        else:
            print('''
{} is not a folder!
'''.format(folder_path))
            exit(2)
    else:
        print('''
Usage:

   fonts2css <Font Name> [<path to folder with font file(s)>]
''')
        exit(1)

if __name__ == "__main__":
    main()
