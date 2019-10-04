#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
from itertools import chain, combinations

from mymodule.nlp.zhnumber import int_zhnumber

logger = logging.getLogger(__name__)


def guess_chapter_id(string, ):
    g = re.search(r'第([\d\s]+)章', string)

    if g:
        try:
            chapter_id = int(g.group(1))
            return chapter_id
        except Exception as e:
            return 0

    g = re.search(r'第([零一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬\s]+)章', string)

    if g:
        try:
            chapter_id = int_zhnumber(g.group(1))
            return chapter_id
        except Exception as e:
            return 0

    logger.warning('interpreter chapter id failed {0}'.format(string))
    return 0


##########################################################################
# learn from nltk
# Ngram iteration
##########################################################################

def pad_sequence(sequence, n, pad_left=False, pad_right=False,
                 left_pad_symbol=None, right_pad_symbol=None):
    """
    Returns a padded sequence of items before ngram extraction.

        >>> list(pad_sequence([1,2,3,4,5], 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
        ['<s>', 1, 2, 3, 4, 5, '</s>']
        >>> list(pad_sequence([1,2,3,4,5], 2, pad_left=True, left_pad_symbol='<s>'))
        ['<s>', 1, 2, 3, 4, 5]
        >>> list(pad_sequence([1,2,3,4,5], 2, pad_right=True, right_pad_symbol='</s>'))
        [1, 2, 3, 4, 5, '</s>']

    :param sequence: the source data to be padded
    :type sequence: sequence or iter
    :param n: the degree of the ngrams
    :type n: int
    :param pad_left: whether the ngrams should be left-padded
    :type pad_left: bool
    :param pad_right: whether the ngrams should be right-padded
    :type pad_right: bool
    :param left_pad_symbol: the symbol to use for left padding (default is None)
    :type left_pad_symbol: any
    :param right_pad_symbol: the symbol to use for right padding (default is None)
    :type right_pad_symbol: any
    :rtype: sequence or iter
    """
    sequence = iter(sequence)
    if pad_left:
        sequence = chain((left_pad_symbol,) * (n - 1), sequence)
    if pad_right:
        sequence = chain(sequence, (right_pad_symbol,) * (n - 1))
    return sequence


def ngrams(sequence, n, pad_left=False, pad_right=False,
           left_pad_symbol=None, right_pad_symbol=None):
    """
    Return the ngrams generated from a sequence of items, as an iterator.
    For example:

        >>> list(ngrams([1,2,3,4,5], 3))
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    Wrap with list for a list version of this function.  Set pad_left
    or pad_right to true in order to get additional ngrams:

        >>> list(ngrams([1,2,3,4,5], 2, pad_right=True))
        [(1, 2), (2, 3), (3, 4), (4, 5), (5, None)]
        >>> list(ngrams([1,2,3,4,5], 2, pad_right=True, right_pad_symbol='</s>'))
        [(1, 2), (2, 3), (3, 4), (4, 5), (5, '</s>')]
        >>> list(ngrams([1,2,3,4,5], 2, pad_left=True, left_pad_symbol='<s>'))
        [('<s>', 1), (1, 2), (2, 3), (3, 4), (4, 5)]
        >>> list(ngrams([1,2,3,4,5], 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
        [('<s>', 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, '</s>')]


    :param sequence: the source data to be converted into ngrams
    :type sequence: sequence or iter
    :param n: the degree of the ngrams
    :type n: int
    :param pad_left: whether the ngrams should be left-padded
    :type pad_left: bool
    :param pad_right: whether the ngrams should be right-padded
    :type pad_right: bool
    :param left_pad_symbol: the symbol to use for left padding (default is None)
    :type left_pad_symbol: any
    :param right_pad_symbol: the symbol to use for right padding (default is None)
    :type right_pad_symbol: any
    :rtype: sequence or iter
    """
    sequence = pad_sequence(sequence, n, pad_left, pad_right,
                            left_pad_symbol, right_pad_symbol)

    history = []
    while n > 1:
        history.append(next(sequence))
        n -= 1
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]


def bigrams(sequence, **kwargs):
    """
    Return the bigrams generated from a sequence of items, as an iterator.
    For example:

        >>> list(bigrams([1,2,3,4,5]))
        [(1, 2), (2, 3), (3, 4), (4, 5)]

    Use bigrams for a list version of this function.

    :param sequence: the source data to be converted into bigrams
    :type sequence: sequence or iter
    :rtype: iter(tuple)
    """

    for item in ngrams(sequence, 2, **kwargs):
        yield item


def trigrams(sequence, **kwargs):
    """
    Return the trigrams generated from a sequence of items, as an iterator.
    For example:

        >>> list(trigrams([1,2,3,4,5]))
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    Use trigrams for a list version of this function.

    :param sequence: the source data to be converted into trigrams
    :type sequence: sequence or iter
    :rtype: iter(tuple)
    """

    for item in ngrams(sequence, 3, **kwargs):
        yield item


def skipgrams(sequence, n, k, **kwargs):
    """
    Returns all possible skipgrams generated from a sequence of items, as an iterator.
    Skipgrams are ngrams that allows tokens to be skipped.
    Refer to http://homepages.inf.ed.ac.uk/ballison/pdf/lrec_skipgrams.pdf

        >>> sent = "Insurgents killed in ongoing fighting".split()
        >>> list(skipgrams(sent, 2, 2))
        [('Insurgents', 'killed'), ('Insurgents', 'in'), ('Insurgents', 'ongoing'), ('killed', 'in'), ('killed', 'ongoing'), ('killed', 'fighting'), ('in', 'ongoing'), ('in', 'fighting'), ('ongoing', 'fighting')]
        >>> list(skipgrams(sent, 3, 2))
        [('Insurgents', 'killed', 'in'), ('Insurgents', 'killed', 'ongoing'), ('Insurgents', 'killed', 'fighting'), ('Insurgents', 'in', 'ongoing'), ('Insurgents', 'in', 'fighting'), ('Insurgents', 'ongoing', 'fighting'), ('killed', 'in', 'ongoing'), ('killed', 'in', 'fighting'), ('killed', 'ongoing', 'fighting'), ('in', 'ongoing', 'fighting')]

    :param sequence: the source data to be converted into trigrams
    :type sequence: sequence or iter
    :param n: the degree of the ngrams
    :type n: int
    :param k: the skip distance
    :type  k: int
    :rtype: iter(tuple)
    """

    # Pads the sequence as desired by **kwargs.
    if 'pad_left' in kwargs or 'pad_right' in kwargs:
        sequence = pad_sequence(sequence, n, **kwargs)

    # Note when iterating through the ngrams, the pad_right here is not
    # the **kwargs padding, it's for the algorithm to detect the SENTINEL
    # object on the right pad to stop inner loop.
    SENTINEL = object()
    for ngram in ngrams(sequence, n + k, pad_right=True, right_pad_symbol=SENTINEL):
        head = ngram[:1]
        tail = ngram[1:]
        for skip_tail in combinations(tail, n - 1):
            if skip_tail[-1] is SENTINEL:
                continue
            yield head + skip_tail


def multi_delimiter_split(string, delimiters='', split_whitespace=True, remove_whitespace=True):
    """
    多个分隔符分割字符串，

    delimiters = ';,'
    split_whitespace 是否加上按照空白分割   默认是按照空白分割
    remove_whitespace 是否移除分隔符两边多余的空白字符 默认移除


    """
    expr_one = '\s' if split_whitespace else ''

    expr = '[{0}{1}]'.format(delimiters, expr_one)

    if remove_whitespace:
        expr = '\s*' + expr + '\s*'

    res = re.split(expr, string)

    return res
