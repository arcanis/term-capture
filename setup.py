from setuptools import setup, find_packages

setup(
    name='term-capture',
    version='0.1',
    packages=find_packages(),
    package_data={'': ['init.sh']},
    entry_points = {
        'console_scripts': [
            'term-capture = term_capture.cli:main',
        ],
    },
    install_requires = [
        'pyperclip',
        'pyte @ git+ssh://git@github.com/selectel/pyte.git@fa5255a2dx1e4ad16b0eeaf97636194c47e98ce1'
    ]
)
