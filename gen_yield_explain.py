#!/usr/bin/python

def test_one():
    iterator = (x for x in [9, 31, 42, '08/18/2015'])
    for item in iterator:
        print(item)

    ###
    for item in select_item():
        print(item)

def select_item():
    yield 9
    yield 31
    yield 42
    yield '08/18/2015'


if __name__ == '__main__':
    test_one()