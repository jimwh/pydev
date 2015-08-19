#!/usr/bin/python

import random

# A generator function is defined like a normal function, but whenever it needs to generate a value,
# it does so with the yield keyword rather than return. If the body of a def contains yield,
# the function automatically becomes a generator function (even if it also contains a return statement).
#

# generator functions create generator iterators. That's the last time you'll see the term generator iterator,
# though, since they're almost always referred to as "generators". Just remember that a generator is a special
# type of iterator. To be considered an iterator, generators must define a few methods, one of which is __next__().
# To get the next value from a generator, we use the same built-in function as for iterators: next().
#

# This point bears repeating: to get the next value from a generator, we use the same built-in function as for
# iterators: next().
# (next() takes care of calling the generator's __next__() method).
# Since a generator is a type of iterator, it can be used in a for loop.

# So whenever next() is called on a generator, the generator is responsible for passing back a value to whomever
# called next(). It does so by calling yield along with the value to be passed back (e.g. yield 7).
# The easiest way to remember what yield does is to think of it as return (plus a little magic) for generator functions.
#
# Again, yield is just return (plus a little magic) for generator functions.
#
# Magic part: When a generator function calls yield, the "state" of the generator function is frozen;
# the values of all variables are saved and the next line of code to be executed is recorded until next()
# is called again. Once it is, the generator function simply resumes where it left off. If next() is never
# called again, the state recorded during the yield call is (eventually) discarded.
#

def test_one():
    iterator = (x for x in [9, 31, 42, '08/18/2015'])
    for item in iterator:
        print(item)

    ###
    for item in select_item():
        print(item)

    # 1. when you call the function, the code you have written in the function body does not run.
    # 2. the function only returns the generator object
    # 3. your function body will be run each time in the "for ..."
    my_generator = create_generator(3)
    print(my_generator)
    for num in my_generator:
        print(num)


def select_item():
    yield 9
    yield 31
    yield 42
    yield '08/18/2015'

def create_generator(const):
    my_list = [1, 3, 9]
    for num in my_list:
        yield num * const


# When you use send and expression yield in a generator, you're treating it as a co-routine;
# a separate thread of execution that can run sequentially interleaved but not in parallel with its caller.
#
# When the caller executes R = m.send(a), it puts the object a into the generator's input slot,
# transfers control to the generator, and waits for a response.
# The generator receives object a as the result of X = yield i, and runs until it hits another yield expression
# e.g. Y = yield j. Then it puts j into its output slot, transfers control back to the caller, and waits until
# it gets resumed again. The caller receives j as the result of R = m.send(a), and runs until it hits another
# S = m.send(b) statement, and so on.
#

# R = next(m) is just the same as R = m.send(None); it's putting None into the generator's input slot,
# so if the generator checks the result of X = yield i then X will be None.
#


def get_data():
    return random.sample(range(10), 3)

def consume():
    running_sum = 0
    data_items_seen = 0

    while True:
        data = yield
        data_items_seen += len(data)
        running_sum += sum(data)
        print('the running average is {}'.format(running_sum / float(data_items_seen)))


def produce(consumer):
    while True:
        data = get_data()
        print('produced {}'.format(data))
        consumer.send(data)
        yield

def test_two():
    consumer = consume()
    consumer.send(None)
    producer = produce(consumer)
    for _ in range(10):
        print('producing ...')
        next(producer)

if __name__ == '__main__':
    test_one()
    test_two()

"""
    generator:

    # Here you create the method of the node object that will return the generator
    def node._get_child_candidates(self, distance, min_dist, max_dist):
        # Here is the code that will be called each time you use the generator object:
        # If there is still a child of the node object on its left
        # AND if distance is ok, return the next child

        if self._left_child and distance - max_dist < self._median:
            yield self._left_child

        # If there is still a child of the node object on its right
        # AND if distance is ok, return the next child
        if self._right_child and distance + max_dist >= self._median:
            yield self._right_child

        # If the function arrives here, the generator will be considered empty
        # there is no more than two values: the left and the right children

    caller:

    # Create an empty list and a list with the current object reference
    result, candidates = list(), [self]

    # Loop on candidates (they contain only one element at the beginning)
    while candidates:

        # Get the last candidate and remove it from the list
        node = candidates.pop()

        # Get the distance between obj and the candidate
        distance = node._get_dist(obj)

        # If distance is ok, then you can fill the result
        if distance <= max_dist and distance >= min_dist:
            result.extend(node._values)

        # Add the children of the candidate in the candidates list
        # so the loop will keep running until it will have looked
        # at all the children of the children of the children, etc. of the candidate
        candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))

    return result
"""


