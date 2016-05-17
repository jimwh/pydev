#!/usr/bin/python

import re
import io


def build_match_and_apply_functions(search_pattern, search_word, replace_char):
    def matches_rule(word):
        return re.search(search_pattern, word)

    def apply_rule(word):
        return re.sub(search_word, replace_char, word)
    return matches_rule, apply_rule

# the rule is a list
# read the entire pattern file and build a list of all the possible rules
#
rules = []
with io.open('plural4-rules.txt', encoding='utf-8') as pattern_file:
    for line in pattern_file:
        # split a line to 3 parts
        # The first argument to the split() method is None,
        # which means split on any whitespace (tabs or spaces, it makes no difference)
        pattern, search, replace = line.split(None, 3)
        fun_tuple = build_match_and_apply_functions(pattern, search, replace)
        rules.append(fun_tuple)


def plural(noun):
    for matches_rule, apply_rule in rules:
        if matches_rule(noun):
            return apply_rule(noun)

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        print(plural(sys.argv[1]))
