#!/usr/bin/python3

def double_print(in_string, out_fh):
    print(in_string)
    out_fh.write(in_string + "\n")