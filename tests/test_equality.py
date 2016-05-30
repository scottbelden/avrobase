def test_same_class(BooleanClass):
    true_boolean = BooleanClass(field=True)
    true_boolean_two = BooleanClass(field=True)
    assert true_boolean == true_boolean_two

    false_boolean = BooleanClass(field=False)
    assert true_boolean != false_boolean


def test_different_class(BooleanClass, IntClass):
    boolean = BooleanClass(field=True)
    integer = IntClass(field=1)

    assert boolean != integer
    assert not (boolean == integer)
