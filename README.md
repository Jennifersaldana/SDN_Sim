# SDN Controller Simulator

A simplified Software-Defined Networking (SDN) controller written in Python. This controller simulates OpenFlow-like behavior by maintaining a network topology, routing traffic, handling failures, and visualizing flows.

## Features

- Network topology management (nodes and links)
- Shortest path computation with load balancing
- Traffic type prioritization
- Automatic rerouting on link failure
- Visualization of topology and link utilization
- Simple CLI interface


## Requirements

- Python 3.x
- `networkx`
- `matplotlib`

Install dependencies:

```
pip install networkx matplotlib
```

## Extensions
1. Python Debugger
2. Python
3. Pylance


## How to Run
Be sure to have VScode first. Here is the link download the application: https://code.visualstudio.com/download

```
1. Open VScode, enable extensions, and create an empty folder
2. cd into folder directory
3. Use the command "git clone 'githubURL'" in the terminal
4. cd into folder directory
5. Create Python environment
- Mac: Ctrl + Shift + P
- Create Python environment with venv
- Activiate the environment by running "source .venv/bin/activate" in the terminal 
- Close terminal and open it again
6. Download dependencies if needed "pip install networkx matplotlib"
7. Run the program by running "python3 sdn.py" in terminal
8. Test
```

## Example Run
```
add node A
add node B
add node C
add node D
add link A B 1
add link B C 1
add link C D 1
add link A D 5
inject traffic A D alerts 10
inject traffic A C video 5
inject traffic B D voice 3
visualize
simulate link failure C D
visualize
query routing A D
remove link a b
visualize
add link a b 2
inject traffic A B data 7
remove node D
visualize
```
