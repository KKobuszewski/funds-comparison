from pathlib import Path


class APIError(Exception):
    pass


class CreditScoringModelNotFoundError(APIError):
    def __init__(self, path: Path):
        self._msg = f"Unable to find Credit Scoring Model in {path} location."
        super().__init__(self._msg)


class RedisConnectionError(APIError):
    def __init__(self, host: str, port: str):
        self._msg = f"Unable to connect to Redis database on {host=}, {port=}."
        super().__init__(self._msg)


class PostgresConnectionError(APIError):
    def __init__(self, database: str, user: str, host: str, port: str):
        self._msg = f"Unable to connect to Postgres database on {database=}, {user=}, {host=}, {port=}."
        super().__init__(self._msg)


class RedisConnectionNotAliveError(APIError):
    def __init__(self, host: str, port: str):
        self._msg = f"Connection to Redis is not alive on {host=}, {port=}."
        super().__init__(self._msg)
