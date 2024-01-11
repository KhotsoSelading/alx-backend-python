#!/usr/bin/env python3
"""
Topic: Python Variable Annotations
Task: 100-safe_first_element.py
Author: Khotso Selading
Date: 11-01-2024
"""
from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ Retrieves the first element of a sequence if it exists. """
    if lst:
        return lst[0]
    else:
        return None
