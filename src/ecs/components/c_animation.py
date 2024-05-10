from typing import List
import pygame

class CAnimation:

    def __init__(self, animations:dict) -> None:
        self.number_frames = animations['number_frames']
        self.animations_list: List[AnimationData] = []
        for anim in animations['list']:
            animation_data = AnimationData(anim['name'],
                                           anim['start'],
                                           anim['end'],
                                           anim['framerate'])
            self.animations_list.append(animation_data)
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animations_list[self.current_animation].start

   
class AnimationData:
    def __init__(self, name:str, start:int, end:int, framerate:float ) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0/framerate