#!/usr/bin/env python3
"""
Topic: Python - Async Comprehension
Author: Khotso Selading
Date: 16-01-2024
"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """A function that generates a sequence of 10 numbers. """
    for x in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
