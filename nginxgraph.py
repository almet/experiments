from collections import namedtuple
from datetime import datetime
from itertools import groupby
from operator import attrgetter
import re
import sys

import pylab as pl

Log = namedtuple("Log", ("url", "date", "ip", "status", "verb"))

def parse_line(line):
    """Given a line, parse it and return a namedtuple object matching it"""
    match = re.search(r"^(?P<ip>[0-9\.]+).*?\[(?P<date>.*?) \+.*?\].*?\"(?P<verb>[A-Z]+) (?P<url>.*?) .*?\" (?P<status>[0-9]+)", line)
    if match:
        data = match.groupdict()
        data['date'] = datetime.strptime(data['date'], "%d/%b/%Y:%H:%M:%S")
        return Log(**data)
    return None


def gather_data(*filenames):
    """Gather data from the given nginx logfiles. 
    Returns a list of Log objects.
    """

    # gather data
    data = []
    for filename in filenames:
        print "analysing %s" % filename
        with open(filename) as f:
            for line in f:
                log = parse_line(line)
                if log:
                    data.append(log)

    return data

def analyze(data, filename):

    # graph
    fig = pl.figure()
    ax = fig.add_subplot(111)

    # number of hits + 404 per month
    ids, hits, _404 = [], [], []
    for idx, (month, views) in enumerate(groupby(data, attrgetter("date.year", "date.month"))):
        ids.append(idx)
        views_ = list(views)
        hits.append(len(views_))
        _404.append(len([v for v in views_ if v.status == "404"]))

    ax.plot(ids, hits)
    ax.plot(ids, _404, 'r--')

    fig.savefig(filename)

analyze(gather_data(*sys.argv[1:]), "nginx-logs.png")
