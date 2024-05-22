#!/usr/bin/python3

def double_print(in_string, out_fh):
    """
    Take in a string, and both print the string, and write it to a file.
    """
    print(in_string)
    out_fh.write(in_string + "\n")
