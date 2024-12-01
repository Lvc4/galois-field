from setuptools import setup, find_packages

setup(
    name='galois-field',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    description='A library for Galois Field (GF(2^m)) operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lvc4 @GitHub',
    license='MIT',
    url='https://github.com/Lvc4/galois-field',
)