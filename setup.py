from setuptools import setup, find_packages

setup(
    name='dnsdumpster',
    version='0.1.0',
    description='DNSDumpster API client for querying DNS records',
    author='milo2012',
    url='https://github.com/milo2012/dnsdumpster',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'dnsdumpster = dnsdumpster.client:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

