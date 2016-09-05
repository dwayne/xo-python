import re

from setuptools import setup


with open('xo/__init__.py', encoding='utf-8') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)


with open('README.rst', encoding='utf-8') as f:
    readme = f.read()


with open('CHANGELOG.rst', encoding='utf-8') as f:
    changelog = f.read()


packages = [
    'xo'
]


setup(
    name='xo',
    version=version,
    description='A Tic-tac-toe CLI game and library.',
    long_description=readme + '\n\n' + changelog,
    url='https://github.com/dwayne/xo-python',
    author='Dwayne Crooks',
    author_email='me@dwaynecrooks.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Games/Entertainment :: Board Games'
    ],
    keywords='tic-tac-toe tic tac toe noughts crosses',
    packages=packages,
    entry_points={
        'console_scripts': [
            'xo=xo.cli:main'
        ]
    }
)
