#!/usr/bin/python

import javaobj
import logging

def read_file(filename):
    file = open(filename, 'rb')
    return file.read()

def main():
    jobj = read_file("./iacucTaskForm1177842_1182605.ser")
    pobj = javaobj.loads(jobj)
    print(pobj)

if __name__ == '__main__':
    main()
