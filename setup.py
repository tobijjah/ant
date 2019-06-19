"""
setup
*****

:Author: tobijjah
:Date: 03.06.19
"""
from setuptools import setup, find_packages
import ant


setup(
    name='ant',
    version=ant.__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'numpy',
        'pygame',
        'affine',
    ],
    entry_points='''
        [console_scripts]
        ant=ant.cli:main
    ''',
)


