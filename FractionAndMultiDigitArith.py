#!/usr/bin/env python3

import random
import time
import sys
import re
from fractions import Fraction
from decimal import Decimal


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
        answer = input(string).strip()
        try:
            if '/' in answer:
                num, denom = [i.strip() for i in answer.split('/')]
                denom = int(denom)
                temp = re.split(' +', num)
                if len(temp) == 1:
                    whole = 0
                else:
                    whole, num = [int(i.strip()) for i in temp]
                value = Fraction(num + (whole * denom), denom)
                if int(whole) != 0:
                    return ('{} {}/{}'.format(whole, num, denom), value)
                else:
                    return ('{}/{}'.format(num, denom), value)
            if '.' in answer:
                return (answer, Decimal(answer))
            else:
                return (answer, int(answer))
        except:
            pass  # invalid input, try again


def fractionToMixedNumString(f):
    """Return mixed number string given any fraction number."""
    if f.numerator > f.denominator and f.denominator != 1:
        return '{} {}/{}'.format(f.numerator // f.denominator,
                                 f.numerator % f.denominator,
                                 f.denominator)
    else:
        return str(f)


def buildIndexArray(distrib):
    """Convert dictionary, like {'x':1, 'y':2, 'z':3} to ['x','y','y','z','z','z']
    The purpose is to control the chance of the element. For the array above,
    if we pick random element, 1/6 chance for 'x', 2/6 chance for 'y', and 3/6
    chance for 'z'."""
    indexArr = []
    for k, v in distrib.items():
        indexArr.extend([k] * v)
    return indexArr


def getRandomSingleDigit():
    """Get random number, from 0-10 with custom chance distribution."""
    # The keys on the dict below is the number and the value is how likely that
    # number will be selected.
    distrib = {
        0: 1,
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
    """Get random fraction single digit."""
    a = random.randint(1,9)
    b = random.randint(1,9)
    num = min(a, b)
    denom = max(a, b)
    return Fraction(num, denom)


def getRandomSingleDigitMixedFraction():
    """Get random fraction single digit."""
    a = random.randint(1,50)
    b = random.randint(1,20)
    return Fraction(a, b)


def getRandomDecimal():
    """Get decimal number."""
    numWhole = random.randint(1,2)
    numDec = random.randint(0,2)
    whole = ''.join([str(getRandomSingleDigit()) for i in range(numWhole)])
    dec = ''.join([str(getRandomSingleDigit()) for i in range(numWhole)])
    return Decimal(whole + '.' + dec)


def makeAdd(getNumFunc, printNumFunc):
    """Return add function."""
    def add():
        a = getNumFunc()
        b = getNumFunc()
        return ('{} + {} = '.format(printNumFunc(a), printNumFunc(b)), a + b)
    return add


def makeMult(getNumFunc, printNumFunc):
    """Return multiply function."""
    def mult():
        a = getNumFunc()
        b = getNumFunc()
        return ('{} x {} = '.format(printNumFunc(a), printNumFunc(b)), a * b)
    return mult


def makeSub(getNumFunc, printNumFunc):
    """Return subtraction function."""
    def sub():
        a = getNumFunc()
        b = getNumFunc()
        big = max(a, b)
        small = min(a, b)
        return ('{} - {} = '.format(printNumFunc(big), printNumFunc(small)), big - small)
    return sub


def makeDiv(getNumFunc, printNumFunc):
    """Return division function."""
    def div():
        a = getNumFunc()
        b = 0
        while b == 0:
            b = getNumFunc()
        return ('{} / {} = '.format(printNumFunc(a * b), printNumFunc(b)), printNumFunc(a))
    return div


def reduceFraction():
    """Create reduce fraction problem."""
    a = getRandomSingleDigitFraction()
    b = random.randint(1,9)
    return ('Reduce {}/{} = '.format(a.numerator*b, a.denominator*b), a)


def getProblem():
    """Construct an arithmetic problem. Return (problem-string, answer)."""
    distrib = {
        #makeMult(getRandomSingleDigit, str): 1
        #makeDiv(getRandomSingleDigit, str): 1
        #reduceFraction: 1,
        #makeAdd(getRandomSingleDigitFraction, fractionToMixedNumString): 1
        #makeSub(getRandomSingleDigitMixedFraction, fractionToMixedNumString): 1
        makeAdd(getRandomDecimal, str): 1
    }
    indexArr = buildIndexArray(distrib)
    return indexArr[random.randint(0, len(indexArr) - 1)]()


def main():
    """Start the arithmetics!!"""
    random.seed()
    print('Math Practice')
    print('Answers can be:')
    print('* integers (e.g. 11, 121)')
    print('* decimals (e.g. 2.34, 1000.354)')
    print('* mixed fraction (e.g. 3 3/4, 234 1/2). Fraction answers must be reduced')
    print('')
    total = getInt('total number of questions: ')
    correct = 0
    wrong = 0

    start = time.time()

    for i in range(0, total):
        (problemString, correctAnswer) = getProblem()
        (answerString, answerValue) = getValidAnswer(problemString)
        if answerValue == correctAnswer:
            if type(answerValue) in [int, Decimal]:
                correct += 1
            if type(answerValue) == Fraction:
                if answerString == fractionToMixedNumString(correctAnswer):
                    correct += 1
                else:
                    wrong += 1
                    print ('The answer is correct, but not reduced correctly. The proper answer: {}'.format(fractionToMixedNumString(correctAnswer)))
        else:
            wrong += 1
            print ('wrong. the right answer: %s' % (str(correctAnswer)))

    end = time.time()

    print ('total correct: %d (%.1f%%)' % (correct, correct / total * 100))
    print ('total wrong: %d (%.1f%%)' % (wrong, wrong / total * 100))
    deltaSecs = end - start
    print ('total time: %d minutes %d seconds' % (int(deltaSecs / 60), deltaSecs % 60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
