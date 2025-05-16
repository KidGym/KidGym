import os
import re
import json
import string
import shutil
import pandas as pd
import gymnasium as gym
from pathlib import Path
from eval.prompt import Prompt

class Evaluation():
    def __init__(self):

        pass

    def change_task(self, task_name: str):
        """
        Change the task to evaluate.
        
        Args:
            task_name (str): Name of the task to evaluate. e.g., "Classification_L1", "Selection_L2", etc.
        """
        if task_name not in gym.envs.registry:
            raise ValueError(f"Task {task_name} not found in gym registry.")
        self.task = gym.make(task_name).unwrapped # only unwrap can visit attributes 
        
        # split task name, e.g., "CL_L1" -> ["CL", "L1"]
        split_task_name = task_name.rsplit("_", 1)
        task = split_task_name[0]
        level = split_task_name[1]
        
        # check if memory task
        if "Memory" in self.task.name or self.task.name == "Selection":
            self.si = False
        else:
            self.si = True
    
    def run(self):
        """
        Run the evaluation.
        """
        
        self.prompt = Prompt(self.task) # init prompt
                    
        while(True):        
            # reset
            self.task.reset()
            print(f"Goal: {self.task.goal}")
            # episode loop
            while True:
                self.task.save_obs(path = "./tmp.png")
                action_id = None
                while True:
                    print("Actions: " + self.prompt.generate_action_list())
                    answer = input(f"Please input the action letter:")
                    action_id = self.process_answer(answer, self.task.actions)
                    if self.task.actions == ['continue']:
                        action_id = 0
                    if action_id is None:
                        print("Invalid action. Try again.")
                    else:
                        break

                _, _, terminated, truncated, info = self.task.step(action_id)
                over = terminated or truncated
                
                # over judgement
                if over:
                    break
        
    def process_answer(self, answer: str, actions: list[str]) -> int | None:
        """
        e.g. 
            actions: A) 'action1' B) 'action2' C) 'action3'
            answer: "C"
            return: 2
        """
        # remove <answer> tags, only for cot
        match = re.search(r'<answer>(.*?)</answer>', answer)
        if match:
            answer = match.group(1)
        
        for i in range(len(actions)):
            if f"'{actions[i]}'" in answer:
                return i
            
        match = re.search(f"\\b([{string.ascii_uppercase[:len(actions)]}])\\b", answer)
        
        if not match:
            match = re.search(f"([{string.ascii_uppercase[:len(actions)]}])", answer)
        
        if match and string.ascii_uppercase.index(match.group(1)) < len(actions):
            index = string.ascii_uppercase.index(match.group(1))
            return index
        return None

                
                
            
            
            
            