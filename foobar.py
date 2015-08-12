#!/usr/bin/python -tt

import os, re, logging, platform

class FooBar:
    population = 0

    def __init__(self, name):
        self.name = name
        self.error_msg = 'no error'
        self.error_code = 0
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
        logging.info("We have {:d} foobars.".format(cls.population))

    def cls_name(self):
        logging.info('Hello, my name is %s' % self.name)

    @classmethod
    def test_greedy(cls, line):
        match = re.search(r'<*?>(\d+)</td><td>([a-zA-Z]+)</td><td>([a-zA-Z]+)</td>', line)
        if match:
            rank, male, female = match.groups()
            logging.info("rank=%s, male=%s, female=%s" % (rank, male, female))
        else:
            logging.info('not match')

    def get_error_details(self):
        return self.error_code, self.error_msg


def main():

    if platform.platform().startswith('Windows'):
        logging_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'), 'test.log')
    else:
        logging_file = os.path.join(os.getenv('HOME'), 'test.log')

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s : %(levelname)s : %(message)s',
        filename=logging_file,
        filemode='w',
    )

    foobar = FooBar("foo_name")
    foobar.cls_name()
    FooBar.how_many()
    line = '<tr align="right"><td>10</td><td>Joseph</td><td>Lauren</td>'
    FooBar.test_greedy(line)
    print(foobar.get_error_details())

    logging.info(line)

if __name__ == '__main__':
    main()

