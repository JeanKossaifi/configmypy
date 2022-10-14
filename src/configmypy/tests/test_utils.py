from ..utils import iter_nested_dict_flat
from ..utils import update_nested_dict_from_flat
from ..bunch import Bunch


def test_iter_nested_dict_flat():
    """Test for iter_nested_dict_flat
    """
    test = dict(a=dict(b=3, c=dict(d='e', f=5), g=5))
    true_res = {'a.b': 3, 'a.c.d': 'e', 'a.c.f': 5, 'a.g': 5}
    res = dict(iter_nested_dict_flat(test))
    assert res == true_res
    
    # Nothing to do for non-nested dict
    test = dict(a=2, b=3, c=4)
    res = dict(iter_nested_dict_flat(test))
    assert res == test
    

def test_update_nested_dict_from_flat():
    """Test for update_nested_dict_from_flat
    """
    test = Bunch(dict(a=dict(b=3, c=dict(d='e', f=5), g=5)))
    update_nested_dict_from_flat(test, 'a.c.f', 8)
    assert test.a.c.f == 8
    
    update_nested_dict_from_flat(test, 'g', 'cool')
    assert test.g == 'cool'
    
