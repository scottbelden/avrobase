
_avro_primitive_types = [
    'null',
    'boolean',
    'int',
    'long',
    'float',
    'double',
    'bytes',
    'string',
]

all_schemas = {}

for t in _avro_primitive_types:
    key = t + '_schema'
    value = {
        'type': 'record',
        'name': t,
        'fields': [{
            'name': 'field',
            'type': t,
        }],
    }
    all_schemas[key] = value
