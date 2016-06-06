#!/usr/bin/python

class Properties:

    def __init__(self):
        self.__props = {}

    def load(self, name):
        stream = open(name)
        for line in stream:
            if not line:
                continue
            if line[0] == '#':
                continue
            if line[0] == '\n':
                continue

            (name, value) = line.replace('\n', '').split('=')
            if not name:
                continue
            if name == '\n':
                continue
            if not value:
                continue
            self.__props[name] = value
        stream.close()

    def get(self, key):
        return self.__props.get(key)

    def print_list(self):
        for key in self.__props.keys():
            print('%s = %s\n' % (key, self.__props[key]))

    def get_dict(self):
        return self.__props


if __name__ == "__main__":
    p = Properties()
    p.load('test2.properties')
    props = p.get_dict()
    print(len(props))
    p.print_list()
    print(len(p.get('abc')))
