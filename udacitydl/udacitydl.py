from __future__ import print_function

import os
import re
import argparse
import requests

import mechanicalsoup
from tqdm import tqdm

from courses import COURSES_DICT


class UdacityDownloader:
    """
    Class to download content (videos, lecture notes, ...) from udacity.com for
    use offline.
    """

    BASE_URL =    'http://udacity.com/wiki/%s'
    DOWNLOAD_URL =    BASE_URL + '/downloads'

    def __init__(self):
        self.browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
        )

    def get_download_url_from_name(self, course_name):
        """Given the name of a course, return the video lecture url"""
        return self.DOWNLOAD_URL % course_name

    def get_downloadable_content(self, course_wiki_url):
        """
        returns {"Lessons" : {"class_name":"link", "class_name": "link"}, "arko_type": {"class_name":"link", "class_name": "link"}}
        """
        course_name = get_course_name_from_wiki_url(course_wiki_url)
        long_course_name = COURSES_DICT.get(course_name, course_name)

        print('* Collecting downloadable content from ' + course_wiki_url)
        # get the course name, and redirect to the course lecture page
        self.browser.open(course_wiki_url)
        wikipage = self.browser.get_current_page()

        # extract the weekly classes
        headers = wikipage.find('div', { 'class' : 'wtabs extl' })

        head_names = headers.findAll('h2')
        resources = {}
        for head_name in head_names:
            ul = head_name.findNextSibling('ul')
            lis = ul.findAll('li')

            weeklyClasses = {}
            classNames = []
            for li in lis:
                className = li.a.text
                classNames.append(className)
                hrefs = li.find('a')
                resourceLink = hrefs['href']
                while className in weeklyClasses:
                    className += '.'
                weeklyClasses[className] = resourceLink
            headText = head_name.text
            while headText in resources:
                headText += '.'
            resources[headText] = weeklyClasses
        return resources


    def download_course(self, cname, dest_dir='.'):
        """Download all the contents (quizzes, videos, lecture notes, ...) of the course to the given destination directory (defaults to .)"""

        course_wiki_url = self.get_download_url_from_name(cname)
        print( '* Need to download from ', course_wiki_url)

        resource_dict = self.get_downloadable_content(course_wiki_url)

        long_cname = COURSES_DICT.get(cname, cname)
        print( '* Got all downloadable content for ' + long_cname)

        course_dir = os.path.abspath(os.path.join(dest_dir, long_cname))

        # ensure the target dir exists
        if not os.path.exists(course_dir):
            os.mkdir(course_dir)

        print( '* ' + cname + ' will be downloaded to ' + course_dir)

        # download the standard pages
        print( '' - Downloading zipped/videos pages')

        for types, download_dict in resource_dict.items():
            # ensure the course directory exists
            resource_dir = os.path.join(course_dir, types)
            if not os.path.exists(resource_dir):
                os.makedirs(resource_dir)
            print( ' -- Downloading ', types)
            for fname, tfname in download_dict.items():
                try:
                    print( '    * Downloading ', fname, '...')
                    download_file(tfname, resource_dir, fname)
                except Exception as e:
                    print( '     - failed ', fname, e)

def get_course_name_from_wiki_url(course_url):
    """Given the course URL, return the name, e.g., cs212"""
    return course_url.split('/')[4]


def download_file(target_link, resource_dir, fname):
    target_file = os.path.join(resource_dir, fname)
    r = requests.get(target_link, stream=True)
    total_size = int(r.headers.get('content-length'))
    block_size = 1024
    wrote = 0
    if os.path.exists(target_file):
        existing_file_size = os.path.getsize(target_file)
        if total_size == existing_file_size:
            print('     - Already downloaded.')
            return

    with open(target_file, 'wb') as f:
        with tqdm(total=total_size / (32*1024.0), unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for data in r.iter_content(32*1024):
                f.write(data);
                pbar.update(len(data))
                wrote = wrote + len(data)
    if total_size != 0 and wrote != total_size:
        print('ERROR, something went wrong')


def main():
    #parse the commandline args
    parser = argparse.ArgumentParser(description='Download Udacity.com course videos/docs for offline use.')
    parser.add_argument('-d', dest='dest_dir', type=str, default=".", help='destination directory where everything will be saved')
    parser.add_argument('course_names', nargs="+", metavar='<course name>',
                        type=str, help='one or more course names (from the url)')
    args = parser.parse_args()

    # download the content
    d = UdacityDownloader()
    for cn in args.course_names:
        d.download_course(cn, dest_dir=args.dest_dir)
    print( ' Download Complete.')

if __name__ == '__main__':
    main()
