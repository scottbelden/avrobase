import pytest

from avrobase.record import create_record_class
from primitive_schemas import all_schemas as all_primitive_schemas


@pytest.fixture
def BooleanClass():
    return create_record_class(all_primitive_schemas['boolean_schema'])


@pytest.fixture
def IntClass():
    return create_record_class(all_primitive_schemas['int_schema'])
