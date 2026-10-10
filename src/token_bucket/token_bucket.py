"""Threaded token-bucket rate limiter."""

import threading
import uuid
from .linked_list import LinkedList

class TokenBucket:
    """Spend prefilled tokens and replenish one token per interval."""

    def __init__(self, capacity:int, fill_rate_seconds:int) -> None:
        """Create a full bucket and start its background refill worker."""
        if capacity <= 0 or fill_rate_seconds <= 0:
            raise ValueError("capacity and fill_rate_seconds must be positive")
        self.capacity = capacity
        self.fill_rate_seconds = fill_rate_seconds
        self.bucket = LinkedList(capacity)
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        for _ in range(capacity):
            self.bucket.append({"id": uuid.uuid4()})
        self.fill_thread = threading.Thread(target=self.fill_bucket, daemon=True)
        self.fill_thread.start()

    def fill_bucket(self):
        """Add one token per interval until the bucket is stopped."""
        while not self.stop_event.wait(self.fill_rate_seconds):
            with self.lock:
                response = self.bucket.append({"id": uuid.uuid4()})
                print(f"Filling bucket:{response}")

    def fetch_token(self) -> dict:
        """Atomically consume and return one token."""
        with self.lock:
            return self.bucket.pop()

    def stop(self) -> None:
        """Stop and join the background refill worker."""
        self.stop_event.set()
        self.fill_thread.join()
