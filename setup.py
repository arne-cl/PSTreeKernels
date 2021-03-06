# This is your "setup.py" file.
# See the following sites for general guide to Python packaging:
#   * `The Hitchhiker's Guide to Packaging <http://guide.python-distribute.org/>`_
#   * `Python Project Howto <http://infinitemonkeycorps.net/docs/pph/>`_

from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README.rst')).read()
#NEWS = open(os.path.join(here, 'NEWS.rst')).read()


version = '0.1.0'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(name='PSTreeKernels',
    version=version,
    description="tree kernels (MFTK, EFTK) using Positional Suffix Trees (Paetzold 2015)",
    #long_description=README + '\n\n' + NEWS,
    # Get classifiers from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    # classifiers=[c.strip() for c in """
    #     Development Status :: 4 - Beta
    #     License :: OSI Approved :: MIT License
    #     Operating System :: OS Independent
    #     Programming Language :: Python :: 2.6
    #     Programming Language :: Python :: 2.7
    #     Programming Language :: Python :: 3
    #     Topic :: Software Development :: Libraries :: Python Modules
    #     """.split('\n') if c.strip()],
    # ],
    keywords='tree kernel mftk eftk positional suffix tree pst',
    author='Gustavo Henrique Paetzold',
    author_email='ghpaetzold1@sheffield.ac.uk',
    # url='',
    # license='3-Clause BSD License',
    packages=find_packages("src"),
    package_dir = {'': "src"},
    package_data= {'PSTreeKernels': ['data/*.txt']},
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['EFTK=PSTreeKernels.EFTK:main', 'MFTK=PSTreeKernels.MFTK:main']
    }
)
