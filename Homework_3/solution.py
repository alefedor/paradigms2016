import numpy as np
import math
import sys

# r: A B  s: E F  ans: J K
#    C D     G H       L M


def strassen_mult(n, r, s):
    if n == 1:
        return s * r
    mid = n // 2
    a = r[:mid, :mid]
    b = r[:mid, mid:]
    c = r[mid:, :mid]
    d = r[mid:, mid:]
    e = s[:mid, :mid]
    f = s[:mid, mid:]
    g = s[mid:, :mid]
    h = s[mid:, mid:]
    p1 = strassen_mult(mid, (a + d), (e + h))
    p2 = strassen_mult(mid, (c + d), e)
    p3 = strassen_mult(mid, a, (f - h))
    p4 = strassen_mult(mid, d, (g - e))
    p5 = strassen_mult(mid, (a + b), h)
    p6 = strassen_mult(mid, (c - a), (e + f))
    p7 = strassen_mult(mid, (b - d), (g + h))
    ans = np.empty((n, n), dtype=np.int)
    ans[:mid, :mid] = p1 + p4 - p5 + p7
    ans[:mid, mid:] = p3 + p5
    ans[mid:, :mid] = p2 + p4
    ans[mid:, mid:] = p1 - p2 + p3 + p6
    return ans


def main():
    n = int(input())
    r = np.loadtxt(sys.stdin, dtype=np.int, ndmin=2)
    s = r[n:]
    r = r[:n]
    n2 =  2 ** math.ceil(math.log2(n))
    r1 = np.zeros((n2, n2), dtype=np.int)
    s1 = np.zeros((n2, n2), dtype=np.int)
    r1[:n, :n] = r
    s1[:n, :n] = s
    ans = strassen_mult(n2, r1, s1)
    ans = ans[:n, :n]
    for i in range(n):
        print(*ans[i])


if __name__ == '__main__':
    main()