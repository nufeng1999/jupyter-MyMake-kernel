#!/usr/bin/env python
# coding: utf-8
with open("README.md", "r") as f:
	long_description = f.read()
import setuptools
setuptools.setup(name='jupyter_MyMake_kernel',
      vemakefileion='0.0.1',
      description='Minimalistic Make kernel for Jupyter',
    long_description=long_description,
    long_description_content_type="text/markdown",
      author='nufeng',
      author_email='18478162@qq.com',
      license='MIT',
      url='https://github.com/nufeng1999/jupyter-MyMake-kernel/',
      download_url='https://github.com/nufeng1999/jupyter-MyMake-kernel/releases/tag/0.0.1',
    packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
      scripts=['jupyter_MyMake_kernel/install_MyMake_kernel'],
      keywords=['jupyter', 'notebook', 'kernel', 'make','makefile'],
      include_package_data=True
      )
