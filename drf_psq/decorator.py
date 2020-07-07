# -*- coding: utf-8 -*-


def psq(psq_rules=[]):
    def decorator(func):
        if (type(psq_rules) is list) and (len(psq_rules)):
            func.psq_rules = psq_rules
        return func
    return decorator
