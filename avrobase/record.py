from copy import deepcopy
import os
import random
from string import ascii_lowercase

RECORD_TYPES = ('record', 'error', 'request')


def _getter(field_name):
    def get_field(self):
        return self._avro_dict[field_name]
    return get_field


def _setter(field_name):
    def set_field(self, value):
        self._avro_dict[field_name] = value
    return set_field


class MetaRecord(type):
    def __new__(cls, _, bases, attrs):
        try:
            schema = attrs['_schema']
        except:
            raise KeyError("Classes using the MetaRecord metaclass must have "
                           "a class attribute '_schema' containing the JSON "
                           "schema")

        if 'namespace' in schema:
            name = '.'.join([schema['namespace'], schema['name']])
        else:
            name = schema['name']

        # name needs to be a string, not unicode
        name = str(name)

        base_dict = {}
        for field in schema['fields']:
            f_name = field['name']
            if (isinstance(field['type'], dict) and
                    field['type']['type'] in RECORD_TYPES):
                embedded_record = create_record_class(field['type'])()
                attrs[f_name] = embedded_record
            else:
                # Make a property for each field
                attrs[f_name] = property(_getter(f_name), _setter(f_name))
                # Fill the base dict with the default values
                base_dict[f_name] = field.get('default')

        attrs['_base_dict'] = base_dict

        return super(MetaRecord, cls).__new__(cls, name, bases, attrs)


class Record(object):
    '''
    The base class for records.
    '''

    def __init__(self, **field_kwargs):
        self._avro_dict = deepcopy(self._base_dict)
        for field, value in field_kwargs.items():
            self._avro_dict[field] = value

    def __repr__(self):
        return '<{} at {}>'.format(self.__class__.__name__, id(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._avro_dict == other._avro_dict
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented

    @classmethod
    def from_dict(cls, avro_dict):
        record = cls()
        record._avro_dict = avro_dict
        return record

    def to_dict(self):
        return self._avro_dict

    @classmethod
    def generate_random(cls):
        '''
        Generates an instance containing random data that conforms to the
        avro schema
        '''
        return cls._generate_random(cls._schema)

    @classmethod
    def _generate_random(cls, schema):
        if isinstance(schema, dict):
            s_type = schema['type']
        elif isinstance(schema, list):
            s_type = 'union'
        else:
            s_type = schema

        if s_type == 'null':
            return None

        elif s_type == 'boolean':
            return random.choice((True, False))

        elif s_type == 'string':
            return ''.join(random.choice(ascii_lowercase) for _ in range(5))

        elif s_type == 'bytes':
            return os.urandom(10)

        elif s_type == 'int':
            return int(random.randint(-5, 5))

        elif s_type == 'long':
            return long(random.randint(-5, 5))

        elif s_type in ['float', 'double']:
            return float(random.random())

        elif s_type in ['record', 'error', 'request']:
            record = cls()

            for field in schema['fields']:
                f_name = field['name']
                f_type = field['type']
                record._avro_dict[f_name] = record._generate_random(f_type)
            return record


def create_record_class(schema):
    return MetaRecord('', (Record,), {'_schema': schema})
