#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 5-sum_list.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """ Computes the sum of a list of floating-point numbers. """
    if input_list is None:
        return 0
    else:
        return float(sum(input_list))
