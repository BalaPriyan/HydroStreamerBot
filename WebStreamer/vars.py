# This file is a part of FileStreamBot
from urllib import request
from typing import List, Optional, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    MULTI_CLIENT: bool = False
    API_ID: int = Field(..., description="API ID from my.telegram.org")
    API_HASH: str = Field(..., description="API HASH from my.telegram.org")
    BOT_TOKEN: str = Field(..., description="Bot Token from @BotFather")
    RUN_MODE: str = Field(default="ALL")
    REDIS_URL: str = Field(default="redis://redis:6379")
    SLEEP_THRESHOLD: int = Field(default=60)
    WORKERS: int = Field(default=6)
    BIN_CHANNEL: int = Field(..., description="Channel ID for multi-client")
    PORT: int = Field(default=8080)
    WEB_SERVER_BIND_ADDRESS: str = Field(default="0.0.0.0")
    PING_INTERVAL: int = Field(default=1200)
    HAS_SSL: bool = Field(default=False)
    NO_PORT: bool = Field(default=False)
    FQDN: str = Field(default="")
    URL: str = Field(default="")
    DATABASE_URL: str = Field(...)
    UPDATES_CHANNEL: str = Field(default="Telegram")
    OWNER_ID: int = Field(...)
    SESSION_NAME: str = Field(default="hydroBot")
    FORCE_UPDATES_CHANNEL: bool = Field(default=False)
    ALLOWED_USERS: List[str] = Field(default_factory=list)
    KEEP_ALIVE: bool = Field(default=False)
    IMAGE_FILEID: str = Field(default="https://cdn.jsdelivr.net/gh/fyaz05/Resources@main/HydroStreamerBot/My%20Files.jpeg")
    TOS: Optional[str] = Field(default=None)
    MODE: str = Field(default="primary")

    _live_config: dict = {}

    def __getattribute__(self, name: str) -> Any:
        try:
            live = object.__getattribute__(self, "_live_config")
            if live and name in live:
                return live[name]
        except AttributeError:
            pass
        return object.__getattribute__(self, name)

    @property
    def BIND_ADDRESS(self) -> str:
        return self.WEB_SERVER_BIND_ADDRESS

    @property
    def SECONDARY(self) -> bool:
        return self.MODE.lower() == "secondary"

    LINK_LIMIT: Optional[int] = Field(default=None)

    @field_validator("ALLOWED_USERS", mode="before")
    @classmethod
    def parse_allowed_users(cls, v: Any):
        if isinstance(v, str):
            return [x.strip("@ ") for x in v.split(",") if x.strip("@ ")]
        return v or []

    def model_post_init(self, __context: Any):
        # Resolve FQDN Fallback
        if not self.FQDN:
            self.FQDN = self.BIND_ADDRESS

        # Resolve URL
        scheme = "https" if self.HAS_SSL else "http"
        port_str = "" if self.NO_PORT else f":{self.PORT}"
        self.URL = f"{scheme}://{self.FQDN}{port_str}/"

        # Resolve TOS
        if self.TOS:
            try:
                resp = request.urlopen(self.TOS)
                self.TOS = resp.read().decode('utf-8').strip()
            except Exception:
                pass

Var = Settings()
