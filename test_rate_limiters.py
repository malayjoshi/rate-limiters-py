import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.fixed_window import FixedWindow
from src.leaky_bucket import LeakyBucket
from src.token_bucket.linked_list import LinkedList
from src.token_bucket.token_bucket import TokenBucket


class RateLimiterTests(unittest.TestCase):
    def test_fixed_window_discards_stale_windows(self):
        limiter = FixedWindow(1, 10)
        now = datetime.now()
        self.assertTrue(limiter.add_request({"id": 1}, now)["allowed"])
        self.assertFalse(limiter.add_request({"id": 2}, now)["allowed"])
        self.assertTrue(limiter.add_request({"id": 3}, now + timedelta(seconds=10))["allowed"])
        self.assertTrue(limiter.add_request({"id": 4}, now + timedelta(seconds=20))["allowed"])
        self.assertEqual(limiter.requests_per_window, [[{"id": 4}]])

    @patch("src.leaky_bucket.time.time", side_effect=[0, 0, 3, 3, 3, 3])
    def test_leaky_bucket_preserves_elapsed_intervals(self, _):
        limiter = LeakyBucket(3, 1)
        self.assertTrue(limiter.add_request({"id": 1}))
        self.assertTrue(limiter.add_request({"id": 2}))
        self.assertTrue(limiter.add_request({"id": 3}))
        self.assertEqual(limiter.dequeue_request(), {"id": 1})
        self.assertEqual(limiter.dequeue_request(), {"id": 2})
        self.assertEqual(limiter.dequeue_request(), {"id": 3})
        self.assertIsNone(limiter.dequeue_request())

    def test_linked_list_clears_last_node(self):
        items = LinkedList(1)
        items.append({"id": 1})
        self.assertTrue(items.pop()["popped"])
        self.assertIsNone(items.head)
        self.assertIsNone(items.tail)

    def test_token_bucket_starts_full_and_stops(self):
        limiter = TokenBucket(1, 60)
        self.assertTrue(limiter.fetch_token()["popped"])
        limiter.stop()
        self.assertFalse(limiter.fill_thread.is_alive())


if __name__ == "__main__":
    unittest.main()
