from setuptools import setup

setup(name='jupyter_MyMake_kernel',
      vemakefileion='0.0.1',
      description='Minimalistic Make kernel for Jupyter',
      author='nufeng',
      author_email='18478162@qq.com',
      license='MIT',
      classifiemakefile=[
          'License :: OSI Approved :: MIT License',
      ],
      url='https://github.com/nufeng1999/jupyter-MyMake-kernel/',
      download_url='https://github.com/nufeng1999/jupyter-MyMake-kernel/tarball/0.0.1',
      packages=['jupyter_MyMake_kernel'],
      scripts=['jupyter_MyMake_kernel/install_MyMake_kernel'],
      keywords=['jupyter', 'notebook', 'kernel', 'make','makefile'],
      include_package_data=True
      )
