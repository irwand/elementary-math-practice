#!/usr/bin/env python3

import random
import time
import sys
import re
from fractions import Fraction
from decimal import Decimal


OPERATIONS = ['+', '-', 'x', '/']


def printNum(val):
    if type(val) == Fraction:
        return fractionToMixedNumString(val)
    else:
        return str(val)


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
                    whole, num = 0, int(temp[0])
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
            pass


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


def getWeightedRandomSingleDigit():
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
    selectedNum = indexArr[random.randint(0, len(indexArr) - 1)]
    return (str(selectedNum), selectedNum)


def getRandomSingleDigitFraction():
    """Get random fraction single digit."""
    a = random.randint(1,9)
    b = a
    while b == a:
        b = random.randint(1,9)
    num = min(a, b)
    denom = max(a, b)
    return (fractionToMixedNumString(Fraction(num, denom)), Fraction(num, denom))


def make_getWeightedRandomMultiDigit(minimum, maximum = None):
    def getWeightedRandomMultiDigit():
        upper = maximum if maximum else minimum
        numdigits = random.randint(minimum, upper)
        l = []
        for i in range(numdigits):
            l.append(getWeightedRandomSingleDigit())
        s = ''.join([i[0] for i in l])
        return (s, int(s))
    return getWeightedRandomMultiDigit


def getRandomSingleDigitMixedFraction():
    """Get random fraction single digit."""
    a = random.randint(1,50)
    b = random.randint(1,20)
    return (fractionToMixedNumString(Fraction(a, b)), Fraction(a, b))


def getRandomDecimal():
    """Get decimal number."""
    numWhole = random.randint(1,3)
    whole = ''.join([getWeightedRandomSingleDigit()[0] for i in range(numWhole)])
    numDec = random.randint(1,3)
    dec = ''
    if numDec:
        dec = '.' + ''.join([getWeightedRandomSingleDigit()[0] for i in range(numDec)])
    s = whole + dec
    return (s, Decimal(s))


def makeAdd(getNumFunc):
    """Return add function."""
    def add():
        (aStr, aVal) = getNumFunc()
        (bStr, bVal) = getNumFunc()
        if set(aStr).intersection(set(OPERATIONS)):
            aStr = '( ' + aStr + ' )'
        if set(bStr).intersection(set(OPERATIONS)):
            bStr = '( ' + bStr + ' )'
        return ('{} + {}'.format(aStr, bStr), aVal + bVal)
    return add


def makeMult(getNumFunc):
    """Return multiply function."""
    def mult():
        (aStr, aVal) = getNumFunc()
        (bStr, bVal) = getNumFunc()
        if set(aStr).intersection(set(OPERATIONS)):
            aStr = '( ' + aStr + ' )'
        if set(bStr).intersection(set(OPERATIONS)):
            bStr = '( ' + bStr + ' )'
        return ('{} x {}'.format(aStr, bStr), aVal * bVal)
    return mult


def makeSub(getNumFunc):
    """Return subtraction function."""
    def sub():
        nums = [getNumFunc(), getNumFunc()]
        nums.sort(key=lambda i: i[1])
        for i,e in enumerate(nums):
            if set(e[0]).intersection(set(OPERATIONS)):
                nums[i] = ('( ' + e[0] + ' )', e[1])
        return ('{} - {}'.format(nums[1][0], nums[0][0]), nums[1][1] - nums[0][1])
    return sub


def makeDiv(getNumFunc):
    """Return division function."""
    def div():
        (aStr, aVal) = getNumFunc()
        (bStr, bVal) = ('0', 0)
        while bVal == 0:
            (bStr, bVal) = getNumFunc()
        if set(aStr).intersection(set(OPERATIONS)):
            aStr = '( ' + aStr + ' )'
        if set(bStr).intersection(set(OPERATIONS)):
            bStr = '( ' + bStr + ' )'
        return ('{} / {}'.format(aStr, bStr), aVal/bVal)
    return div


def mixedOpAddSubInt():
    """Return mixed operations with add/sub to be the main op."""
    def getMultDiv():
        distrib = {
            makeMult(make_getWeightedRandomMultiDigit(2)): 2,
            makeDivInt(make_getWeightedRandomMultiDigit(2)): 1,
        }
        indexArr = buildIndexArray(distrib)
        return indexArr[random.randint(0, len(indexArr) - 1)]()

    distrib = {
            makeAdd(getMultDiv): 1,
            makeSub(getMultDiv): 1,
        }
    indexArr = buildIndexArray(distrib)
    return indexArr[random.randint(0, len(indexArr) - 1)]()


def makeMixedOpAddSubFracDec(getNumFunc):
    """Return mixed operations with add/sub to be the main op."""
    def getMultDiv():
        distrib = {
            makeMult(getNumFunc): 1,
            makeDivInt(getNumFunc): 1,
        }
        indexArr = buildIndexArray(distrib)
        return indexArr[random.randint(0, len(indexArr) - 1)]()

    def mixedOpAddSubFracDec():
        distrib = {
                makeAdd(getMultDiv): 1,
                makeSub(getMultDiv): 1,
            }
        indexArr = buildIndexArray(distrib)
        return indexArr[random.randint(0, len(indexArr) - 1)]()
    return mixedOpAddSubFracDec

def makeDivInt(getNumFunc):
    def div():
        (aStr, aVal) = getNumFunc()
        (bStr, bVal) = getNumFunc()
        while not bVal:
            (bStr, bVal) = getNumFunc()
        return ('{} / {}'.format(str(aVal * bVal), bStr), aVal)
    return div


def reduceFraction():
    """Create reduce fraction problem."""
    (aStr, aVal) = getRandomSingleDigitFraction()
    b = random.randint(2,10)
    return ('Reduce {}/{}'.format(aVal.numerator*b, aVal.denominator*b), aVal)


def reduceToMixedNumber():
    """Create reduce to mixed number problem."""
    num = random.randint(1,999)
    denom = random.randint(1,12)
    return ('Reduce to mixed number {}/{}'.format(str(num), str(denom)), Fraction(num, denom))


def getProblem():
    """Construct an arithmetic problem. Return (problem-string, answer)."""
    distrib = {
        # makeMult(make_getWeightedRandomMultiDigit(2)): 1,
        # makeDivInt(getWeightedRandomSingleDigit): 1,
        # reduceFraction: 1,
        reduceToMixedNumber: 1,
        # makeAdd(getRandomSingleDigitFraction): 1,
        # makeSub(getRandomSingleDigitMixedFraction): 1,
        # makeAdd(getRandomDecimal): 1,
        # makeSub(getRandomDecimal): 1,
        mixedOpAddSubInt: 1,
        makeMixedOpAddSubFracDec(getRandomSingleDigitFraction): 1,
        makeMixedOpAddSubFracDec(getRandomSingleDigitMixedFraction): 1,
        makeMixedOpAddSubFracDec(getRandomDecimal): 1,
        makeDivInt(make_getWeightedRandomMultiDigit(2)): 1,
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
    print('* mixed fraction (e.g. 1/2, 1 3/4, 234 12/13). Fraction answers must be reduced')
    print('')
    total = getInt('total number of questions: ')
    correct = 0
    wrong = 0

    start = time.time()

    for i in range(0, total):
        (problemString, correctAnswer) = getProblem()
        problemString += ' = '
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
            print ('wrong. the right answer: %s' % (printNum(correctAnswer)))

    end = time.time()

    print ('total correct: %d (%.1f%%)' % (correct, correct / total * 100))
    print ('total wrong: %d (%.1f%%)' % (wrong, wrong / total * 100))
    deltaSecs = end - start
    print ('total time: %d minutes %d seconds' % (int(deltaSecs / 60), deltaSecs % 60))
    input('press <Enter> to quit program...')
    return 0


if __name__ == '__main__':
    sys.exit(main())
