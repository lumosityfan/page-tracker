"""A simple Flask app that tracks page views using Redis."""

# src/page_tracker/app.py

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """Index function that increments and displays page views."""
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{PENSIVE FACE}", 500
    return f"This page has been seen {page_views} times."


@cache
def redis():
    """A cached function that returns a Redis client."""
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
