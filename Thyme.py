import threading
import time
class Timer:
    def __init__(self):
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0

        # Initialize the timer thread
        self.timer_thread = threading.Thread(target=self.timer_function)

        # Start the timer thread
        self.timer_thread.start()

    def start_timer(self):
        if not self.timer_running:#
            self.start_time = time.time()  # Update start time only if the timer is not running
            print("Timer started")
            self.timer_running = True

    def stop_timer(self):
        if self.timer_running: # Stop the timer only if it is running
            self.timer_running = False
            self.elapsed_time = 0 # Reset the elapsed time
            print("Timer stopped")

    def timer_function(self):
        while True:  # Run indefinitely
            if self.timer_running:
                self.elapsed_time = int(time.time() - self.start_time)
            time.sleep(1)  # Update the timer every second