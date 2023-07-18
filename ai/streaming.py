import time

def streaming(text):
    for i in range(10):
        yield f"hello{i} "
        time.sleep(0.5)
    yield text