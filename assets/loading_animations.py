import sys
import time
import threading

class Animation:

    def dots_loader(self, stop_event, text = "Reading documents"):
        dots = ""
        while not stop_event.is_set():
            dots = "." if dots == "..." else dots + "."
            sys.stdout.write(f"\r{text}{dots}   ")
            sys.stdout.flush()
            time.sleep(0.5)

    def progress_bar(self, current, total, bar_length=30):
        percent = current / total
        filled = int(bar_length * percent)
        bar = "█" * filled + "-" * (bar_length - filled)
        sys.stdout.write(f"\r[{bar}] {int(percent * 100)}%")
        sys.stdout.flush()



            