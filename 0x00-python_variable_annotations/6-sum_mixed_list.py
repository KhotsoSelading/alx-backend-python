#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 6-sum_mixed_list.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ Computes the sum of a list of integers and floating-point numbers. """
    return float(sum(mxd_lst))
