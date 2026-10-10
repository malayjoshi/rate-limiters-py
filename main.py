"""Command-line simulations for the included rate-limiting algorithms."""

import argparse
import time
from datetime import datetime, timedelta

from src.fixed_window import FixedWindow
from src.leaky_bucket import LeakyBucket
from src.token_bucket.token_bucket import TokenBucket


def simulate_fixed_window():
    """Show acceptance, rejection, and rollover of a fixed window."""
    limiter = FixedWindow(max_requests=2, seconds_window=5)
    start = datetime.now()

    for request_id, seconds in enumerate((0, 1, 2, 5), start=1):
        result = limiter.add_request(
            {"id": request_id}, start + timedelta(seconds=seconds)
        )
        print(f"t={seconds}s request={request_id}: {result}")


def simulate_leaky_bucket():
    """Show queue capacity and fixed-rate request processing."""
    limiter = LeakyBucket(capacity=3, leak_rate_seconds=0.5)

    for request_id in range(1, 5):
        accepted = limiter.add_request({"id": request_id})
        print(f"request={request_id}: queued={accepted}")

    while not limiter.queue.empty():
        time.sleep(limiter.leak_rate_seconds)
        print(f"processed: {limiter.dequeue_request()}")


def simulate_token_bucket():
    """Show initial token capacity and background replenishment."""
    limiter = TokenBucket(capacity=3, fill_rate_seconds=0.5)
    try:
        for request_id in range(1, 5):
            print(f"request={request_id}: {limiter.fetch_token()}")

        time.sleep(limiter.fill_rate_seconds + 0.1)
        print(f"after refill: {limiter.fetch_token()}")
    finally:
        limiter.stop()


SIMULATIONS = {
    "fixed": simulate_fixed_window,
    "leaky": simulate_leaky_bucket,
    "token": simulate_token_bucket,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate rate-limiting algorithms")
    parser.add_argument("algorithm", choices=[*SIMULATIONS, "all"], nargs="?", default="all")
    args = parser.parse_args()

    selected = SIMULATIONS if args.algorithm == "all" else {args.algorithm: SIMULATIONS[args.algorithm]}
    for name, simulate in selected.items():
        print(f"\n--- {name.replace('_', ' ').title()} ---")
        simulate()
