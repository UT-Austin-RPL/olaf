from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    lines = f.readlines()

# remove images from README
lines = [x for x in lines if (('.png' not in x) and ('.gif' not in x))]
long_description = ''.join(lines)

setup(
    name="lflf",
    packages=[
        package for package in find_packages() if package.startswith("lflf")
    ],
    install_requires=[
        "h5py",
    ],
    eager_resources=['*'],
    include_package_data=True,
    python_requires='>=3',
    description="lflf: Learning from Language Feedback",
    author="",
    url="git@github.com:huihanl/LfLF",
    author_email="huihanl@utexas.edu",
    version="0.1",
    long_description=long_description,
    long_description_content_type='text/markdown'
)