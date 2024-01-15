#!/usr/bin/env python3
"""
Topic: Python - Async
Author: Khotso Selading
Date: 08-01-2024
"""
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """ A program that takes an integer max_delay
    and returns a asyncio.Task. """
    return asyncio.create_task(wait_random(max_delay))
