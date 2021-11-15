import time

_this_year = time.strftime("%Y")
__version__ = "dev"
__author__ = "Renato N. Watanabe    "
__author_email__ = "renato.watanabe@ufabc.edu.br"
__license__ = "GNU 3.0"
__copyright__ = f"Copyright (c) 2021-{_this_year}, {__author__}."
__homepage__ = "https://github.com/rnwatanabe/frac_Fourier"
__docs__ = (
    "Frac_Fourier is a package to compute the fractional Fourier"
    "transform written in PyTorch"
)
__long_docs__ = """
    Frac_Fourier is a package to compute the fractional Fourier
    transform written in PyTorch
"""

__all__ = ["__author__", "__author_email__", "__copyright__", "__docs__", "__homepage__", "__license__", "__version__"]