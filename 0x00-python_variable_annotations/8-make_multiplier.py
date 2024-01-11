#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 8-make_multiplier.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Creates a multiplier function. """
    return lambda x: x * multiplier
