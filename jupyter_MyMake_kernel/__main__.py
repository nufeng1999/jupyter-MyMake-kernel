from ipykernel.kernelapp import IPKernelApp
from .kernel import MakeKernel
IPKernelApp.launch_instance(kernel_class=MakeKernel)
