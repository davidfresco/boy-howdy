import re
import time
import json
from seleniumwire.utils import decode


def _does_req_body_match_sig(body_text, sig):
    try:
        data = json.loads(body_text)
        try:
            for key in sig.split("."):
                data = data[key]
        except KeyError:
            return False
        return True
    except Exception:
        pass
    return False


def get_target_request_body(driver, url_regex=".*", response_sig=None,
                            timeout=5, poll_interval=1):
    start = time.time()
    while time.time() - start < timeout:
        for req in driver.requests:
            if req.response is None:
                continue
            if re.match(url_regex, req.url) is None:
                continue
            body_text = decode(
                req.response._body,
                req.response.headers.get("content-encoding", "identity"))
            if response_sig is None:
                return body_text
            elif _does_req_body_match_sig(body_text, response_sig):
                return body_text
        time.sleep(poll_interval)
    return None
