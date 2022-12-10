import re

from ipykernel.ipkernel import IPythonKernel

INITIAL_RUN_TEMPLATE = """\
import sys

from hamilton import ad_hoc_utils
from hamilton import driver

_MODULES = dict()
"""

FUNCTION_CELL_TEMPLATE = """\
{code}

sys.modules.pop('{function_name}', None)
temp_module = ad_hoc_utils.create_temporary_module(
    {function_name},
    module_name='{function_name}'
)
_MODULES['{function_name}'] = temp_module

dr = driver.Driver(dict(), *_MODULES.values()) 
dr.execute(['{function_name}'], inputs=input_data)
"""

class HamiltonEagerKernel(IPythonKernel):
    """Kernel which eagerly executes Hamilton code.

    This allows you to run parts of the DAG just by running a Jupyter cell.

    The goal here was to prototype how, well, prototyping using Hamilton should feel.
    My sense is it should be at least as easy as prototyping using a Jupyter notebook,
    and right now it isn't: you need to define your functions in a different file,
    toggle back to your notebook, and then update your driver code to test your new or
    updated function. That's several clicks, plus typing.  The alternative is to use
    `ad_hoc_utils`, which is also laborious.

    It would be nice if instead you could just build up your DAG in Jupyter, testing as
    you go. This kernel implements that approach. 

    The risk of all this is that people write spaghetti code, so I'm not sure this is actually
    the right direction, but I do think it's an interesting experiment. If people could
    prototype rapidly in Hamilton, would that spur adoption?

    Note that this is a prototype which is missing a lot of things:
    1. We create a new module every time you run a cell, even if the function in the cell hasn't changed.
    2. We only allow running one function per cell (maybe good, but still confusing).
    3. The developer MUST define an `input_data` variable before running a node, and this is totally undocumented.
    """

    implementation = 'Hamilton Eager'
    implementation_version = '0.0.1'
    banner = "Hamilton Eager Kernel - Executes Hamilton Nodes At Function-Definition Time"

    _is_first_run = True

    async def do_execute(
        self,
        code: str,
        silent: bool,
        store_history: bool = True,
        user_expressions: bool = None,
        allow_stdin: bool = False,
        *,
        cell_id=None,
    ):
        match = re.match(r'^def\s(?P<function_name>[A-Za-z_][A-Za-z0-9_]+)', code)
        if match is not None:
            # This is a function we can treat as a node in a graph, so let's execute it
            # treating all the prior cells as upstream nodes in the same graph.
            function_name = match.groupdict()['function_name']
            code = FUNCTION_CELL_TEMPLATE.format(code=code, function_name=function_name)
            if self._is_first_run:
                code = f"{INITIAL_RUN_TEMPLATE}\n{code}"
                self._is_first_run = False

        return await super().do_execute(
            code,
            silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin,
            cell_id=cell_id
        )