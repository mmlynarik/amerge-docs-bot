from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

INTRO_MESSAGE = (
    "Hi <@{user}>:\n\n"
    "The Amerge Docs Bot is currently not providing any useful info.\n\n"
    "But that will change soon..."
)

OUTRO_MESSAGE = (
    "🤖 If you still need help please try re-phrase your question, \n\n"
    " Was this response helpful? Please react below to let us know"
)

ERROR_MESSAGE = (
    "Oops!, Something went wrong. Please retry again in some time"
)

FALLBACK_WARNING_MESSAGE = (
    "**Warning: Falling back to {model}**, These results may nor be as good as "
    "**gpt-4**\n\n"
)


class SlackAppConfig(BaseSettings):
    APPLICATION: str = Field("Slack_EN")
    SLACK_APP_TOKEN: str = Field(..., validation_alias="SLACK_APP_TOKEN")
    SLACK_BOT_TOKEN: str = Field(..., validation_alias="SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET: str = Field(
        ..., validation_alias="SLACK_SIGNING_SECRET"
    )
    INTRO_MESSAGE: str = Field(INTRO_MESSAGE)
    OUTRO_MESSAGE: str = Field(OUTRO_MESSAGE)
    ERROR_MESSAGE: str = Field(ERROR_MESSAGE)
    WARNING_MESSAGE: str = Field(FALLBACK_WARNING_MESSAGE)
    WANDBOT_API_URL: AnyHttpUrl = Field(..., validation_alias="WANDBOT_API_URL")
    include_sources: bool = True
    bot_language: str = "en"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
