import os
import re
import argparse
import requests
import progressbar
from mechanize import Browser
from bs4 import BeautifulSoup
from courses import COURSES_DICT

class UdacityDownloader():
    """
    Class to download content (videos, lecture notes, ...) from udacity.com for
    use offline.
    """

    BASE_URL =    'http://udacity.com/wiki/%s'
    DOWNLOAD_URL =    BASE_URL + '/downloads'

    def __init__(self):
        self.browser = Browser()
        self.browser.set_handle_robots(False)

    def get_course_name_from_url(self, course_url):
        """Given the course URL, return the name, e.g., cs212"""
        return course_url.split('/')[4]

    def get_download_url_from_name(self, course_name):
        """Given the name of a course, return the video lecture url"""
        return self.DOWNLOAD_URL % course_name

    def get_downloadable_content(self, course_url):
        """
        returns {"types" : {"class_name":"link", "class_name": "link"}, "arko_type": {"class_name":"link", "class_name": "link"}}
        """
        course_name = self.get_course_name_from_url(course_url)
        long_course_name = COURSES_DICT.get(course_name, course_name)

        print "* Collecting downloadable content from " + course_url

        # get the course name, and redirect to the course lecture page
        vidpage = self.browser.open(course_url)

        # extract the weekly classes
        soup = BeautifulSoup(vidpage,"lxml")
        headers = soup.find("div", { "class" : "wtabs extl" })

        head_names = headers.findAll("h2")
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
                    className += "."
                weeklyClasses[className] = resourceLink
            headText = head_name.text
            while headText in resources:
                headText += "."
            resources[headText] = weeklyClasses
        return resources

    def download_course(self, cname, dest_dir="."):
        """Download all the contents (quizzes, videos, lecture notes, ...) of the course to the given destination directory (defaults to .)"""

        download_url = self.get_download_url_from_name(cname)
        print "* Need to download from ", download_url

        resource_dict = self.get_downloadable_content(download_url)

        long_cname = COURSES_DICT.get(cname, cname)
        print '* Got all downloadable content for ' + long_cname

        course_dir = os.path.abspath(os.path.join(dest_dir, long_cname))

        # ensure the target dir exists
        if not os.path.exists(course_dir):
            os.mkdir(course_dir)

        print "* " + cname + " will be downloaded to " + course_dir

        # download the standard pages
        print " - Downloading zipped/videos pages"

        for types, download_dict in resource_dict.iteritems():
            # ensure the course directory exists
            resource_dir = os.path.join(course_dir, types)
            if not os.path.exists(resource_dir):
                os.makedirs(resource_dir)
            print " -- Downloading ", types
            for fname, tfname in download_dict.iteritems():
                try:
                    print "    * Downloading ", fname, "..."
                    download_file(tfname, resource_dir, fname)
                except Exception as e:
                    print "     - failed ", fname, e

def download_file(url, path ,fn):
    file = os.path.join(path, fn)     
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    total_length = int(r.headers.get('content-length'))

    if os.path.exists(file):
        existing_file_len = os.path.getsize(file)
        if total_length == existing_file_len:
            # File downloaded, early return 
            return

    ch_size = (1024**2) * 2 # MBs
    bar = progressbar.ProgressBar(max_value=total_length/ch_size) 
    
    with open(file, 'wb') as f:
        counter = 0
        for chunk in r.iter_content(chunk_size=ch_size): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
                counter += 1
                bar.update(counter)
def main():
    #parse the commandline args
    parser = argparse.ArgumentParser(description='Download Udacity.com course videos/docs for offline use.')
    parser.add_argument("-d", dest='dest_dir', type=str, default=".", help='destination directory where everything will be saved')
    parser.add_argument('course_names', nargs="+", metavar='<course name>',
                        type=str, help='one or more course names (from the url)')
    args = parser.parse_args()

    # check the parser
    # instantiate the downloader class
    d = UdacityDownloader()

    # download the content
    for cn in args.course_names:
        d.download_course(cn, dest_dir=args.dest_dir)

    print " Download Complete."

if __name__ == '__main__':
    main()


