from setuptools import setup

from frac_Fourier import __version__
from importlib.util import module_from_spec, spec_from_file_location

from setuptools import find_packages, setup
import os

# https://packaging.python.org/guides/single-sourcing-package-version/
# http://blog.ionelmc.ro/2014/05/25/python-packaging/
_PATH_ROOT = os.path.dirname(__file__)
_PATH_REQUIRE = os.path.join(_PATH_ROOT, "requirements")


def _load_py_module(fname, pkg="frac_Fourier"):
    spec = spec_from_file_location(fname, os.path.join(_PATH_ROOT, fname))
    py = module_from_spec(spec)
    spec.loader.exec_module(py)
    return py


about = _load_py_module("__about__.py")
setup_tools = _load_py_module("setup_tools.py")

setup(
    name='frac_Fourier',
    version=__version__,

    url='https://github.com/rnwatanabe/frac_Fourier',
    author='Renato N. Watanabe',
    author_email='renato.watanabe@ufabc.edu.br',

    py_modules=['frac_Fourier'],

    install_requires=setup_tools._load_requirements(_PATH_ROOT),
)