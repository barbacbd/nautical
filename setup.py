from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nautical',
    version='1.2.0',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'bs4',
        'pykml'
    ],
    url='https://barbacbd@bitbucket.org/barbacbd/nautical',
    download_url='https://barbacbd@bitbucket.org/barbacbd/nautical/archive/v_101.tar.gz',
    description='The nautical package is able to lookup NOAA buoy data including swell and wave information.',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    include_package_data=True,
    zip_safe=False
)
