from model import *
import pytest
from io import StringIO
from operator import *
from unittest.mock import patch


@pytest.fixture(scope="function")
def scope():
    return Scope()


def assert_equal(a, b):
    sc = Scope()
    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        Print(b).evaluate(sc)
        assert mock_out.getvalue() == str(a)+"\n"

def assert_not_equal(a, b):
    sc = Scope()
    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        Print(b).evaluate(sc)
        assert mock_out.getvalue() != str(a)+"\n"


class TestScope:
    def test_basic(self, scope):
        scope['a'] = Number(23)
        scope['A'] = Number(25)
        assert isinstance(scope['a'], Number)
        assert_equal(23, scope['a'])
        assert_equal(25, scope['A'])

    def test_inheritance(self, scope):
        child = Scope(scope)
        scope['a'] = Number(23)
        assert isinstance(child['a'], Number)
        assert_equal(23, child['a'])
        child['a'] = Number(25)
        assert_equal(25, child['a'])
        assert_equal(23, scope['a'])


class TestNumber():
    def test_basic(self, scope):
        a = Number(23)
        assert isinstance(a.evaluate(scope), Number)
        assert_equal(23, a)


class TestPrint:
    def test_basic(self, scope):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            Print(Number(23)).evaluate(scope)
            assert mock_out.getvalue() == "23\n"
            scope['a'] = Number(25)
            Print(scope['a']).evaluate(scope)
            assert mock_out.getvalue() == "23\n25\n"
            Print(Number(-1)).evaluate(scope)
            assert mock_out.getvalue() == "23\n25\n-1\n"


class TestRead:
    def test_basic(self, scope):
        for i in range(-3, 4):
            with patch("sys.stdin", StringIO(str(i)+"\n")):
                Read('a').evaluate(scope)
                assert isinstance(scope['a'], Number)
                assert_equal(i, scope['a'])


class TestReference:
    def test_basic(self, scope):
        scope['a'] = Number(23)
        ref = Reference('a')
        assert_equal(23, ref.evaluate(scope))

    def test_inheritance(self, scope):
        scope['a'] = Number(23)
        ref = Reference('a')
        child = Scope(scope)
        assert_equal(23, ref.evaluate(child))
        assert_equal(23, ref.evaluate(scope))


class TestUnaryOperation:
    ops = {'-': lambda x: -x,
           '!': lambda x: 1 if x == 0 else 0}

    def test_operations(self):
        for op, func in self.ops.items():
            for i in range(-3, 4):
                if (op == '!'):
                    if (func(i)):
                        assert_not_equal(0, UnaryOperation(op, Number(i)))
                    else:
                        assert_equal(0, UnaryOperation(op, Number(i)))
                else:
                    assert_equal(int(func(i)), UnaryOperation(op, Number(i)))


class TestBinaryOperation:
    ops = {'+': add,
           '-': sub,
           '*': mul,
           '/': floordiv,
           '%': mod,
           '==': eq,
           '!=': ne,
           '<': lt,
           '>': gt,
           '<=': le,
           '>=': ge,
           '&&': lambda x,y: 1 if x != 0 and y != 0 else 0,
           '||': lambda x,y: 1 if x != 0 or y != 0 else 0}

    logic = {'==', '<', '>', '!=', '<=', '>=', '&&', '||'}

    def test_operations(self):
        for op, func in self.ops.items():
            for i in range(-3, 4):
                for j in range(-3, 4):
                    if j != 0 or (op != '/' and op != '%'):
                        if (op in self.logic):
                            if (func(i, j)):
                                assert_not_equal(0, BinaryOperation(Number(i), op, Number(j)))
                            else:
                                assert_equal(0, BinaryOperation(Number(i), op, Number(j)))
                        else:
                            assert_equal(int(func(i, j)), BinaryOperation(Number(i), op, Number(j)))


class TestFunction:
    def test_empty(self, scope):
        fun = Function([], [])
        fun.evaluate(scope)

    def test_basic(self):
        fun = Function([], [Number(1), Number(2), Number(3)])
        assert_equal(3, fun)

    def test_complex(self):
        fun = Function([], [UnaryOperation('-', Number(-3))])
        assert_equal(3, fun)


class FunctionDefinitionTest:
    def test_basic(self, scope):
        fun = Function([], [Number(23)])
        fun_def = FunctionDefinition("foo", fun)
        get_fun = fun_def.evaluate(scope)
        assert_equal(23, scope["foo"])
        assert_equal(23, get_fun)


class TestFunctionCall:
    def test_local_ans(self):
        fun = Function(['a', 'b', 'c'], [Reference('a'), Reference('b'), Reference('c')])
        fun_def = FunctionDefinition("foo", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        assert_equal(3, fun_call)

    def test_global_ans(self, scope):
        scope['d'] = Number(23)
        fun = Function(['a', 'b', 'c'], [Reference('a'), Reference('b'), Reference('d')])
        fun_def = FunctionDefinition("foo", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        assert_equal(23, fun_call.evaluate(scope))

    def test_overwrite(self, scope):
        scope['c'] = Number(23)
        fun = Function(['a', 'b', 'c'], [Reference('a'), Reference('b'), Reference('c')])
        fun_def = FunctionDefinition("foo", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        assert_equal(3, fun_call.evaluate(scope))


class TestConditional:
    def test_true(self):
        cond = Conditional(Number(1), [Number(1)], [Number(2)])
        assert_equal(1, cond)

    def test_true_many(self):
        cond = Conditional(Number(1), [Number(-1), Number(3), Number(1)], [Number(2)])
        assert_equal(1, cond)

    def test_false(self):
        cond = Conditional(Number(0), [Number(1)], [Number(2)])
        assert_equal(2, cond)

    def test_false_many(self):
        cond = Conditional(Number(0), [Number(1)], [Number(-1), Number(3), Number(2)])
        assert_equal(2, cond)

    def test_complex_true(self):
        cond = Conditional(BinaryOperation(Number(-1), '+', Number(3)),
                           [BinaryOperation(Number(-1), '+', Number(2))],
                           [BinaryOperation(Number(-1), '+', Number(3))])
        assert_equal(1, cond)

    def test_complex_false(self):
        cond = Conditional(BinaryOperation(Number(-2), '+', Number(2)),
                           [BinaryOperation(Number(-1), '+', Number(2))],
                           [BinaryOperation(Number(-1), '+', Number(3))])
        assert_equal(2, cond)

    def test_true_empty(self, scope):
        cond = Conditional(Number(1), [], [Number(2)])
        cond.evaluate(scope)
        cond = Conditional(Number(1), None, [Number(2)])
        cond.evaluate(scope)

    def test_false_empty(self, scope):
        cond = Conditional(Number(0), [Number(1)], [])
        cond.evaluate(scope)
        cond = Conditional(Number(0), [Number(1)], None)
        cond.evaluate(scope)

    def test_true_all_empty(self, scope):
        cond = Conditional(Number(1), [], [])
        cond.evaluate(scope)