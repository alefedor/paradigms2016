class Scope(object):
    def __init__(self, parent = None):
        self.dict = dict()
        self.parent = parent

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        if self.parent != None:
            return self.parent[item]
        else:
            raise Exception

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number(int):
    def __init__(self, value):
        self = value

    def evaluate(self, scope):
        return self


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope)
        if self.op == "-":
            return -a
        else:
            return 0 if a != 0 else 1


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope)
        r = self.rhs.evaluate(scope)
        if self.op == "+":
            return l + r
        elif self.op == "-":
            return l - r
        elif self.op == "*":
            return l * r
        elif self.op == "/":
            return l // r
        elif self.op == "%":
            return l % r
        elif self.op == "==":
            return Number(l == r)
        elif self.op == "!=":
            return Number(l != r)
        elif self.op == "<":
            return Number(l < r)
        elif self.op == ">":
            return Number(l > r)
        elif self.op == "<=":
            return Number(l <= r)
        elif self.op == ">=":
            return Number(l >= r)
        elif self.op == "&&":
            return Number(l and r)
        else:
            return Number(l or r)


class Function:
    def __init__(self, args, body):
        self.body = body

    def evaluate(self, scope):
        last = Number(0)
        for x in self.body:
            last = x.evaluate(scope) #?todo?
        return last


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.func = function

    def evaluate(self, scope):
        scope[self.name] = self.func #???
        return self.func


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.args = args
        self.fun_expr = fun_expr

    def evaluate(self, scope):
        func = self.fun_expr
        call_scope = Scope(scope)
        for x in self.args:
            call_scope[x] = scope[x].evaluate()
        return func.evaluate(call_scope)


class Conditional:
    def __init__(self, condition, if_true, if_false = None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        last = Number(0)
        if self.condition.evaluate():
            for x in self.if_true:
                last = x.evaluate(scope)
        elif self.if_false:
            for x in self.if_false:
                last = x.evaluate(scope)
        return last


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope)
        print(a)
        return a


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        a = int(input())
        scope[self.name] = a
        return a


def main():
    #Simple tests
    parent = Scope()
    parent["bar"] = Number(10)
    scope = Scope(parent)
    print(scope["bar"])
    scope["bar"] = Number(20)
    print(scope["bar"])
    f = FunctionCall(Number(1), [])
    add = BinaryOperation(f, "+", Number(2))
    print(add.evaluate(Scope))

if __name__ == '__main__':
    main()