# Rate Limiter Algorithms in Python

Small standard-library implementations of three common rate-limiting algorithms.

## Algorithms

- **Fixed window:** allows a fixed number of requests during each time window.
- **Leaky bucket:** queues requests up to a capacity and processes them at a steady rate.
- **Token bucket:** starts full, consumes one token per request, and replenishes tokens in the background.

## Requirements

- Python 3.12 or newer
- No third-party dependencies

## Run the simulations

Run every simulation:

```bash
python main.py
```

Run one algorithm:

```bash
python main.py fixed
python main.py leaky
python main.py token
```

The output shows which requests are accepted, rejected, queued, processed, or served after a refill.

## Run the tests

```bash
python -m unittest -v test_rate_limiters.py
```

## Project layout

```text
main.py                         Simulation driver
src/fixed_window.py             Fixed-window limiter
src/leaky_bucket.py             Leaky-bucket limiter
src/token_bucket/token_bucket.py Token-bucket limiter
src/token_bucket/linked_list.py Token storage used by the token bucket
test_rate_limiters.py           Focused unit tests
```

Call `TokenBucket.stop()` when finished with a token bucket to stop its refill thread cleanly.
