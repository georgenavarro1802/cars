from setuptools import setup, find_packages
import icdb

setup(
    name='icdb',
    description='The Internet Car DataBase',
    version=icdb.__version__,
    packages=find_packages(),
    install_requires=[
        'nose',
        'mock',
    ],
    entry_points={
        'console_scripts': [
            'icdb = icdb.process:main'
        ]
    },
)
