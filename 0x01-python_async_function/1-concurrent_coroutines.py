#!/usr/bin/env python3
"""
Topic: Python - Async
Author: Khotso Selading
Date: 08-01-2024
"""
import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ A program that spawns wait_random n times with the specified max_delay,
    then wait_n returns the list of all the delays (float values).
    """
    time_delayed = await asyncio.gather(
        *tuple(map(lambda _: wait_random(max_delay), range(n)))
    )
    return sorted(time_delayed)
