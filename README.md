## What is this?

This is a quick demo of running Hamilton *eagerly* in Jupyter notebooks. That is, evaluating a cell causes the function in the cell to be treated as a node in a Hamilton graph, and evaluated as such immediately.

## Why?

For a framework like Hamilton to gain adoption, I believe that iteration speed needs to be on par with existing approaches. Today, Jupyter is the dominant approach to prototyping data analytics code; if people can't prototype in Jupyter using Hamilton as rapidly as they can with other frameworks, it seems reasonable that they'll be less likely to use Hamilton in general.

Of course, there are real downsides to translating notebook code directly to Hamilton: one of the benefits of Hamilton is that it asks you to be more intentional about your code than you'd be in a notebook.

So this isn't intended to be a production-ready solution. It's more of an exploration of how prototyping in Hamilton could feel, even if ultimately a more bespoke solution might make sense.

## How?

A major pain point to prototyping in Hamilton using Jupyter is iteration speed. You need to:

1. Write a function in a Python file.
2. Switch back to your notebook.
3. Update your driver to output the result of that function.

That's a lot of keypresses.

Instead, what if we could just write Hamilton code as usual, and then run it as we go? That would let us verify that each cell does what we expect, while also making it easy to transfer cells to a `.py` file once we're happy with them.

To allow this, I created a new Jupyter kernel which takes functions, turns them into adhoc modules, and then runs them in a driver whenever a cell is executed. This means that prototyping is as easy as writing a function and executing the node — no need to switch contexts.

## Improvements

Obviously this is a super brittle prototype. Here are some issues with it:
1. It requires that you define an `input_data` variable at the top of your notebook before defining any function.
2. It recreates the entire graph every time you execute a cell even though upstream cells have not changed.
3. It creates a new temporary module each time you execute a cell, even if the function body hasn't changed.
4. Error messages are going to be really confusing since I'm injecting a bunch of code into each cell before running it.
5. Things can get out of sync — if I edit a cell but don't run it, then downstream nodes won't pick up the latest code from that cell. This is how Jupyter works today but it's still confusing.

## Usage

1. Clone this repo.
2. Set up a virtual environment: `python3 -m venv .venv`
3. Activate the venv: `. .venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Install the kernel: `python -m hamilton_eager_kernel.install`
6. Open the `hello_world` notebook with the `hamilton_eager` kernel: `jupyter notebook hello_world.ipynb --MultiKernelManager.default_kernel_name=hamilton_eager`
7. Viola! Play around in the notebook and, as you define functions in cells, you'll see the result of executing that function in the DAG.
