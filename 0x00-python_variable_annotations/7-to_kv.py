#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 7-to_kv.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ Converts a key and its value to a tuple of the key and
    the square of its value. """
    return (k, float(v**2))
