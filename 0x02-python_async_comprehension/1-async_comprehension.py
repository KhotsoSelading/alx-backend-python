#!/usr/bin/env python3
"""
Topic: Python - Async Comprehension
Author: Khotso Selading
Date: 16-01-2024
"""
from typing import List
from importlib import import_module as using


async_generator = using('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """A function that reates a list of 10 numbers from a 10-number
    generator."""
    return [x async for x in async_generator()]
