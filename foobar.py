#!/usr/bin/python -tt

import re

class FooBar:
    population = 0

    def __init__(self, name):
        self.name = name
        FooBar.population += 1

    def die(self):
        FooBar.population -= 1
        """I am dying."""
        print("{} is being destroyed!".format(self.name))

        if FooBar.population == 0:
            print("{} was the last one.".format(self.name))
        else:
            print("There are still {:d} robots working.".format(FooBar.population))

    @classmethod
    def how_many(cls):
        """Prints the current population."""
        print("We have {:d} foobars.".format(cls.population))

    def cls_name(self):
        print('Hello, my name is %s' % self.name)

    @classmethod
    def test_greedy(cls, line):
        match = re.search(r'<*?>(\d+)</td><td>([a-zA-Z]+)</td><td>([a-zA-Z]+)</td>', line)
        if match:
            rank, male, female = match.groups()
            print("rank=%s, male=%s, female=%s" % (rank, male, female))
        else:
            print('not match')


def main():
    foobar = FooBar("foo_name")
    foobar.cls_name()
    FooBar.how_many()
    line = '<tr align="right"><td>10</td><td>Joseph</td><td>Lauren</td>'
    FooBar.test_greedy(line)

if __name__ == '__main__':
    main()