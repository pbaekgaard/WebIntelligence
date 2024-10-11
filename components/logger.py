import time

class Logger:
    def __init__(self):
        self.timers = {}

    def time(self, label="LOGGER"):
        self.timers[label] = time.time()

    def endtime(self, label="LOGGER"):
        if label in self.timers:
            elapsed = time.time() - self.timers[label]
            print(f"[{label}] -> {elapsed:.4f} seconds")
            del self.timers[label]
        else:
            print(f"Timer '{label}' does not exist.")
