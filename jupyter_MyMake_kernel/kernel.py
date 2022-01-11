###%file:make_kernel.py
#
#   MyMake Jupyter Kernel
#   generated by MyPython
#
from math import exp
from queue import Queue
from threading import Thread
from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from jinja2 import Environment, PackageLoader, select_autoescape,Template
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple, Sequence
from shutil import copyfile,move
from urllib.request import urlopen
import socket
import copy
import mmap
import contextlib
import atexit
import platform
import atexit
import base64
import urllib.request
import urllib.parse
import pexpect
import signal
import typing 
import typing as t
import re
import signal
import subprocess
import tempfile
import os
import stat
import sys
import traceback
import os.path as path
import codecs
import time
import importlib
import importlib.util
import inspect
from . import ipynbfile
from plugins import ISpecialID
# from plugins.ISpecialID import IStag,IDtag,IBtag,ITag,ICodePreproc
from plugins._filter2_magics import Magics
from .Mymacroprocessor import Mymacroprocessor
try:
    zerorpc=__import__("zerorpc")
    # import zerorpc
except:
    pass
fcntl = None
msvcrt = None
bLinux = True
if platform.system() != 'Windows':
    fcntl = __import__("fcntl")
    bLinux = True
else:
    msvcrt = __import__('msvcrt')
    bLinux = False
from .MyKernel import MyKernel
class MakeKernel(MyKernel):
    kernel_info={
        'info':'[MyMake Kernel]',
        'extension':'.makefile',
        'execsuffix':'',
        'needmain':'',
        'compiler':{
            'cmd':'',
            'clargs':[],
            'crargs':[],
        },
        'interpreter':{
            'cmd':'make',
            'clargs':['-f'],
            'crargs':[],
        },
    }
    implementation = 'jupyter_MyMake_kernel'
    implementation_version = '1.0'
    language = 'Make'
    language_version = ''
    language_info = {'name': 'text/make',
                     'mimetype': 'text/make',
                     'file_extension': kernel_info['extension']}
    runfiletype='script'
    banner = "Make kernel.\n" \
             "Uses Make, compiles in make, and creates source code files and executables in temporary folder.\n"
    main_head = "\n" \
            "\n" \
            "int main(List<String> arguments){\n"
    main_foot = "\nreturn 0;\n}"
    
##//%include:../../src/comm_attribute.py
    def __init__(self, *args, **kwargs):
        super(MakeKernel, self).__init__(*args, **kwargs)
        self.runfiletype='script'
        self.kernelinfo="[MyMakeKernel{0}]".format(time.strftime("%H%M%S", time.localtime()))
#################
    def getout_filename(self,cflags,defoutfile):
        outfile=''
        binary_filename=defoutfile
        index=0
        for s in cflags:
            if s.startswith('-o'):
                if(len(s)>2):
                    outfile=s[2:]
                    del cflags[index]
                else:
                    outfile=cflags[cflags.index('-o')+1]
                    if outfile.startswith('-'):
                        outfile=binary_filename
                    del cflags[cflags.index('-o')+1]
                    del cflags[cflags.index('-o')]
            binary_filename=outfile
            index+=1
        return binary_filename
    def compile_with_sc(self, source_filename, binary_filename, cflags=None, ldflags=None,env=None,magics=None):
        outfile=binary_filename
        orig_cflags=cflags
        orig_ldflags=ldflags
        ccmd=[]
        clargs=[]
        crargs=[]
        # index=0
        # for s in cflags:
        #     if s.startswith('--outFile'):
        #         if(len(s)>9):
        #             outfile=s[9:]
        #             del cflags[index]
        #         else:
        #             outfile=cflags[cflags.index('--outFile')+1]
        #             if outfile.startswith('-'):
        #                 outfile=binary_filename
        #             del cflags[cflags.index('--outFile')+1]
        #             del cflags[cflags.index('--outFile')]
        #     binary_filename=outfile
        #     index+=1
        binary_filename=self.getout_filename(cflags,outfile)
        args=[]
        if magics!=None and len(self.mymagics.addkey2dict(magics,'ccompiler'))>0:
            args = magics['ccompiler'] + orig_cflags +[source_filename] + orig_ldflags
        else:
            if len(self.kernel_info['compiler']['cmd'])>0:
                ccmd+=[self.kernel_info['compiler']['cmd']]
            if len(self.kernel_info['compiler']['clargs'])>0:
                clargs+=self.kernel_info['compiler']['clargs']
            if len(self.kernel_info['compiler']['crargs'])>0:
                crargs+=self.kernel_info['compiler']['crargs']
            args = ccmd+cflags+[source_filename] +clargs+ [binary_filename]+crargs+ ldflags
        # self._log(''.join((' '+ str(s) for s in args))+"\n")
        return self.mymagics.create_jupyter_subprocess(args,env=env,magics=magics),binary_filename,args
    def _exec_sc_(self,source_filename,magics):
        self.mymagics._logln('Generating executable file')
        with self.mymagics.new_temp_file(suffix=self.kernel_info['execsuffix']) as binary_file:
            magics['status']='compiling'
            p,outfile,tsccmd = self.compile_with_sc(
                source_filename, 
                binary_file.name,
                self.mymagics.get_magicsSvalue(magics,'cflags'),
                self.mymagics.get_magicsSvalue(magics,'ldflags'),
                self.mymagics.get_magicsbykey(magics,'env'),
                magics=magics)
            returncode=p.wait_end(magics)
            p.write_contents()
            magics['status']=''
            binary_file.name=os.path.join(os.path.abspath(''),outfile)
            if returncode != 0:  # Compilation failed
                self.mymagics._logln(' '.join((str(s) for s in tsccmd))+"\n",3)
                self.mymagics._logln("TSC compiler exited with code {}, the executable will not be executed".format(returncode),3)
                # delete source files before exit
                os.remove(source_filename)
                os.remove(binary_file.name)
        return p.returncode,binary_file.name
##do_runcode
    def do_runcode(self,return_code,fil_ename,magics,code, silent, store_history=True,
                    user_expressions=None, allow_stdin=True):
        return_code=return_code
        fil_ename=fil_ename
        bcancel_exec=False
        retinfo=self.mymagics.get_retinfo()
        retstr=''
        ##代码运行前
        interpreter=[]
        if len(self.kernel_info['interpreter']['cmd'])>0:
            interpreter+=[self.kernel_info['interpreter']['cmd']]
            if len(self.kernel_info['interpreter']['clargs'])>0:
                interpreter+=self.kernel_info['interpreter']['clargs']
            interpreter+=[fil_ename]
            if len(self.kernel_info['interpreter']['crargs'])>0:
                interpreter+=self.kernel_info['interpreter']['crargs']
        cmd=[fil_ename]
        if len(interpreter)>0:
            cmd=interpreter
        p = self.mymagics.create_jupyter_subprocess(cmd+ magics['_st']['args'],cwd=None,shell=False,env=self.mymagics.addkey2dict(magics,'env'),magics=magics)
        self.mymagics.g_rtsps[str(p.pid)]=p
        return_code=p.returncode
        ##代码启动后
        # bcancel_exec,retstr=self.raise_plugin(code,magics,return_code,fil_ename,3,2)
        # if bcancel_exec:return bcancel_exec,retinfo,magics, code,fil_ename,retstr
         
        if magics!=None and len(self.mymagics.addkey2dict(magics,'showpid'))>0:
            self.mymagics._write_to_stdout("The process PID:"+str(p.pid)+"\n")
        return_code=p.wait_end(magics)
        ##代码运行结束
        # self.cleanup_files()
        if p.returncode != 0:
            self.mymagics._log("Executable exited with code {}".format(p.returncode),2)
        return bcancel_exec,retinfo,magics, code,fil_ename,retstr
##do_compile_code
    def do_compile_code(self,return_code,fil_ename,magics,code, silent, store_history=True,
                    user_expressions=None, allow_stdin=True):
        return_code=0
        fil_ename=fil_ename
        sourcefilename=fil_ename
        bcancel_exec=False
        retinfo=self.mymagics.get_retinfo()
        retstr=''
        if len(self.kernel_info['compiler']['cmd'])>0:
            returncode,binary_filename=self._exec_sc_(fil_ename,magics)
            fil_ename=binary_filename
            return_code=returncode
        
            if returncode!=0:return  True,retinfo, code,fil_ename,retstr
        return bcancel_exec,retinfo,magics, code,fil_ename,retstr
##do_make_create_codefile
    def do_create_codefile(self,magics,code, silent, store_history=True,
                    user_expressions=None, allow_stdin=True):
        return_code=0
        fil_ename=''
        bcancel_exec=False
        retinfo=self.mymagics.get_retinfo()
        retstr=''
        
        source_file=self.mymagics.create_codetemp_file(magics,code,suffix=self.kernel_info['extension'])
        newsrcfilename=source_file.name
        fil_ename=newsrcfilename
        return_code=True
        
        return bcancel_exec,retinfo,magics, code,fil_ename,retstr
##do_make_preexecute
    def do_preexecute(self,code, magics,silent, store_history=True,
                user_expressions=None, allow_stdin=False):
        bcancel_exec=False
        retinfo=self.mymagics.get_retinfo()
        if (len(self.mymagics.addkey2dict(magics,'noruncode'))<1 
            and len(self.kernel_info['needmain'])>0 ):
            magics, code = self.mymagics._add_main(magics, code)
        return_code=0
        fil_ename=''
        return bcancel_exec,retinfo,magics, code
