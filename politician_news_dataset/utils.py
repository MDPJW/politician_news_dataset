from glob import glob
import os
import re


sep = os.path.sep
installpath = os.path.dirname(os.path.realpath(__file__))
newspath_form = sep.join(installpath.split(sep)[:-1] + ['data', '{}', 'news'])
commentspath_form = sep.join(installpath.split(sep)[:-1] + ['data', '{}', 'comments'])


class News:
    """
        # Use news from entire period
        >>> news = News(category=0)

        # With specific begin and end date
        >>> news = News(category=0, begin_date='2018-01-01', end_date='2018-01-03')

        # With specific begin date and unbounded end date
        >>> news = News(category=0, begin_date='2018-03-01')

        # With unbounded begin date and specific end date
        >>> news = News(category=0, end_date='2018-03-01')
    """

    def __init__(self, category, begin_date=None, end_date=None):
        dirname = newspath_form.format(category)
        self.dirname = dirname
        newspaths = sorted(glob('{}/*.txt'.format(dirname)))
        indexpaths = sorted(glob('{}/*.index'.format(dirname)))

        begin_date, end_date = self._set_dates(newspaths, begin_date, end_date)
        self._check_dates(begin_date, end_date)

        self.newspaths = self._filter_paths(newspaths, begin_date, end_date)
        self.indexpaths = self._filter_paths(indexpaths, begin_date, end_date)
        self.num_docs = [(parse_date(path), line_count(path)) for path in self.indexpaths]

    def _set_dates(self, paths, begin_date, end_date):
        dates = [parse_date(path) for path in paths]
        if begin_date is None:
            begin_date = dates[0]
        if end_date is None:
            end_date = dates[-1]
        return begin_date, end_date

    def _check_dates(self, begin_date, end_date):
        if not check_date_format(begin_date):
            raise ValueError('Check begin_date form: {}'.format(begin_date))
        if not check_date_format(end_date):
            raise ValueError('Check end_date form: {}'.format(end_date))

    def _filter_paths(self, paths, begin_date, end_date):
        paths = [path for path in paths if begin_date <= parse_date(path) <= end_date]
        return paths

    def get_news(self, begin_date=None, end_date=None):
        """
        Arguments
        ---------
        begin_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        end_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        Returns
        ------
        list of str
            A str is a doublespace line format document of a news
        """

        return [doc for doc in self.iter_news(begin_date, end_date)]

    def iter_news(self, begin_date=None, end_date=None):
        """
        Arguments
        ---------
        begin_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        end_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        Yields
        ------
        doc : str
            Doublespace line format document of a news
        """

        begin_date, end_date = self._set_dates(
            self.newspaths, begin_date, end_date)
        self._check_dates(begin_date, end_date)

        for doc in self._iter(self.newspaths, begin_date, end_date):
            yield doc

    def get_index(self, begin_date=None, end_date=None):
        """
        Arguments
        ---------
        begin_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        end_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        Returns
        ------
        list of str
            Each str is tap separated index (press/yy/mm/dd/article, category, date, title)
            For example,
                $ 421/2018/01/02/0003129236	100	2018-01-02 15:53	'NLL 파문' 대화록 유출 수사 빈손…검찰 "기소 없을듯"
        """

        return [index for index in self.iter_index(begin_date, end_date)]

    def iter_index(self, begin_date=None, end_date=None):
        """
        Arguments
        ---------
        begin_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        end_date : str
            yyyy-mm-dd format
            If it is None, use first date of news in dirname
            Default is None
        Yields
        ------
        index : str
            Tap separated index (press/yy/mm/dd/article, category, date, title)
            For example,
                $ 421/2018/01/02/0003129236	100	2018-01-02 15:53	'NLL 파문' 대화록 유출 수사 빈손…검찰 "기소 없을듯"
        """

        begin_date, end_date = self._set_dates(
            self.indexpaths, begin_date, end_date)
        self._check_dates(begin_date, end_date)

        for doc in self._iter(self.indexpaths, begin_date, end_date):
            yield doc

    def _iter(self, paths, begin_date, end_date):
        for path in paths:
            if not (begin_date <= parse_date(path) <= end_date):
                continue
            with open(path, encoding='utf-8') as f:
                for doc in f:
                    yield doc.strip()


def parse_date(path):
    """
    Arguments
    ---------
    path : str
        File path
    Usage
    -----
        >>> path = '/workspace/data/politician/0/news/2013-01-02_politician.index'
        >>> parse_date(path)
        $ '2013-01-02'
    """
    return path.split('/')[-1][:10]

def check_date_format(date):
    """
    Argument
    --------
    date : str
        Datetime

    Returns
    -------
    True if date is yyyy-mm-dd form
    """

    date_regex = re.compile('[\d]{4}-[\d]{2}-[\d]{2}')
    pattern = date_regex.match(date)
    return pattern is not None

def line_count(path):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    n_lines : int
        Number of lines
    """

    n_lines = 0
    with open(path, encoding='utf-8') as f:
        for _ in f:
            n_lines += 1
    return n_lines

def load_docs(path):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    List of str
        Each str is a news article. It uses double space as sentence separator
    """

    with open(path, encoding='utf-8') as f:
        docs = [line.strip() for line in f]
    return docs