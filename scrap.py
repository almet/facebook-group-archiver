# -*- coding: utf-8 -*-
import argparse
import codecs
import shutil
import os
import json
import hashlib

from operator import attrgetter

import dateutil.parser
import requests
from jinja2 import Environment, FileSystemLoader

THEME_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'theme')


class Author(object):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class Comment(object):
    def __init__(self, item):
        self.content = item['message'] if 'message' in item else None
        self.author = Author(item['from'])
        self.date = dateutil.parser.parse(item['created_time'])
        self.likes = [Author(d) for d in item['likes']['data']] if 'likes' in item else []


class Entry(object):
    def __init__(self, item):
        if 'picture' in item:
            self.picture = item['picture']
        self.content = item['message'] if 'message' in item else None
        self.author = Author(item['from']) if 'from' in item else None
        self.date = dateutil.parser.parse(item['created_time'])
        self.likes = [Author(d) for d in item['likes']['data']] if 'likes' in item else []
        self.comments = [Comment(d) for d in item['comments']['data']] if 'comments' in item else []


def render_template(output_path, tpl_name, filename, **options):
    env = Environment(loader=FileSystemLoader(THEME_PATH))
    template = env.get_template(tpl_name)
    output = template.render(**options)

    full_path = os.path.join(output_path, filename)

    with codecs.open(full_path, 'w+', encoding='utf-8') as f:
        f.write(output)


def copy(source, destination):
    """Recursively copy source into destination.

    Taken from pelican.

    If source is a file, destination has to be a file as well.
    The function is able to copy either files or directories.
    :param source: the source file or directory
    :param destination: the destination file or directory
    """
    source_ = os.path.abspath(os.path.expanduser(source))
    destination_ = os.path.abspath(os.path.expanduser(destination))

    if os.path.isfile(source_):
        dst_dir = os.path.dirname(destination_)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy2(source_, destination_)

    elif os.path.isdir(source_):
        if not os.path.exists(destination_):
            os.makedirs(destination_)
        if not os.path.isdir(destination_):
            return

        for src_dir, subdirs, others in os.walk(source_):
            dst_dir = os.path.join(destination_,
                                   os.path.relpath(src_dir, source_))

            if not os.path.isdir(dst_dir):
                # Parent directories are known to exist, so 'mkdir' suffices.
                os.mkdir(dst_dir)

            for o in others:
                src_path = os.path.join(src_dir, o)
                dst_path = os.path.join(dst_dir, o)
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dst_path)


def download(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    m = hashlib.md5()
    m.update(url)
    filename = m.hexdigest()
    file_path = os.path.join(output_path, filename)
    if not os.path.exists(file_path):
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            with open(file_path, 'wb') as f:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, f)
    return filename


def parse_data(data):
    entries = [Entry(d) for d in data]
    entries.sort(key=attrgetter('date'))
    return entries


def download_pictures(entries, output_path):
    for entry in entries:
        if hasattr(entry, 'picture'):
            new_url = download(entry.picture, os.path.join(output_path, 'pictures'))
            entry.picture = 'pictures/%s' % new_url


def generate_archive(data, output_path):
    with open(data, 'r') as f:
        data_json = json.load(f)
    entries = parse_data(data_json)
    download_pictures(entries, output_path)
    render_template(output_path, 'index.html', 'index.html', entries=entries)


def copy_assets(output_path):
    copy(os.path.join(THEME_PATH, 'fonts'), os.path.join(output_path, 'fonts'))
    copy(os.path.join(THEME_PATH, 'assets'), os.path.join(output_path, 'assets'))


def parse_args():
    parser = argparse.ArgumentParser(description='Generate facebook group archive pages.')
    parser.add_argument('--data', dest='data', default='data.json',
                        help='Location of the JSON file containing the data.')
    parser.add_argument('--output', dest='output_path',
                        default='output',
                        help='Path where to output the generated files.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    generate_archive(args.data, args.output_path)
    copy_assets(args.output_path)
    print('')
