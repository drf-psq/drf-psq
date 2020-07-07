# -*- coding: utf-8 -*-

from functools import reduce
import inspect


class Rule(object):

    def __init__(self, permission_classes=None, serializer_class=None,
                 queryset=None, get_obj=None):
        self.permission_classes = permission_classes
        self.serializer_class = serializer_class
        self.queryset = queryset
        self.get_obj = get_obj



def and_permissions(permission_classes):
    return reduce(lambda a ,b: a & b, permission_classes)


def get_caller_name():
    return inspect.currentframe().f_back.f_back.f_code.co_name
    # return sys._getframe().f_back.f_back.f_code.co_name
