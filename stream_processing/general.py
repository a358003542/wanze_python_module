#!/usr/bin/env python
# -*-coding:utf-8-*-

from functools import reduce


def build_compose_function(*funcs):
    """
    组件一个符合函数流对象 数据处理流模式

    每个函数的参数是任意的 但严格意义上一个合格的数据流管道设计应该在进口数据格式和入口数据格式上做出一些规范

    现在做出如下规范 入口是字典格式 出口也是字典格式 当然内核更细小的粒度的函数不做如此要求，这个只是数据处理流那边
    :param args:
    :return:
    """
    return reduce(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)), funcs)


def build_stream_function(*funcs):
    """
    构建流处理函数 函数参数更严格 只接受一个参数 d 字典值
    :param funcs:
    :return:
    """

    return reduce(lambda f, g: lambda d: f(g(d)), funcs)
