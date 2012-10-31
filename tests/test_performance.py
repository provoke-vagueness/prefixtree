from __future__ import print_function
import os
import subprocess
import sys

try:
    # python 2.x
    import unittest2 as unittest
    PENALTY_MEM = 10
    PENALTY_CPU = 100
except ImportError:
    # python 3.x
    import unittest
    PENALTY_MEM = 10
    PENALTY_CPU = 150


enableIf = unittest.skipIf(
        os.getenv('PREFIXTREE_PERF') is None and sys.version_info[:2] > (2, 6),
        'Set PREFIXTREE_PERF environment variable to run performance tests')


def run_benchmark(script):
    cmd = ['PYTHONPATH=. {0} {1}'.format(sys.executable, script)]
    output = subprocess.check_output(cmd, shell=True)
    mem, time = output.split()
    return float(mem), float(time)


class TestPerformance(unittest.TestCase):

    def _benchmark(self):
        mem_dict, cpu_dict = run_benchmark('tests/benchmark_dict.py')
        TestPerformance._cpu_dict = cpu_dict
        TestPerformance._mem_dict = mem_dict
        mem_trie, cpu_trie = run_benchmark('tests/benchmark_trie.py')
        TestPerformance._cpu_trie = cpu_trie
        TestPerformance._mem_trie = mem_trie

    @property
    def cpu_dict(self):
        if not hasattr(TestPerformance, '_cpu_dict'):
            self._benchmark()
        return TestPerformance._cpu_dict

    @property
    def cpu_trie(self):
        if not hasattr(TestPerformance, '_cpu_trie'):
            self._benchmark()
        return TestPerformance._cpu_trie

    @property
    def mem_dict(self):
        if not hasattr(TestPerformance, '_mem_dict'):
            self._benchmark()
        return TestPerformance._mem_dict

    @property
    def mem_trie(self):
        if not hasattr(TestPerformance, '_mem_trie'):
            self._benchmark()
        return TestPerformance._mem_trie

    @enableIf
    def test_cpu_performance(self):
        self.assertLess(self.cpu_trie, PENALTY_CPU * self.cpu_dict)

    @enableIf
    def test_mem_performance(self):
        self.assertLess(self.mem_trie, PENALTY_MEM * self.mem_dict)


if __name__ == '__main__':
    mem_dict, cpu_dict = run_benchmark('tests/benchmark_dict.py')
    mem_trie, cpu_trie = run_benchmark('tests/benchmark_trie.py')
    mem_factor = mem_trie / mem_dict
    mem_status = 'GOOD' if mem_factor < PENALTY_MEM else 'BAD'
    cpu_factor = cpu_trie / cpu_dict
    cpu_status = 'GOOD' if cpu_factor < PENALTY_CPU else 'BAD'
    print('{0} memory impact ({1})'.format(mem_factor, mem_status))
    print('{0} cpu impact ({1})'.format(cpu_factor, cpu_status))
