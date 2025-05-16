import os
import json
import gymnasium as gym

from src.grid import Grid
from src.config import *
from src.utils import *

from abc import abstractmethod

class GridAgentTask(gym.Env):   
    def __init__(self,
                 task_name: str = "GridAgentTask",
                 grid_size: int = GRID_SIZE,
                 bag_size: int = BAG_SIZE,
                 tile_px: int = TILE_PIXEL,
                 high_level: bool = False,
                 max_steps: int = MAX_STEP):
        
        super().__init__()
        
        # task settings
        
        task_name = task_name.rsplit("_", 1)
        self.name = task_name[0]
        self.level = int(task_name[1][-1])
        self.grid = Grid(grid_size, bag_size, tile_px)
        self.high_level = high_level
        
        # train settings
        self.cur_step = 0
        self.max_steps = max_steps
        self.iter = 0
        
        self.observation_space =  gym.spaces.Box(low=0, high=255, shape=(*RESOLUTION, 4), dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(1) # will change later
    
    def reset(self, *, seed = None, options = None):
        """
        Reset when a new game starts.
        """
        # settings reset
        self.grid.reset()
        self.iter += 1
        self.cur_step = 0
        
        # generate game
        self.generate_game()
        
        # return the observation
        obs = self.render()
        return obs
    
    def step(self, action: int):
        """
        Take high-level or low-level action based on self.high_level.
        """
        
        self.cur_step += 1

        step_success, task_success, terminated = self.high_level_step(action) \
            if self.high_level else self.low_level_step(action)

        # check whether the game is over
        truncated = True if self.cur_step >= self.max_steps else False
        
        # print infos
        # if task_success and (terminated or truncated):
        #     print("!!!!!!! Task success !!!!!!!")
        # elif terminated or truncated:
        #     print("....... Task failed .......")
        
        obs = self.render()
        
        # reward is always 0(no meaning)
        return obs, 0, terminated, truncated, {"step_success": step_success, 
                                               "task_success": task_success}    
    
    def low_level_step(self, action: int):
        """
        Take low-level action.
        """
        step_success = False
        # 0-3: move down/right/up/left
        if 0 <= action < 4:
            step_success = self.grid.try_move(action)
        # 4: rotate clockwise
        elif action == 4:
            step_success = self.grid.try_rotate()
        # 5: pick
        elif action == 5:
            step_success = self.grid.try_pick()
        # >=6: drop
        elif action >= 6:
            step_success = self.try_drop(action - 6)

        task_success, terminated = self.check_goal()
        return step_success, task_success, terminated
    
    def high_level_step(self, action: int):
        """
        Take high-level action based on the task.
        """
        # action id out of range
        if action >= len(self.actions):
            return False, False, False
     
        instruction = self.actions[action]
        low_level_actions = self.extract_actions(instruction) # TODO: low level actions is None
        # print(f'low level actions: {low_level_actions}')
        step_suceess_list = []
        # check whether the action is "continue"
        if low_level_actions == ["continue"]:
            step_success, task_success, terminated = True, False, False
        else:
            for low_level_action in low_level_actions:
                step_success, task_success, terminated = self.low_level_step(low_level_action)
                step_suceess_list.append(step_success)
                if terminated:
                    break
        # all low-level actions are successful means high-level action is successful
        step_success = all(step_suceess_list)
        # re-generate actions if high-level action is successful(but not terminated)
        if step_success:
            self.actions = self.generate_actions()
            if not terminated: # action space should always > 0
                self.action_space = gym.spaces.Discrete(len(self.actions)) 
                # print(f"Actions: {self.actions}")
        self.render()
        return step_success, task_success, terminated
    
    @abstractmethod
    def get_info_img(self):
        """
        Get the information image.
        """
        info_bg = np.ones((TILE_PIXEL * 9, TILE_PIXEL * 2, 4), dtype = np.uint8) * 255
        return info_bg
    
    def get_template(self) -> dict:
        """
        Get the goal/action template.
        """
        with open(TEMPLATE_JSON_PATH, "r") as f:
            template = json.load(f)
        
        task_template = template[self.name]
        for task_level_template in task_template:
            if task_level_template["level"] == self.level or (isinstance(task_level_template["level"], list) and self.level in task_level_template["level"]):
                return task_level_template
 
    def render(self):
        """
        Render the current scene based on the task.
        """
        grid_img = self.grid.render()
        bg_img_path = os.path.join(IMG_BASE_PATH, f"{self.type}/{RESOURCE[self.type]['background']}.png")
        bg_img = LoadImage(bg_img_path)
        
        
        if self.type == "figure":
            img = ImgOverlay(bg_img, grid_img, bottom_center=True, offset = (TILE_PIXEL, -122))
        elif self.type == "maze":
            img = ImgOverlay(bg_img, grid_img, bottom_center=True, offset = (0, -TILE_PIXEL))
        else:
            img = ImgOverlay(bg_img, grid_img, bottom_center=True)
            
        bag_img = self.bag.render()
        combined_img = ImgCombine(img, bag_img, pad_h=True)
        
        if self.side_bar:
            combined_img = ImgCombine(self.get_info_img(), combined_img, pad_h=False)
            
        return combined_img
    
    def generate_game(self):
        """
        Generate the game based on the task.
        """
        # generate random map
        while True:
            self.grid.reset()
            self.generate_scene_and_goal()
            self.grid.gen_random_scene()
            if self.check_grid():
                break
        self.actions = self.generate_actions()
        random.shuffle(self.actions)
        self.action_space = gym.spaces.Discrete(len(self.actions))
        # print(f"\n======= {self.name} Iteration: {self.iter} =======")
        # print(f"Goal: {self.goal}")
        # print(f"Actions: {self.actions}")
    
    @abstractmethod
    def generate_scene_and_goal(self):
        """
        Generate the scene and goal based on the task.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_actions(self) -> list:
        """
        Generate high-level action list based on the task.
        """
        raise NotImplementedError
    
    @abstractmethod
    def extract_actions(self, instruction: str) -> list:
        """
        Extract the low-level actions from the high-level instruction.
        """
        raise NotImplementedError
    
    @abstractmethod
    def check_grid(self) -> bool:
        """
        Check if the grid is solvable and feasible.
        """
        def check(self, grid, queue, visited):
            num = 0
            while queue:
                x, y = queue.popleft()
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    # make sure in grid
                    if not self.grid.in_grid(nx, ny):
                        continue
                    # make sure not visited
                    if (nx, ny) in visited:
                        continue
                    if grid[nx, ny] == 0:
                        queue.append((nx, ny))
                    if grid[nx, ny] == 1:
                        num += 1
                    # mark as visited
                    visited.add((nx, ny))         
            return num
        
        grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        for obj in self.grid.objs:
            if obj.pos is None:
                return False
            grid[obj.pos[1]][obj.pos[0]] = 1
        
        start_pos = tuple(self.agent.pos[::-1])
        queue = deque([start_pos])
        visited = set([start_pos])
        
        if check(self, grid, queue, visited) != len(self.grid.objs):
            return False     
            
        return True
    
    @abstractmethod
    def check_goal(self) -> tuple[bool, bool]:
        """
        Check whether the goal is achieved based on the task.
        Return: task_success(bool), terminated(bool)
        """
        raise NotImplementedError
    
    @property
    def agent(self):
        return self.grid.agent
    
    @property
    def bag(self):
        return self.agent.bag
    
    @abstractmethod
    def try_drop(self, idx: int):
        """
        Try to drop the object at specific index.
        Based on the task.
        """
        return self.grid.try_drop(idx)
    
    def save_obs(self, path: str) -> str:
        """
        Save the observation image.
        """
        SaveImage(self.render(), path)
        