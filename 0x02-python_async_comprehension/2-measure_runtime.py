#!/usr/bin/env python3
"""
Topic: Python - Async Comprehension
Author: Khotso Selading
Date: 16-01-2024
"""
import asyncio
import time
from importlib import import_module as using


async_comprehension = using('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """A function that executes async_comprehension 4 times and measures the
    total execution time. """
    start_time = time.time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    return time.time() - start_time
