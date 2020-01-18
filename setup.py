from setuptools import setup, find_packages

with open('requirements.txt') as file:
    reqs = file.read().splitlines()

setup(
    name='nautical',
    version='1.0.0',
    license='MIT',
    packages=find_packages(),
    url='https://barbacbd@bitbucket.org/barbacbd/nautical',
    download_url='https://barbacbd@bitbucket.org/barbacbd/nautical/archive/v_100.tar.gz',
    description='The nautical package is able to lookup NOAA buoy data including swell and wave information.',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    include_package_data=True,
    install_requires=reqs,
    zip_safe=False
)
