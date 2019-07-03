import os
import requests
import zipfile
from .loader import newspath_form


num_categories = 20
url_form = 'https://lovit-politician-news-dataset.s3.ap-northeast-2.amazonaws.com/zips/news/{}.zip'
sep = os.path.sep
zipdirname = sep.join(os.path.dirname(os.path.realpath(__file__)).split(sep)[:-1] + ['zips'])

def check_dir(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('created dir {}'.format(dirname))

def fetch(category=None, remove_zip=True):

    def sort(paths):
        return sorted(paths, key=lambda x:int(x.split(sep)[-1].split('.')[0]))

    if isinstance(category, int):
        categories = [category]
    else:
        categories = [c for c in range(num_categories)]

    for c in categories:
        url = url_form.format(c)
        dirname = newspath_form.format(c)
        zippath = '{}/{}.zip'.format(zipdirname, c)
        check_dir(zippath)
        download_a_file(url, zippath)
        filename = '/'.join(zippath.split('/')[-2:])
        print('downloaded {}'.format(filename))
        unzip(zippath, dirname)
        print('unziped {}'.format(filename))

        if remove_zip:
            os.remove(zippath)
    print('done')

def unzip(source, destination):
    """
    Arguments
    ---------
    source : str
        zip file address. It doesn't matter absolute path or relative path
    destination :
        Directory path of unzip
    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    abspath = os.path.abspath(destination)
    dirname = os.path.dirname(abspath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    try:
        downloaded = zipfile.ZipFile(source)
        downloaded.extractall(destination)
        return True
    except Exception as e:
        print(e)
        return False

def download_a_file(url, fname):
    """
    Arguments
    --------
    url : str
        URL address of file to be downloaded
    fname : str
        Download file address
    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # If you do not set user-agent, downloading from url is stalled.
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}

    try:
        r = requests.get(url, stream=True, headers=headers)
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(e)
        return False