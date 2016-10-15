from yat.model import *
from yat.printer import *


class ConstantFolder:
    def __init__(self):
        self.level = 0

    def visit(self, tree):
        name = tree.__class__.__name__
        try:
            fn = getattr(self, 'visit' + name)
        except AttributeError:
            print("Method for {} not found!".format(name))
            raise NotImplementedError
        return fn(tree)

    def visitNumber(self, num):
        return num

    def visitReference(self, ref):
        return ref

    def visitUnaryOperation(self, unop):
        unop.expr = self.visit(unop.expr)
        if isinstance(unop.expr, Number):
            return unop.evaluate(...)
        return unop

    def visitBinaryOperation(self, binop):
        binop.lhs = self.visit(binop.lhs)
        binop.rhs = self.visit(binop.rhs)
        if isinstance(binop.lhs, Number) and isinstance(binop.rhs, Number):
            return binop.evaluate(...)
        if binop.op == '*':
            if isinstance(binop.lhs, Number) and isinstance(binop.rhs, Reference) and binop.lhs.value == 0:
                return binop.lhs
            if isinstance(binop.lhs, Reference) and isinstance(binop.rhs, Number) and binop.rhs.value == 0:
                return binop.rhs
        if binop.op == '-' and isinstance(binop.lhs, Reference) and isinstance(binop.rhs, Reference) and binop.lhs.name == binop.rhs.name:
            return Number(0)
        return binop

    def visitFunction(self, func):
        for i in range(len(func.body)):
            func.body[i] = self.visit(func.body[i])
        return func

    def visitFunctionDefinition(self, fundef):
        fundef.func = self.visit(fundef.func)
        return fundef

    def visitFunctionCall(self, funcall):
        for i in range(len(funcall.args)):
            funcall.args[i] = self.visit(funcall.args[i])
        return funcall

    def visitConditional(self, cond):
        cond.condition = self.visit(cond.condition)
        for i in range(len(cond.if_true)):
            cond.if_true[i] = self.visit(cond.if_true[i])
        if not cond.if_false is None:
            for i in range(len(cond.if_false)):
                cond.if_false[i] = self.visit(cond.if_false[i])
        return cond

    def visitPrint(self, p):
        p.expr = self.visit(p.expr)
        return p

    def visitRead(self, r):
        return r


def test():
    printer = PrettyPrinter()
    folder = ConstantFolder()
    a = BinaryOperation(Number(1), '*', BinaryOperation(Number(2), '+', Number(3)))
    printer.visit(a)
    a = folder.visit(a)
    printer.visit(a)
    print('')
    a = Conditional(BinaryOperation(Number(2), '<', Number(1)), [Print(UnaryOperation('-', Number(5)))], [Print(Number(4))])
    printer.visit(a)
    a = folder.visit(a)
    printer.visit(a)
    print('')
    sc = Scope()
    sc["foo"] = Function(['a', 'b', 'c'],
                        [Print(Reference("c")),
                         BinaryOperation(BinaryOperation(Reference("a"), "-", Reference("a")),
                                        "*",
                                        Reference("c"))])
    a = Number(3)
    b = Number(4)
    c = Number(5)
    d = FunctionDefinition("calc", sc["foo"])
    printer.visit(d)
    d = folder.visit(d)
    printer.visit(d)
    print('')
    d = FunctionCall(FunctionDefinition("calc", sc["foo"]), [a, b, c])
    printer.visit(d)
    d = folder.visit(d)
    printer.visit(d)


if __name__ == '__main__':
    test()