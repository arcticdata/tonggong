# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='tonggong',
    version='0.0.16',
    description='Universal toolkit',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Arctic Data',
    author_email='hello@datarc.cn',
    url='https://github.com/arcticdata/tonggong',
    license='MIT License',
    install_requires='',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
