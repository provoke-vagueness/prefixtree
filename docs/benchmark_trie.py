"""Test memory consumption and processing time with PrefixDict.

Use words from '/usr/share/dict/words' as keys for PrefixDict and measure
memory consumption and load time.
"""
import resource
import sys

from prefixtree import PrefixDict


if __name__ == '__main__':
    start = resource.getrusage(resource.RUSAGE_SELF)
    glossary = PrefixDict()
    with open('/usr/share/dict/words') as words:
        for word in words:
            glossary[word.strip()] = None
    stop = resource.getrusage(resource.RUSAGE_SELF)
    rss_mb = (stop.ru_maxrss- start.ru_maxrss) / 1024.0 / 1024.0
    tused = (stop.ru_utime + stop.ru_stime)
    sys.stdout.write('{0} MB\n'.format(rss_mb))
    sys.stdout.write('{0} seconds\n'.format(tused))
