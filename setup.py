"""Setup tools for libkarel."""

import subprocess
import setuptools  # type: ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='omegaup',
    version=subprocess.check_output(['/usr/bin/git', 'describe', '--tags'],
                                    universal_newlines=True),
    author='omegaUp',
    author_email='lhchavez@omegaup.org',
    description='Utilities for interacting with omegaUp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/omegaup/libomegaup',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
