class StreamingQueue:
    def __init__(self):
        self.main_queue = list()
        self.end_flag = False
        self.anchor = "###"
        self.wait_flag = False
        self.generating_card = False

    def __len__(self):
        return len(self.main_queue)

    def append(self, new_text):
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

    def is_empty(self):
        return len(self.main_queue) == 0

    def is_streaming_end(self):
        return self.end_flag and len(self.main_queue) > 0

    def wait(self):
        self.wait_flag = True

    def release(self):
        self.wait_flag = False

    def is_waiting(self):
        return self.wait_flag

    def set_anchor(self, anchor):
        self.anchor = anchor

    def check_anchor_point(self):
        context = "".join(self.main_queue).strip()
        if context.startswith(self.anchor):
            self.flush()
            self.append(context[len(self.anchor) :])
            return "Front"
        if context.endswith(self.anchor):
            self.flush()
            self.append(context[: len(self.anchor)])
            return "Back"
        return False

    def flush(self):
        for _ in range(len(self.main_queue)):
            self.main_queue.pop(0)
