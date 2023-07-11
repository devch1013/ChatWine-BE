import time

def streaming(text):
    for i in range(10):
        # print(f"hello{i}")
        yield f"hello{i}"
        time.sleep(0.5)
    yield text