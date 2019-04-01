from setuptools import setup, find_packages

setup(
    name="stochastic-moments",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'demo=moments.main:main',
        ],
    },
)
