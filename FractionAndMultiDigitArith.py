#!/usr/bin/env python3

import random
import time
import sys
from fractions import Fraction


def getInt(str):
    """Try and try again to get integer."""
    while True:
        try:
            return int(input(str))
        except:
            pass


def getValidAnswer(string):
    """Try and try again to get a valid answer."""
    while True:
        answer = input(string)
        try:
            if '/' in answer:
                num, denom = answer.split('/')
                return Fraction(int(num), int(denom))
            else:
                return int(answer)
        except:
            pass

def getAndCheckAnswer(string, correctAnswer):
    answer = getValidAnswer(problem)
    if answer == correctAnswer:
        correct += 1
    else:
        wrong += 1
        print ('wrong. the right answer: %s' % (str(correctAnswer)))

def buildIndexArray(distrib):
    """convert dictionary, like {'x':1, 'y':2, 'z':3} to ['x','y','y','z','z','z']
    The purpose is to control the chance of the element. For the array above,
    if we pick random element, 1/6 chance for 'x', 2/6 chance for 'y', and 3/6
    chance for 'z'."""
    indexArr = []
    for k, v in distrib.items():
        indexArr.extend([k] * v)
    return indexArr


def getRandomSingleDigit():
    """get random number, from 0-10 with custom chance distribution."""
    # The keys on the dict below is the number and the value is how likely that
    # number will be selected.
    distrib = {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 2,
        7: 2,
        8: 2,
        9: 2,
    }
    indexArr = buildIndexArray(distrib)
    return indexArr[random.randint(0, len(indexArr) - 1)]


def getRandomSingleDigitFraction():
    """get random fraction single digit."""
    a = getRandomSingleDigit()
    b = getRandomSingleDigit()
    num = min(a, b)
    denom = max(a, b)
    return Fraction(num, denom)


def getProblem():
    """Construct an arithmetic problem. Return (problem-string, answer)."""
    def addInt():
        a = getRandomSingleDigit()
        b = getRandomSingleDigit()
        return ('{} + {} = '.format(a, b), a + b)

    def multInt():
        a = getRandomSingleDigit()
        b = getRandomSingleDigit()
        return ('{} x {} = '.format(a, b), a * b)

    def minusInt():
        a = getRandomSingleDigit()
        b = getRandomSingleDigit()
        big = max(a, b)
        small = min(a, b)
        return ('{} - {} = '.format(big, small), big - small)

    def divInt():
        a = getRandomSingleDigit()
        b = 0
        while b == 0:
            b = getRandomSingleDigit()
        return ('{} / {} = '.format(a * b, b), a)

    def addFraction():
        a = getRandomSingleDigitFraction()
        b = getRandomSingleDigitFraction()
        return ('{} + {} = '.format(str(a), str(b)), a + b)

    def minusFraction():
        a = getRandomSingleDigitFraction()
        b = getRandomSingleDigitFraction()
        big = max(a, b)
        small = min(a, b)
        return ('{} - {} = '.format(str(big), str(small)), big - small)

    def reduceFraction():
        a = getRandomSingleDigitFraction()
        b = getRandomSingleDigit()
        return ('Reduce {}/{} = '.format(a.numerator*b, a.denominator*b), a)

    distrib = {
        #addInt: 1,
        #multInt: 1,
        #divInt: 1,
        #minusInt: 1,
        #addFraction: 1,
        #minusFraction: 1,
        reduceFraction: 1,
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

        getAndCheckAnswer(problem, correctAnswer)

    end = time.time()

    print ('total correct: %d (%.1f%%)' % (correct, correct / total * 100))
    print ('total wrong: %d (%.1f%%)' % (wrong, wrong / total * 100))
    deltaSecs = end - start
    print ('total time: %d minutes %d seconds' % (int(deltaSecs / 60), deltaSecs % 60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
