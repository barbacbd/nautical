from setuptools import setup, find_packages
from os import path
from json import loads
from pip.req import parse_requirements


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory,"about.json"), "r") as about:
    jd = loads(about.read())


with open(path.join(this_directory, "requirements.txt"), "r") as reqs:
    requirements = reqs.read().split()
requirements = [x for x in requirements if x]

    
setup(
    name=jd["project"],
    version=jd["version"],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=requirements,
    url=jd["url"],
    download_url="https://github.com/barbacbd/nautical/archive/v_{}.tar.gz".format(jd["version"].replace(".", "")),
    description='The nautical package is able to lookup NOAA buoy data including swell and wave information.',
    author=jd["author"],
    author_email=jd["email"],
    package_data={'': ['*.yaml']},
    include_package_data=True,
    zip_safe=False
)
