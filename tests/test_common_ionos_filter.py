import re
import unittest
from unittest.mock import MagicMock


def _validate_filter_key_segment(segment):
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', segment):
        raise Exception("Invalid filter key segment: '%s'" % segment)


def get_method_from_filter(filter_tuple):
    key, value = filter_tuple
    def method(item):
        current = item
        _LEAF_TYPES = (str, int, float, bool, bytes, list, dict)
        for key_part in key.split('.'):
            _validate_filter_key_segment(key_part)
            if current is None:
                return False
            if isinstance(current, _LEAF_TYPES):
                return current == value
            current = getattr(current, key_part)
        return current == value
    return method


class _Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestFilterKeyValidation(unittest.TestCase):

    def test_valid_key_passes(self):
        obj = _Obj(properties=_Obj(name='myserver'))
        f = get_method_from_filter(('properties.name', 'myserver'))
        self.assertTrue(f(obj))

    def test_valid_key_no_match(self):
        obj = _Obj(properties=_Obj(name='other'))
        f = get_method_from_filter(('properties.name', 'myserver'))
        self.assertFalse(f(obj))

    def test_dunder_key_is_valid_per_regex(self):
        # The regex ^[a-zA-Z_][a-zA-Z0-9_]*$ allows dunders; they are not rejected
        obj = _Obj(__class__name='x')
        f = get_method_from_filter(('__class__name', 'x'))
        self.assertTrue(f(obj))

    def test_metacharacter_key_raises(self):
        # 'na;me' contains ';' which fails the regex
        obj = _Obj(prop=_Obj())
        obj.prop = _Obj()  # ensure prop exists so validator reaches na;me
        f = get_method_from_filter(('prop.na;me', 'x'))
        with self.assertRaises(Exception) as ctx:
            f(obj)
        self.assertIn('Invalid filter key segment', str(ctx.exception))

    def test_none_intermediate_returns_false(self):
        obj = _Obj(properties=None)
        f = get_method_from_filter(('properties.name', 'myserver'))
        self.assertFalse(f(obj))

    def test_leaf_type_short_circuits(self):
        # When we encounter a leaf (str) before consuming all key parts, compare directly
        obj = _Obj(status='active')
        f = get_method_from_filter(('status', 'active'))
        # Should match directly since 'active' == 'active'
        self.assertTrue(f(obj))

    def test_underscore_prefix_key_valid(self):
        obj = _Obj(_private=_Obj(value='yes'))
        f = get_method_from_filter(('_private.value', 'yes'))
        self.assertTrue(f(obj))

    def test_digit_start_key_raises(self):
        # '1invalid' starts with a digit, fails the regex
        obj = _Obj()
        f = get_method_from_filter(('1invalid', 'x'))
        with self.assertRaises(Exception) as ctx:
            f(obj)
        self.assertIn('Invalid filter key segment', str(ctx.exception))

    def test_slash_in_key_raises(self):
        obj = _Obj()
        f = get_method_from_filter(('prop/etc', 'x'))
        with self.assertRaises(Exception) as ctx:
            f(obj)
        self.assertIn('Invalid filter key segment', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
