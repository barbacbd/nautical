from setuptools import setup, find_packages

with open('requirements.txt') as file:
    reqs = file.read().splitlines()

setup(
    name='nautical',
    version='0.0.1',
    scripts=['nautical_test'],
    packages=find_packages(),
    description='The nautical package is able to lookup NOAA buoy data including swell and wave information.',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    license='Proprietary',
    include_package_data=True,
    install_requires=reqs,
    zip_safe=False
)
