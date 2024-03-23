import os

class BlindrConfig:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or os.getenv("SDK_BASE_URL")
        self.api_key = api_key or os.getenv("SDK_API_KEY")
        