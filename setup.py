#!/usr/bin/env python

from os.path import dirname, join
from setuptools import setup

package_name = 'avrobase'
setup_dir = dirname(__file__)

with open(join(setup_dir, package_name, 'version.py')) as fp:
    exec(fp.read())

setup(name=package_name,
      version=__version__,
      description='Python Classes for Avro',
      author='Scott Belden',
      author_email='scottabelden@gmail.com',
      license='Apache 2.0',
      url='https://github.com/scottbelden/avrobase',
      download_url='https://github.com/scottbelden/avrobase/tarball/0.0.1',
      packages=[package_name],
)
