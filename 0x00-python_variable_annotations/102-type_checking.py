#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 102-type_checking.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """ Creates multiple copies of items in a tuple. """
    zoomed_in: List = [
        item for item in lst
        for i in range(int(factor))
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
