from setuptools import setup, find_packages


setup(
    name="datapunt-django-snapshot",
    author="Yahia Elsherbini",
    version="0.1",
    packages=find_packages(),
    long_description='file: README.md',
    install_requires=['requests', 'django']
)
