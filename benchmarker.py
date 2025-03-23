import psutil
import os
from time import perf_counter
from functools import wraps


class MemoryTracker:
    def __init__(self, name):
        self.changes = {}
        self.total_memories = {}
        self.keys = []
        self.name = name

        self.total_time = 0
        self.times = {}

    def start(self, name):
        self.curr = name
        self.process = psutil.Process(os.getpid())
        self.start_memory = self.process.memory_info().rss / (1024 * 1024)  # in MB
        self.start_time = perf_counter()

    def end(self):
        time_taken = perf_counter() - self.start_time

        end_memory = self.process.memory_info().rss / (1024 * 1024)  # in MB
        name = self.curr
        memory_used = end_memory - self.start_memory
        self.total_memories[name] = end_memory
        self.changes[name] = memory_used
        self.keys.append(name)
        self.times[name] = time_taken
        self.total_time += time_taken

    def display_results(self):
        print(f"\n--- Performance Metrics for {self.name} ---")
        print(
            f"{'Section':<20} {'Memory Change (MB)':<20} {'Total Memory (MB)':<20} {'Time (s)':<10}"
        )
        print("-" * 70)

        for key in self.keys:
            print(
                f"{key:<20} {self.changes.get(key, 0):<20.2f} {self.total_memories.get(key, 0):<20.2f} {self.times[key]:<10.4f}"
            )

        print(f"\nPeak memory usage: {max(self.total_memories.values()):.2f} MB")
        print(f"\nTotal time taken: {sum(self.times.values()):.2f}s")

        print("-" * 70)
