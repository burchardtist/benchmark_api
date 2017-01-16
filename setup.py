import os
from setuptools import setup


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='benchmark_api',
    version='0.0.0',
    include_package_data=True,
    license='MIT License',
    description='benchmark_api',
    long_description='benchmark_api',
    author='Aleksander Philips',
    packages=['src'],
    entry_points={
        'console_scripts': [
            'run_server=src.api_server:run_server',
            'start_benchmark=src.__main__:run'
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
