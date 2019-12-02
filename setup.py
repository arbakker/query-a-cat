from setuptools import setup, find_packages
with open('README.md') as f:
    readme = f.read()

setup(
    name='query-a-cat',
    version='0.1',
    description='CLI to query a CSW (Catalog Service for the Web)',
    long_description=readme,
    author='Anton Bakker',
    author_email='anton.bakker@kadaster.nl',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': []},
    setup_requires=['wheel'],
    install_requires=[
        'Click',
        'lxml',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        qac=query_a_cat.cli:cli
    ''',
)