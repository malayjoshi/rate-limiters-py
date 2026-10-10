"""Fixed-window rate limiter."""

import datetime
from datetime import timedelta


class FixedWindow:
    """Allow a fixed number of requests during each time window."""

    def __init__(self, max_requests:int, seconds_window:int) -> None:
        """Create a limiter with a request limit and window duration."""
        if max_requests <= 0 or seconds_window <= 0:
            raise ValueError("max_requests and seconds_window must be positive")
        self.max_requests = max_requests
        self.seconds_window = seconds_window
        self.counter = self.max_requests
        self.start_time = None
        self.end_time = None
        self.requests_per_window = [[]]


    def add_request(self, data:dict, now = None) -> dict:
        """Record a request and report whether the current window allows it."""
        if now is None:
            now = datetime.datetime.now()
        if self.start_time is None:
            self.start_time = now
            self.end_time = self.start_time + timedelta(seconds=self.seconds_window)
        elif now >= self.end_time:
            # The request that crosses the boundary belongs to the new window.
            self.add_new_window(now)

        if self.counter == 0:
            return {"allowed":False, "limit_left":0}

        self.requests_per_window[-1].append(data)
        self.counter -= 1
        print(f"Request:{data} was placed in window:{len(self.requests_per_window) - 1}")
        return {"allowed":True, "limit_left":self.counter}

    def add_new_window(self, now):
        """Start an empty window at ``now`` and reset its allowance."""
        self.counter = self.max_requests
        self.start_time = now
        self.end_time = self.start_time + timedelta(seconds=self.seconds_window)
        # Only the active window is needed; discard stale request history.
        self.requests_per_window = [[]]
