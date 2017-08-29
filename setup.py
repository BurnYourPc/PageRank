from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='PAgeRankImplementation',
    version='0.1.0',
    description='Sample implementation of Page Rank Algorithm',
    long_description=readme,
    author='Tolis Chal, Pantelispanka, nikfot',
    author_email='burnyourpc@gmail.com',
    url='https://github.com/BurnYourPc',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
