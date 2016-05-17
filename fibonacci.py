#!/usr/bin/python

# generators are used to generate a series of values
# yield is like the return of generator functions
# the only other thing yield does is ave the "state" of a generator function
# a generator is just a special type of iterator
# like iterators, once can get the next value from a generator using next(),
# for gets values by calling next() implicitly
"""
When we call a normal Python function, execution starts at function's first line and continues
until a return statement, exception, or the end of the function (which is seen as an implicit return None)
is encountered.
Once a function returns control to its caller, that's it.
Any work done by the function and stored in local variables is lost.
A new call to the function creates everything from scratch.

"return" implies that the function is returning control of execution to the point where the function was called.
"yield," however, implies that the transfer of control is temporary and voluntary, and our function expects to
regain it in the future.
"""


def fib(max_num):
    a, b = 0, 1
    while a < max_num:
        # yield pauses a function
        #
        yield a
        a, b = b, a+b

if __name__ == '__main__':
    import sys
    if sys.argv[1] is not None:
        a = list(fib(int(sys.argv[1])))
        print(a)
