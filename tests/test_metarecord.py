import pytest
from avrobase.record import MetaRecord, Record

test_schema = {
    "namespace": "foo",
    "type": "record",
    "name": "User",
    "fields": [{
        "name": "name",
        "type": "string"
    }],
}


def test_class_naming():
    schema = test_schema.copy()
    schema_ns = schema['namespace']
    schema_name = schema['name']

    # With namespace
    AvroClass = MetaRecord('', (Record,), {'_schema': schema})
    assert AvroClass.__name__ == '.'.join([schema_ns, schema_name])

    # Without namespace
    del schema['namespace']
    AvroClass = MetaRecord('', (Record,), {'_schema': schema})
    assert AvroClass.__name__ == schema_name


def test_required_schema():
    with pytest.raises(KeyError):
        MetaRecord('', (Record,), {})
