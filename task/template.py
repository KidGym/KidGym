import random
from src.obj import Obj
from src.task import GridAgentTask
from src.config import *
from src.utils import *

class Classification(GridAgentTask):
    def __init__(self, 
                 **kwargs):
        """
        Your set up here.
        """
        super().__init__(**kwargs)

        
    def generate_scene_and_goal(self):
        """
        Your goal here.
        """
        pass

    def render(self):
        """
        Render the current scene based on the task.
        """
        return super().render()
    
    def check_grid(self) -> bool:
        """
        Check if the grid is solvable and feasible.
        """
        return super().check_grid()
        
    def generate_actions(self) -> list:
        """
        Your actions here.
        """
        pass

    def check_goal(self) -> tuple[bool, bool]:
        """
        Check whether the goal is achieved based on the task.
        """
        pass
