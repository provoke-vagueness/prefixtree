"""Test memory consumption and processing time with builtin dict.

Use all 3 character permutations of ASCII letters as keys for dict and measure
memory consumption and load time.
"""
import itertools
import resource
import string
import sys


if __name__ == '__main__':
    letters = []
    for i in range(len(string.ascii_letters)):
        letters.append(string.ascii_letters[i:i+1].encode('ascii'))
    start = resource.getrusage(resource.RUSAGE_SELF)
    glossary = {}
    for word in itertools.permutations(letters, 3):
        glossary[b''.join(word)] = None
    stop = resource.getrusage(resource.RUSAGE_SELF)
    rss_mb = stop.ru_maxrss - start.ru_maxrss
    tused = stop.ru_utime + stop.ru_stime
    sys.stdout.write('{0}\n'.format(rss_mb))
    sys.stdout.write('{0}\n'.format(tused))
