from setuptools import setup, find_packages
from os import path, stat


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

    
version="LOCAL"
if stat("VERSION").st_size > 0:
    with open(path.join(this_directory, "VERSION"), encoding='utf-8') as v:
        for line in v:
            # make some assumptions that its not all bad data in the file
            # since my CI _should_ be the one adding this data
            if line.startswith("version:"):
                version_info = "".join(line.split()).split(":")
                if len(version_info) >= 2:
                    version = version_info[1]
            break  # exit early, don't care what else was there

    
setup(
    name='nautical',
    version=version,
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[
        'bs4',
        'pykml'
    ],
    entry_points={
        'console_scripts': [
            'NauticalTests=nautical.tests.nautical_tests:main'
        ]
    },
    url='https://barbacbd@bitbucket.org/barbacbd/nautical',
    download_url='https://barbacbd@bitbucket.org/barbacbd/nautical/archive/v_101.tar.gz',
    description='The nautical package is able to lookup NOAA buoy data including swell and wave information.',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    include_package_data=True,
    zip_safe=False
)
