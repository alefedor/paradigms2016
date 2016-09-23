import numpy as np

# r: A B  s: E F  ans: J K
#    C D     G H       L M

def main():
    n = int(input())
    odd = False
    if n % 2 == 1:
        odd = True;
    r = np.array([0 for i in range(n + odd)] * (n + odd)).reshape(n + odd, n + odd)
    for i in range(n):
        r[i] = [int(x) for x in input().split()] + odd * [0]
    s = np.array([0 for i in range(n + odd)] * (n + odd)).reshape(n + odd, n + odd)
    for i in range(n):
        s[i] = [int(x) for x in input().split()] + odd * [0]
    mid = (n + odd) // 2
    a = r[:mid, :mid]
    b = r[:mid, mid:]
    c = r[mid:, :mid]
    d = r[mid:, mid:]
    e = s[:mid, :mid]
    f = s[:mid, mid:]
    g = s[mid:, :mid]
    h = s[mid:, mid:]
    p1 = np.dot((a + d), (e + h))
    p2 = np.dot((c + d), e)
    p3 = np.dot(a, (f - h))
    p4 = np.dot(d, (g - e))
    p5 = np.dot((a + b), h)
    p6 = np.dot((c - a), (e + f))
    p7 = np.dot((b - d), (g + h))
    j = p1 + p4 - p5 + p7
    k = p3 + p5
    l = p2 + p4
    m = p1 - p2 + p3 + p6
    ans = np.array([0 for i in range(n + odd)] * (n + odd)).reshape(n + odd, n + odd)
    for i in range(mid):
        ans[i] = [j[i][p] for p in range(mid)] + [k[i][p] for p in range(mid)]
    for i in range(mid):
        ans[i + mid] = [l[i][p] for p in range(mid)] + [m[i][p] for p in range(mid)]
    #assert ans.sum() == np.dot(q, r).sum()
    if (odd):
        ans = ans[:-1, :-1]
    for i in range(n):
        print(*ans[i])


if __name__ == '__main__':
    main()