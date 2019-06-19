"""
setup
*****

:Author: tobijjah
:Date: 03.06.19
"""
from setuptools import find_packages
from setuptools import setup

version = ''

try:
    import ant
    version = ant.__version__

except ImportError:
    with open('../ant/__init__.py') as src:
        for line in src.readlines():
            if line.startswith('__version'):
                version = line.split('=')[1]
                version = version.strip()
                version = version.strip("'")
                version = version.strip('"')


with open('requirements.txt') as src:
    dependencies = src.read().split('\n')

with open('README.md') as src:
    readme = src.read()


setup(
    author='tobijjah',
    author_email='tobi.seyde@gmail.com',
    description='Agent based modelling on example of ant colony optimization.',
    long_description=readme,
    name='ant',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    entry_points='''
        [console_scripts]
        ant=ant.cli:main
    ''',
)


