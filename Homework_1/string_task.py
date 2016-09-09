def verbing(s):
    if len(s) < 3:
        return s
    if s[len(s) - 3::] == "ing":
        s += "ly"
    else:
        s += "ing"
    return s


# "not" and "Not", "bad" and "Bad" are supposed to be different strings

def not_bad(s):
    a = s.find("not")
    b = s.find("bad")
    if a == -1 or b == -1:
        print("Error, trere is no substring not or bad(or both)")
        return s
    if  a < b:
        s = s[:a] + "good" + s[b + 3:]
    return s


def front_back(a, b):
    ma = (len(a) + 1) // 2
    mb = (len(b) + 1) // 2
    res = a[:ma] + b[:mb] + a[ma:] + b[mb:]
    return res
