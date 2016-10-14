from model import *


def brackets(func):
    def wrapper(*args, **kwargs):
        print("(", end='')
        res = func(*args, **kwargs)
        print(")", end='')

    return wrapper


class PrettyPrinter:
    def __init__(self):
        self.level = 0

    def visit(self, tree, is_sentence=True):
        name = tree.__class__.__name__
        try:
            fn = getattr(self, 'visit' + name)
        except AttributeError:
            print("Method for {} not found!".format(name))
            raise NotImplementedError
        if is_sentence:
            print("    " * self.level, end='')
        fn(tree)
        if is_sentence:
            print(";")

    def visitNumber(self, num):
        print(num.value, end='')

    def visitReference(self, ref):
        print(ref.name, end='')

    @brackets
    def visitUnaryOperation(self, unop):
        print(unop.op, end='')
        self.visit(unop.expr, False)

    @brackets
    def visitBinaryOperation(self, binop):
        self.visit(binop.lhs, False)
        print(" " + binop.op + " ", end='')
        self.visit(binop.rhs, False)

    def visitFunction(self, func):
        print("(", end='')
        first = True
        for arg in func.args:
            if first:
                first = False
            else:
                print(", ", end='')
            print(arg, end='')
        print(") {")
        self.level += 1
        for expr in func.body:
            self.visit(expr)
        self.level -= 1
        print("    " * self.level + "}", end='')

    def visitFunctionDefinition(self, fundef):
        print("def " + fundef.name, end='')
        self.visit(fundef.func, False)

    def visitFunctionCall(self, funcall):
        print(funcall.fun_expr.name + "(", end='')
        first = True
        for arg in funcall.args:
            if first:
                first = False
            else:
                print(", ", end='')
            self.visit(arg, False)
        print(")", end = "")

    def visitConditional(self, cond):
        print("if (", end='')
        self.visit(cond.condition, False)
        print(") {")
        self.level += 1
        for expr in cond.if_true:
            self.visit(expr)
        self.level -= 1
        print("    " * self.level + "} else {")
        self.level += 1
        for expr in cond.if_false:
            self.visit(expr)
        self.level -= 1
        print("    " * self.level + "}", end='')

    def visitPrint(self, p):
        print("print ", end='')
        self.visit(p.expr, False)

    def visitRead(self, r):
        print("read " + r.name, end='')


def test():
    #Example
    printer = PrettyPrinter()
    number = Number(42)
    conditional = Conditional(number, [], [])
    printer.visit(conditional)
    function = Function([], [])
    definition = FunctionDefinition("foo", function)
    printer.visit(definition)
    number = Number(42)
    pri = Print(number)
    printer.visit(pri)
    ten = Number(10)
    printer.visit(ten)
    reference = Reference("x")
    printer.visit(reference)
    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer.visit(mul)
    number = Number(42)
    unary = UnaryOperation('-', Number(42))
    printer.visit(unary)
    call = FunctionCall(definition, [Number(1), Number(2), Number(3)])
    printer.visit(call)
    print("")

    #Complex Test
    sc = Scope()
    sc["sqr"] = Function(["a"], [BinaryOperation(Reference("a"), "*", Reference("a"))])
    ref = FunctionDefinition("sqr", sc["sqr"])
    sc["foo"] = Function(['a', 'b', 'c'],
                        [Print(Reference("c")),
                         BinaryOperation(BinaryOperation(FunctionCall(ref, [Reference("a")]), "+", FunctionCall(ref, [Reference("b")])),
                                        "==",
                                        FunctionCall(ref, [Reference("c")]))])
    printer.visit(ref)
    a = Number(3)
    b = Number(4)
    c = Number(5)
    printer.visit(FunctionDefinition("calc", sc["foo"]))
    printer.visit(FunctionCall(FunctionDefinition("calc", sc["foo"]), [a, b, c]))

if __name__ == '__main__':
    test()