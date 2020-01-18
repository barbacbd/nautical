from setuptools import setup, find_packages

setup(
    name='nautical',
    version='1.0.1',
    license='MIT',
    packages=find_packages(),
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
