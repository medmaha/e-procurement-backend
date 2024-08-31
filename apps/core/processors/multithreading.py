import threading
import multiprocessing


class MultiProcessing(multiprocessing.Process):
    def __init__(self, target, args=(), auto_run=True):
        self.daemon = True  # Set as daemon thread to exit when the main program exits
        self.target = target
        self.args = args
        if auto_run:
            self.run()

    def run(self):
        # Check if multithreading is possible
        if threading.active_count() > 1:
            super().run()  # Execute in a separate thread
        else:
            self.target(*self.args)  # Execute in the main thread


class MultiThreading(threading.Thread):
    def __init__(self, target, args=(), auto_run=True):
        super().__init__(target=target, args=args)
        self.daemon = True  # Set as daemon thread to exit when the main program exits
        self.target = target
        self.args = args

        if auto_run:
            self.start()

    def run(self):
        # Check if multithreading is possible
        try:
            if threading.active_count() > 1:
                super().run()  # Execute in a separate thread
            else:
                self.target(*self.args)  # Execute in the main thread
        except Exception as e:
            print("ERROR!", e)
