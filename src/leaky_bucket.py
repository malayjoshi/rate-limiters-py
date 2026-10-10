"""Leaky-bucket queue that processes requests at a fixed rate."""

import time
import queue

class LeakyBucket:
    """Queue requests up to capacity and release them at fixed intervals."""

    def __init__(self, capacity, leak_rate_seconds):
        """Create a bucket with a maximum queue size and leak interval."""
        if capacity <= 0 or leak_rate_seconds <= 0:
            raise ValueError("capacity and leak_rate_seconds must be positive")
        self.capacity = capacity
        self.leak_rate_seconds = leak_rate_seconds
        self.queue = queue.Queue(maxsize=self.capacity)
        self.last_processed_time = time.time()

    def add_request(self, request:dict) -> bool:
        """Queue a request without blocking, or reject it when full."""
        was_empty = self.queue.empty()
        try:
            self.queue.put_nowait(request)
            if was_empty:
                self.last_processed_time = time.time()
            return True
        except queue.Full:
            return False

    def dequeue_request(self) -> dict | None:
        """Return the next request when a leak interval has elapsed."""
        current_time = time.time()
        elapsed_time = current_time - self.last_processed_time
        if elapsed_time < self.leak_rate_seconds:
            return None

        if self.queue.empty():
            return None

        # Advance by one interval so repeated calls can catch up after a delay.
        self.last_processed_time += self.leak_rate_seconds
        return self.queue.get()
