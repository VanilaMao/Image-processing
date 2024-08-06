from dataclasses import dataclass


@dataclass
class ProcessConfig:
    left_min:int =0
    left_max:int = 0
    right_min:int=0
    right_max:int=0
    particle_size_max:int = 0
    particle_size_min:int=0
    background:int =100
    start:int = 0
    end:int =0
    first_second_shift:bool = False
