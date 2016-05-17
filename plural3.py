#!/usr/bin/python

import re

# return a tuple with two values: match and apply
# build_match_and_apply_functions(pattern, search, replace) within a dynamic function is called closures.
#


def build_match_and_apply_functions(pattern, search, replace):
    def matches_rule(word):
        return re.search(pattern, word)

    def apply_rule(word):
        return re.sub(search, replace, word)

    return matches_rule, apply_rule


patterns = \
    (
        ('[sxz]$',           '$',  'es'),
        ('[^aeioudgkprt]h$', '$',  'es'),
        ('(qu|[^aeiou])y$',  'y$', 'ies'),
        ('$',                '$',  's')
    )

# list comprehensions
rules = [build_match_and_apply_functions(pattern, search, replace)
         for (pattern, search, replace) in patterns]


def plural(noun):
    for matches_rule, apply_rule in rules:
        if matches_rule(noun):
            return apply_rule(noun)

if __name__ == '__main__':
    import sys
    num = [1, 2, 3, 4]
    list_num = [elem * 2 for elem in num]
    print(list_num)

    if sys.argv[1:]:
        print(plural(sys.argv[1]))