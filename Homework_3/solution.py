import numpy as np
import sys

# r: A B  s: E F  ans: J K
#    C D     G H       L M


def strassen_mult(n, r, s):
    if n == 1:
        return s * r
    odd = 0
    if n % 2 == 1:
        odd = 1
        s1 = np.array([0 for i in range(n + odd)] * (n + odd)).reshape(n + odd, n + odd)
        for i in range(n):
            s1[i] = [x for x in s[i]] + [0]
        s = s1
        r1 = np.array([0 for i in range(n + odd)] * (n + odd)).reshape(n + odd, n + odd)
        for i in range(n):
            r1[i] = [x for x in r[i]] + [0]
        r = r1
    mid = (n + odd) // 2
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
    j = p1 + p4 - p5 + p7
    k = p3 + p5
    l = p2 + p4
    m = p1 - p2 + p3 + p6
    ans = np.array([0 for i in range(n + odd)] * (n + odd)).reshape(n + odd, n + odd)
    for i in range(mid):
        ans[i] = [j[i][p] for p in range(mid)] + [k[i][p] for p in range(mid)]
    for i in range(mid):
        ans[i + mid] = [l[i][p] for p in range(mid)] + [m[i][p] for p in range(mid)]
    if odd:
        ans = ans[:-1, :-1]
    return ans


def main():
    n = int(input())
    if n == 1:
        a = int(input())
        b = int(input())
        print(a * b)
        return
    r = np.loadtxt(sys.stdin, dtype=np.int)
    s = r[n:]
    r = r[:n]
    ans = strassen_mult(n, r, s)
    for i in range(n):
        print(*ans[i])


if __name__ == '__main__':
    main()