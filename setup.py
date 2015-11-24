from setuptools import setup, find_packages

setup(
    name = 'greengrapher',
    version = '1.0',
    packages = find_packages(exclude = ['*test']),
    scripts = ['scripts/greengraph'],
    install_requires = ['numpy','matplotlib','geopy','requests','StringIO','argparse','nose']
)
