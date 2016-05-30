from avrobase.record import create_record_class

test_schema = {
    "namespace": "example.avro",
    "type": "record",
    "name": "User",
    "fields": [{
        "name": "name",
        "type": "string"
    }, {
        "name": "favorite_number",
        "type": ["int", "null"]
    }, {
        "name": "favorite_color",
        "type": ["string", "null"]
    }]
}

default_schema = {
    "name": "Default",
    "type": "record",
    "fields": [{
        "name": "default_field",
        "type": "string",
        "default": "default_value"
    }]
}


def _get_instance(schema):
    return create_record_class(schema)()


def test_repr():
    record = _get_instance(test_schema)
    repr(record)


def test_avro_dictionary():
    record = _get_instance(test_schema)

    avro_dict = {
        'name': 'test',
        'favorite_number': 1,
        'favorite_color': 'red',
    }

    record.name = avro_dict['name']
    record.favorite_number = avro_dict['favorite_number']
    record.favorite_color = avro_dict['favorite_color']

    assert record.name == avro_dict['name']
    assert record.favorite_number == avro_dict['favorite_number']
    assert record.favorite_color == avro_dict['favorite_color']

    assert record.to_dict() == avro_dict
