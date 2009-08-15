from setuptools import setup, find_packages
import os

version = '1.0dev'

setup(name='plone.app.jqtools',
      version=version,
      description="JQuery Tools Integration for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
        ],
      keywords='Plone JQuery',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.app.jqtools',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFCore',
          'Products.GenericSetup',
      ],
      entry_points="""
          [z3c.autoinclude.plugin]
          target = plone
      """,
      )
