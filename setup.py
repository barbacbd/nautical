from setuptools import setup, find_packages

with open('requirements.txt') as file:
    reqs = file.read().splitlines()

setup(
    name='forecaster',
    version='0.0.1',
    packages=find_packages(),
    description='The forecaster is able to lookup forecasted data for the NOAA Buoys.',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    license='Proprietary',
    include_package_data=True,
    install_requires=reqs,
    zip_safe=False
)
