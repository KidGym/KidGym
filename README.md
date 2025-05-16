# Children's Intelligence Tests Pose Challenges for MLLMs? KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs

## Install

[![python version](https://img.shields.io/badge/Python_Version_%3E=_3.10-green)](https://www.python.org/downloads/release/python-3100/)

It is highly recommended to use [Anaconda](https://www.anaconda.com/download/) for managing your python packages.

```sh
$ pip install -r requirements.txt
```

## Run
The repository's code structure is as follows:

```sh
├── src/
│   ├── agent.py
│   ├── bag.py
│   ├── grid.py
│   ├── obj.py
│   └── ...   
├── task/
│      ├── task_1.py
│      ├── task_2.py
│      └── ...
└── main.py
```

Each task type is a **class** file located in `task/` and you can run it by:

```sh
python main.py [task_gym_environment]
```

## Tasks
| Task Name      | Required Capability             | Task Gym Environment |
|:---------------|:--------------------------------|:-------------------- |
| Classification | Execution                       | CL_L1/CL_L2/CL_L3    |
| Selection      | Memory                          | SE_L1/SE_L2/SE_L3    |
| Decode         | Learning                        | DE_L1/DE_L2/DE_L3    |
| Maze           | Planning                        | MA_L1/MA_L2/MA_L3    |
| Filling        | Perception Reasoning            | FI_L1/FI_L2/FI_L3    |
| Puzzle         | Perception Reasoning (Abstract) | PU_L1/PU_L2/PU_L3    |
| Maze*          | Planning + Memory               | MMA_L1/MMA_L2/MMA_L3 |
| Decode*        | Learning + Memory               | MDE_L1/MDE_L2/MDE_L3 |
| Sorting        | Execution + Learning            | SO_L1/SO_L2/SO_L3    |
| Placement      | Execution + Learning            | PL_L1/PL_L2/PL_L3    |
| Filling*       | Perception Reasoning + Memory   | MFI_L1/MFI_L2/MFI_L3 |
| Counting       | Perception Reasoning + Planning | CO_L1/CO_L2/CO_L3    |

All gym envrionments can be found at [task/config.py](./task/config.py).

## Create
Users can easily create their own tasks by referring to [template.py](./task/template.py).
