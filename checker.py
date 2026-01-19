import requests
import time


def check_website(url, timeout=10):
    try:
        start = time.time()
        r = requests.get(url, timeout=timeout)
        end = time.time()

        response_time = round(end - start, 2)

        if r.status_code < 400:
            return "ok", response_time
        else:
            return "down", response_time

    except Exception:
        return "down", None
