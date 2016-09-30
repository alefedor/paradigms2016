class Scope(object):
    def __init__(self, parent=None):
        self.dict = dict()
        self.parent = parent

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        if self.parent:
            return self.parent[item]
        else:
            raise Exception

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number(int):
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
            return Number(-a)
        else:
            return Number(a==0)


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope)
        r = self.rhs.evaluate(scope)
        if self.op == "+":
            return Number(l + r)
        elif self.op == "-":
            return Number(l - r)
        elif self.op == "*":
            return Number(l * r)
        elif self.op == "/":
            return Number(l // r)
        elif self.op == "%":
            return Number(l % r)
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
        self.args = args

    def evaluate(self, scope):
        last = Number(0)
        for x in self.body:
            last = x.evaluate(scope)
        return last


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.func = function

    def evaluate(self, scope):
        scope[self.name] = self.func
        return self.func


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.args = args
        self.fun_expr = fun_expr

    def evaluate(self, scope):
        func = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        results = [x.evaluate(scope) for x in self.args]
        for i, x in enumerate(func.args):
            call_scope[x] = results[i]
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
        return Number(a)


def main():
    #Example
    parent = Scope()
    parent["bar"] = Number(10)
    scope = Scope(parent)
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'), '+', Reference('world')))])
    assert type(FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)) == Number
    assert scope["bar"] == 10
    scope["bar"] = Number(20)
    assert scope["bar"] == 20
    assert type(scope["bar"]) == Number
    #Test: Function sqr and Function a*a+b*b==c*c
    sc = Scope()
    #Read("a").evaluate(sc)
    #Read("b").evaluate(sc)
    #Read("c").evaluate(sc)
    sc["sqr"] = Function(["a"], [BinaryOperation(Reference("a"), "*", Reference("a"))])
    ref = FunctionDefinition("sqr", sc["sqr"])
    sc["foo"] = Function(['a', 'b', 'c'],
                        [BinaryOperation(BinaryOperation(FunctionCall(ref, [Reference("a")]), "+", FunctionCall(ref, [Reference("b")])),
                                        "==",
                                        FunctionCall(ref, [Reference("c")]))])
    a = Number(3)
    b = Number(4)
    c = Number(5)
    assert Print(FunctionCall(FunctionDefinition("calc", sc["foo"]), [a, b, c]).evaluate(sc)).evaluate(sc) ==  (a*a+b*b==c*c)
    c = Number(6)
    assert Print(FunctionCall(FunctionDefinition("calc", sc["foo"]), [a, b, c]).evaluate(sc)).evaluate(sc) ==  (a*a+b*b==c*c)


if __name__ == '__main__':
    main()