# https://github.com/kamyu104/GoogleCodeJam-2019/blob/master/World%20Finals/wont-sum-must-now.py
# Copyright (c) 2019 kamyu. All rights reserved.
#
# Google Code Jam 2019 World Finals - Problem C. Won't sum? Must now
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000051708/000000000016c77e
#
# Time:  O(2^(D/2) * D), D is the number of digits of S
# Space: O(D)
#

from itertools import imap

def to_int(x):  # list of ints to int
    return int("".join(map(str, x)))

def to_list(X):  # int to list of ints
    return map(int, list(str(X)))

def gen_palindromes(S):
    # at most 208 times because the smallest palindrome of triples
    # is at most 10801 (208-th smallest palindrome) in this problem
    l, n = 1, None
    while True:
        lefts = [""] if n is None else imap(str, xrange(n, 10*n))
        for left in lefts:
            mids = [""] if l%2 == 0 else imap(str, xrange(10))
            for mid in mids:
                P = int(left + mid + left[::-1])
                if P > S:
                    return
                yield P
        if l%2 == 1:
            n = 1 if n is None else n*10
        l += 1

def set_digits(x, o, start):
    for i in xrange(len(o)):
        if x[start+i] is not None and x[start+i] != o[i]:
            return False
        x[start+i], x[-1-(start+i)] = o[i], o[i]
    return True

def clear_digits(x, o, start):
    for i in xrange(len(o)):
        x[start+i], x[-1-(start+i)] = None, None

def find_pair_with_same_length(s, x, y, start, left_carry, right_carry):
    def gen_X_Y():
        for Y in xrange(max(target-9, 0), min(target+1, 10)):  # make X >= Y
            X = target-Y
            if start == 0 and (X == 0 or Y == 0):  # leading digit can't be 0
                continue
            yield X, Y

    if len(x)-start*2 <= 0:
        return left_carry == right_carry
    for new_left_carry in xrange(2):
        target = s[len(x)-1-start] + left_carry*10 - new_left_carry
        if s[start] != (target+right_carry)%10:
            continue
        new_right_carry = right_carry if len(x)-start*2 == 1 else (target+right_carry)//10
        for X, Y in gen_X_Y():  # it doesn't matter which of options we take except for making a leading 0
            set_digits(x, [X], start), set_digits(y, [Y], start)
            if find_pair_with_same_length(s, x, y, start+1, new_left_carry, new_right_carry):
                return True
            clear_digits(y, [Y], start), clear_digits(x, [X], start)
            break  # if an option fails, other options also fail
    return False

def find_pair_with_overhang_length(s, x, y, start, left_carry, right_carry, left_Y):
    def find_left_x():
        left_X = to_int(s[len(x)-1-(start+overhang-1):len(x)-start][::-1]) + \
                 left_carry*(10**overhang) - new_left_carry - left_Y
        if not (0 <= left_X < 10**overhang):
            return None
        left_x = to_list(left_X)
        left_x = [0]*(overhang-len(left_x)) + left_x  # 0-padding
        if start == 0 and left_x[0] == 0:  # leading digit can't be 0
            return None
        if not set_digits(x, left_x, start):
            clear_digits(x, left_x, start)
            return None
        return left_x

    def find_left_y():
        if len(y)-start*2 <= 0:
            return [], right_carry  # pass current right carry if y is not updated
        right_y_len = min(len(y)-start*2, overhang)
        right_S, right_X = map(to_int, [s[start:start+right_y_len][::-1], left_x[:right_y_len][::-1]])
        new_right_carry, right_Y = map(abs, divmod(right_S-right_X-right_carry, 10**right_y_len))
        right_y = to_list(right_Y)
        right_y = [0]*(right_y_len-len(right_y)) + right_y  # 0-padding
        left_y = right_y[::-1]
        if start == 0 and left_y[0] == 0:  # leading digit can't be 0
            clear_digits(x, left_x, start)
            return None, None
        if not set_digits(y, left_y, start):
            clear_digits(y, left_y, start), clear_digits(x, left_x, start)
            return None, None
        return left_y, new_right_carry

    if len(x)-start*2 <= 0:
        return left_carry == right_carry
    overhang = min(len(x)-2*start, len(x)-len(y))
    for new_left_carry in xrange(2):
        left_x = find_left_x()
        if left_x is None:
            continue
        left_y, new_right_carry = find_left_y()
        if left_y is None or new_right_carry is None:
            continue
        new_left_Y = 0 if len(y)-start*2 <= overhang else to_int(left_y[:(len(y)-start*2)-overhang])
        if find_pair_with_overhang_length(s, x, y, start+overhang,
                                          new_left_carry, new_right_carry, new_left_Y):
            return True
        clear_digits(y, left_y, start), clear_digits(x, left_x, start)
    return False

def find_pair(s, i, j, left_carry):
    x, y = [None]*i, [None]*j
    result = find_pair_with_same_length(s, x, y, 0, left_carry, 0) if i == j else \
        find_pair_with_overhang_length(s, x, y, 0, left_carry, 0, 0)
    if not result:
        return None, None
    x.reverse(), y.reverse()
    return to_int(x), to_int(y)

def wont_sum_must_now():
    S = input()

    s = to_list(S)
    if s == s[::-1]:
        return S
    for P in gen_palindromes(S):
        s = to_list(S-P)
        s.reverse()
        carry = int(s[-1] == 1)
        for i in reversed(xrange(len(s)-carry, len(s)+1)):  # prefer larger X
            left_carry = len(s)-i
            for j in xrange(1, i+1):
                X, Y = find_pair(s, i, j, left_carry)
                if X is None or Y is None:
                    continue
                assert(X >= Y >= P)
                result = [X, Y]
                if P != 0:
                    result.append(P)
                return " ".join(map(str, result))
    assert(False)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, wont_sum_must_now())