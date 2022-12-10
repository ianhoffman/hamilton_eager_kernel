from ipykernel.kernelapp import IPKernelApp
from . import HamiltonEagerKernel

IPKernelApp.launch_instance(kernel_class=HamiltonEagerKernel)