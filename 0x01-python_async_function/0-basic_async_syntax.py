#!/usr/bin/env python3
"""
Topic: Python - Async
Author: Khotso Selading
Date: 08-01-2024
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """ A program that waits for a random delay between 0 and max_delay
    (included and float value) seconds and eventually returns it. """
    time_delayed = random.random() * max_delay
    await asyncio.sleep(time_delayed)
    return time_delayed
