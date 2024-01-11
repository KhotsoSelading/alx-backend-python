#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 9-element_length.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Computes the length of a list of sequences. """
    return [(i, len(i)) for i in lst]
