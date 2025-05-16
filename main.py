import argparse
from task.config import *
from eval.evaluation import Evaluation

def main():
    parser = argparse.ArgumentParser(description=
        'KidGym: A 2D Reasoning Benchmark for MLLMs Inspired by Children Intelligence Tests')
    parser.add_argument("task", type=str, help="Task Name")
    args = parser.parse_args()
    evaluation = Evaluation()
    evaluation.change_task(args.task)
    evaluation.run()

if __name__ == '__main__':
    main()
