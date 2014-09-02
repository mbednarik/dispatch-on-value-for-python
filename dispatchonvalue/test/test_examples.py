import unittest
import dispatchonvalue as dv


class TestExamples(unittest.TestCase):
    def test_example1(self):
        called = [0]

        dispatch_on_value = dv.DispatchOnValue()
        @dispatch_on_value.add([1, 2, 3])  # Primitive type value 1 is the matching pattern
        def _(a):
            called[0] = 1
            # Do something

        @dispatch_on_value.add([4, 5, 6])  # Primitive type value 2 is the matching pattern
        def _(a):
            called[0] = 2
            # Do something

        p = [4, 5, 6]
        dispatch_on_value.dispatch(p)  # Will call second function above
        assert called[0] == 2

    def test_1_multi_dispatch_on_value(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add([1, 2, 3])
        def fn_1(a):
            assert a == [1, 2, 3]
            called[0] = 1

        @dispatch_on_value.add([4, 5, 6])
        def fn_2(a):
            assert a == [4, 5, 6]
            called[0] = 2

        p = [1, 2, 3]
        dispatch_on_value.dispatch(p)  # Call fn_1 and return True
        assert called[0] == 1

        p = [4, 5, 6]
        dispatch_on_value.dispatch(p)  # Call fn_2 and return True
        assert called[0] == 2

        called = [0]
        p = [1, 2, 6]
        dispatch_on_value.dispatch(p)  # Not call anything and return False
        assert called[0] == 0

    def test_2_arbitrary_nested(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add({'one': 3, 'animals': ['frog', 'mouse']})
        def fn_1(a):
            assert a == {'one': 3, 'animals': ['frog', 'mouse']}
            called[0] = 1

        dispatch_on_value.dispatch({'one': 3, 'animals': ['frog', 'mouse']})
        assert called[0] == 1

    def test_3_wildcard(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add([dv.any_a, 'b', 3, [3, 'd', dv.any_a]])
        def _(a):
            called[0] = 1

        dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'c']])  # This will match
        assert called[0] == 1

        called[0] = 0
        dispatch_on_value.dispatch(['f', 'b', 3, [3, 'd', 'f']])  # This will match
        assert called[0] == 1

        called[0] = 0
        dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'f']])  # This will not match
        assert called[0] == 0

    def test_4_pass_parameters(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add([1, 2])  # This is the matching pattern
        def _(a, my_abc, my_def):
            assert a == [1, 2]
            assert my_abc == 'abc'
            assert my_def == 'def'
            called[0] = 1
            # Do something

        dispatch_on_value.dispatch([1, 2], 'abc', 'def')
        assert called[0] == 1

    def test_5_use_lambdas1(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add([1, 2, lambda x: 3 < x < 7, 'hello'])
        def _(a):
            called[0] = 1

        dispatch_on_value.dispatch([1, 2, 4, 'hello'])  # This will match
        assert called[0] == 1

        called[0] = 0
        dispatch_on_value.dispatch([1, 2, 2, 'hello'])  # This will not match
        assert called[0] == 0

    def test_5_use_lambdas2(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add(['a', 2, lambda x: x == 'b' or x == 'c'])
        def _(a):
            called[0] = 1

        dispatch_on_value.dispatch(['a', 2, 'c'])  # This will match
        assert called[0] == 1

        called[0] = 0
        dispatch_on_value.dispatch(['a', 2, 's'])  # This will not match
        assert called[0] == 0

    def test_partial_or_strict(self):
        called = [0]
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add({'name': 'john', 'age': 32})
        def _(a):
            called[0] = 1

        # These will match because they contain the minimal dictionary items
        dispatch_on_value.dispatch({'name': 'john', 'age': 32})
        assert called[0] == 1

        called[0] = 0
        dispatch_on_value.dispatch({'name': 'john', 'age': 32, 'sex': 'male'})
        assert called[0] == 1

        # This will match because it's strict and the pattern is exactly the
        # same
        called[0] = 0
        dispatch_on_value.dispatch_strict({'name': 'john', 'age': 32})
        assert called[0] == 1

        called[0] = 0
        # This will not match because the dictionary doesn't match exactly
        dispatch_on_value.dispatch_strict(
            {'name': 'john', 'age': 32, 'sex': 'male'}
        )
        assert called[0] == 0