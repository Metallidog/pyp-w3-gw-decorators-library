from __future__ import print_function
import signal
import time
from .exceptions import TimeoutError
import logging

def timeout(seconds):
    def decorate(function):
        def wrapper():
            def handler(signum, frame):
                raise TimeoutError("Function call timed out")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            return function()
        return wrapper
    return decorate

def debug(logger=None):
    if logger is None:
        logger = logging.getLogger('tests.test_decorators')
            #'test_decorators.error_logger')
    def decorate(function):
        def wrapper(*args, **kwargs):
            logger.debug('Executing "{}" with params: {}, {}'.format(function.__name__, args, kwargs))
            result = function(*args, **kwargs)
            logger.debug('Finished "{}" execution with result: {}'.format(function.__name__, result))
            return result
        return wrapper
    return decorate


class count_calls(object):
    
    dictionary = {} 
    
    def __init__(self, function):
        self.function = function
        self.function_name = function.__name__
        count_calls.dictionary[self.function_name] = 0
        
    def __call__(self, *args, **kwargs):
        count_calls.dictionary[self.function_name] += 1
        #self.function(*args, **kwargs)
        #return self.function
        
    def counter(self):
        return count_calls.dictionary[self.function_name]
    
    @classmethod    
    def counters(cls):
        return cls.dictionary
        
    @classmethod
    def reset_counters(cls):
        cls.dictionary = {}
 
class memoized():
    def __init__(self, function):
        self.function = function
        self.cache = {}
    
    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.function(*args)
            self.cache[args] = result
            return result
