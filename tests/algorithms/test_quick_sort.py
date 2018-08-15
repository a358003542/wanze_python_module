#!/usr/bin/env python
# -*-coding:utf-8-*-



import pytest
from bihu.algorithms.sort.selection_sort import selection_sort
from bihu.algorithms.sort.quick_sort import quick_sort, quick_sort2


def test_quick_sort():
    seq = [1, 2, 4, 5, 6, 23, 22]
    assert quick_sort(seq) == [1, 2, 4, 5, 6, 22, 23]


@pytest.mark.skip(reason="i have test it")
def test_sort_timeit():
    import numpy as np
    data = np.random.randn(10000)
    seq = list(data)
    import time

    t1 = time.time()

    quick_sort(seq)
    t2 = time.time()

    selection_sort(seq)
    t3 = time.time()
    print('select_sort use time {0}'.format(t3 - t2))

    print('quick sort use time {0}'.format(t2 - t1))

@pytest.mark.skip(reason="i have test it")
def test_sort_timeit2():
    import numpy as np
    data = np.random.randn(1000000)
    seq = list(data)
    import time

    t1 = time.time()

    quick_sort2(seq)
    t2 = time.time()
    quick_sort(seq)
    t3 = time.time()

    print('quick_sort use time {0}'.format(t3 - t2))
    print('quick_sort2 use time {0}'.format(t2 - t1))


