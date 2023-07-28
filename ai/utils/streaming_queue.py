class StreamingQueue:
    def __init__(self):
        self.main_queue = list()
        self.end_flag = False
        self.anchor = None

    def push(self, new_text):
        self.main_queue.append(new_text)

    def get(self):
        """
        return and delete first object of queue
        """
        return self.main_queue.pop(0)

    def end_job(self):
        self.end_flag = True

    def is_end(self):
        return self.end_flag and len(self.main_queue) == 0

    def is_streaming_end(self):
        return self.end_flag and len(self.main_queue) > 0

    def set_anchor(self, anchor):
        self.anchor = anchor
