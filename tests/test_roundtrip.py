from avrobase.record import create_record_class
from primitive_schemas import all_schemas as all_primitive_schemas


def test_roundtrip():
    for schema in all_primitive_schemas.values():
        AvroClass = create_record_class(schema)

        random = AvroClass.generate_random()
        other = AvroClass.from_dict(random.to_dict())

        assert random == other


def test_embedded_record():
    outer_name = 'Outer'
    inner_name = 'Inner'
    schema = {
        'name': outer_name,
        'type': 'record',
        'fields': [{
            'name': 'outer_field',
            'type': {
                'type': 'record',
                'name': inner_name,
                'fields': [{
                    'name': 'inner_field',
                    'type': 'string'
                }]
            }
        }]
    }

    AvroClass = create_record_class(schema)
    assert AvroClass.__name__ == outer_name

    outer_record = AvroClass()
    assert outer_record.outer_field.__class__.__name__ == inner_name
    assert outer_record.outer_field.inner_field is None

    random = AvroClass.generate_random()
    other = AvroClass.from_dict(random.to_dict())

    assert random == other


def test_embedded_record_with_namespace():
    namespace = 'namespace'
    outer_name = 'Outer'
    inner_name = 'Inner'
    schema = {
        'namespace': namespace,
        'name': outer_name,
        'type': 'record',
        'fields': [{
            'name': 'outer_field',
            'type': {
                'type': 'record',
                'name': inner_name,
                'fields': [{
                    'name': 'inner_field',
                    'type': 'string'
                }]
            }
        }]
    }

    AvroClass = create_record_class(schema)
    assert AvroClass.__name__ == '.'.join([namespace, outer_name])

    outer_record = AvroClass()
    # TODO: Fix embedded namespaces
    # inner_record_name = outer_record.outer_field.__class__.__name__
    # assert inner_record_name == '.'.join([namespace, inner_name])
    assert outer_record.outer_field.inner_field is None

    random = AvroClass.generate_random()
    other = AvroClass.from_dict(random.to_dict())

    assert random == other
