#!/usr/bin/env python3

import random
import time
import sys


def getInt(str):
    """Try and try again to get integer."""
    while True:
        try:
            return int(input(str))
        except:
            pass


def buildIndexArray(distrib):
    """convert dictionary, like {'x':1, 'y':2, 'z':3} to ['x','y','y','z','z','z']
    The purpose is to control the chance of the element. For the array above,
    if we pick random element, 1/6 chance for 'x', 2/6 chance for 'y', and 3/6
    chance for 'z'."""
    indexArr = []
    for k, v in distrib.items():
        indexArr.extend([k] * v)
    return indexArr


def getRandomNumber():
    """get random number, from 0-10 with custom chance distribution."""
    # The keys on the dict below is the number and the value is how likely that
    # number will be selected.
    distrib = {
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 3,
        8: 4,
        9: 3,
        10: 1,
    }
    indexArr = buildIndexArray(distrib)
    return indexArr[random.randint(0, len(indexArr) - 1)]


def getProblem():
    """Construct an arithmetic problem. Return (problem-string, answer)."""
    def add():
        a = getRandomNumber()
        b = getRandomNumber()
        return ('{} + {} = '.format(a, b), a + b)

    def mult():
        a = getRandomNumber()
        b = getRandomNumber()
        return ('{} x {} = '.format(a, b), a * b)

    def minus():
        a = getRandomNumber()
        b = getRandomNumber()
        big = max(a, b)
        small = min(a, b)
        return ('{} - {} = '.format(big, small), big - small)

    def divide():
        a = getRandomNumber()
        b = 0
        while b == 0:
            b = getRandomNumber()
        return ('{} / {} = '.format(a * b, b), a)

    distrib = {
        add: 1,
        mult: 2,
        divide: 2,
        minus: 1,
    }
    indexArr = buildIndexArray(distrib)
    return indexArr[random.randint(0, len(indexArr) - 1)]()


def main():
    """Start the arithmetics!!"""
    random.seed()
    total = getInt('total number of questions: ')
    correct = 0
    wrong = 0

    start = time.time()

    for i in range(0, total):
        (problem, correctAnswer) = getProblem()

        answer = getInt(problem)
        if answer == correctAnswer:
            correct += 1
        else:
            wrong += 1
            print ('wrong. the right answer: %d' % (correctAnswer))

    end = time.time()

    print ('total correct: %d (%.1f%%)' % (correct, correct / total * 100))
    print ('total wrong: %d (%.1f%%)' % (wrong, wrong / total * 100))
    deltaSecs = end - start
    print ('total time: %d minutes %d seconds' % (int(deltaSecs / 60), deltaSecs % 60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
