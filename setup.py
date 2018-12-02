"""
Setup script for 'bif' library.
"""

from setuptools import setup

# Note: installing pcpp from github and not pypi
# because we depend on PR #7 which has not (as of
# writing) been merged.
#
# See https://github.com/ned14/pcpp/pull/7

setup(name='bif',
      version='0.1',
      description='Basic image format',
      url='http://github.com/nathanrw/single-header-c-libs-in-python',
      author='Nathan Woodward',
      author_email='nathanrichardwoodward@gmail.com',
      license='Public domain',
      setup_requires=["cffi>=1.0.0", "ply", "pcpp==1.0.1"],
      cffi_modules=["build.py:maker"],
      install_requires=["cffi>=1.0.0"],
      dependency_links=["http://github.com/nathanrw/pcpp/tarball/master#egg=pcpp-1.0.1"],
      zip_safe=False)