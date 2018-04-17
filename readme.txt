README

In order to run “tsp_marco_rangan.py”, follow these steps:

1)	Install python 2.7.10 from the following website (choose the appropriate system specifications): https://www.python.org/downloads/release/python-2710/.
2)	Before you proceed make sure that the version of python you are running is indeed 2.7.10. Run the following command in the terminal: “alias python=python2.7”.
3)	Run “pip install graphviz” on the terminal/command line.
4)	Install gurobi from http://www.gurobi.com/downloads/download-center.
5)	Using the terminal, go to the installation directory of gurobi on your local machine and run “python setup.py install”.
6)	Using the terminal, go to the directory where the tsp_marco_rangan.py file is located.
7)	Run “gurobi.sh ./tsp_marco_rangan.py” in the terminal and you are good to go! 

NOTE: The code bundle also includes “tsp_solver_demo.py” which contains additional code that displays the original graph and the optimal tour at each iteration, including the final one.

