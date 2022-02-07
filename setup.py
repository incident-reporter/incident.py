#!/usr/bin/env python

"""The setup script."""

import re
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('incident/__version__.py', 'r') as f:
    ver_re = re.compile(
        r'''__version__\s*=\s*['"](([0-9]+\.?)+(a|b|rc)?)['"]'''
    )
    version = ver_re.search(f.read()).group(1)

setup(
    author='Leo Developer',
    author_email='leodeveloper@protonmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description='Manage incidents over discord webhooks.',
    license='MIT license',
    long_description=readme,
    keywords='incident-reporter discord-webhook',
    name='incident.py',
    packages=find_packages(include=['incident', 'incident.*']),
    tests_require=['pytest>=6.2,<8'],
    url='https://github.com/incident-reporter/incident.py',
    version=version,
    zip_safe=False,
    extras_require={
        'tests': ['pytest>=6.2,<8']
    }
)
