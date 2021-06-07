from setuptools import setup  # type: ignore
from setuptools import find_packages


if __name__ == '__main__':
    # This is based on the instructions from
    # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    from os import path
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as readme_file:
        long_description = readme_file.read()

    setup(
        name='compiler-identification',
        version='1.0.1',
        url='https://github.com/yugabyte/compiler-identification',
        author='Mikhail Bautin',
        author_email='mbautin@users.noreply.github.com',
        description='Identifying the properties of a C/C++ compiler, such as type and version',
        packages=find_packages(where='src'),
        install_requires=[
            'packaging',
            'codecheck >= 1.0.9',
            'autorepr >= 0.3.0'
        ],
        long_description=long_description,
        long_description_content_type='text/markdown',

        extras_require={
            # Following advice in this answer: https://stackoverflow.com/a/28842733/220215
            # Install with:
            # pip install -e '.[dev]'
            'dev': [
                'pycodestyle',
                'mypy',
                'codecheck'
            ]
        },
        package_dir={"": "src"},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
    )
