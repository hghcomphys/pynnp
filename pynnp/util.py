"""Util"""

def read_and_tokenize_line(in_file):
    return next(in_file).rstrip("/n").split()