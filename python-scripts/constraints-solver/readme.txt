
Installation
------------
pip install python-constraint
pip install morph

#may require additional pkgs


Link to python constraint-solver package
-----------------------------------------
https://github.com/python-constraint/python-constraint


The const_solver.py script is based on the "python-constraint" package.
This script in an envelope to the python-constraint package and provides a simple inteface to using it.
The concept behind this environment is to enables the user by composing a set of json files to run use cases
without the need to write any python code


usage example
-------------
cd path\to\cs
python.exe const_solver.py root.json


root.json is a list of 3 other jason files that participate in a use case execution

more info in:
--------------
constraint.pptx


output
-------
The results after running the use case will reside in the workdir folder

