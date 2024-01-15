#!/usr/bin/env python3
"""
Topic: Python - Async
Author: Khotso Selading
Date: 08-01-2024
"""
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ A program that executes task_wait_random n times. """
    time_delayed = await asyncio.gather(
        *tuple(map(lambda _: task_wait_random(max_delay), range(n)))
    )
    return sorted(time_delayed)
