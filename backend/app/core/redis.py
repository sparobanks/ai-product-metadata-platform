import os


class RedisSettings:
    def __init__(self) -> None:
        self.url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.enabled = os.getenv('ENABLE_REDIS', 'false').lower() == 'true'


redis_settings = RedisSettings()
