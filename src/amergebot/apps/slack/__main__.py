"""A Slack bot that interacts with users and processes their queries.

This module contains the main functionality of the Slack bot. It listens for mentions of the bot in messages,
processes the text of the message, and sends a response. It also handles reactions added to messages and
saves them as feedback. The bot supports both English and Japanese languages.

The bot uses the Slack Bolt framework for handling events and the langdetect library for language detection.
It also communicates with an external API for processing queries and storing chat history and feedback.

"""

import argparse
import asyncio
import logging
from typing import Callable

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_sdk.web import SlackResponse

from amergebot.api.client import AsyncAPIClient
from amergebot.apps.slack.config import SlackAppEnConfig, SlackAppJaConfig
from amergebot.apps.slack.formatter import MrkdwnFormatter

# from amergebot.apps.utils import format_response


parser = argparse.ArgumentParser()

parser.add_argument(
    "-l",
    "--language",
    default="en",
    help="Language of the bot",
    type=str,
    choices=["en", "ja"],
)

args = parser.parse_args()

if args.language == "ja":
    config = SlackAppJaConfig()
else:
    config = SlackAppEnConfig()


app = AsyncApp(token=config.SLACK_BOT_TOKEN)
api_client = AsyncAPIClient(url=config.WANDBOT_API_URL)


async def send_message(say: Callable, message: str, thread: str = None) -> SlackResponse:
    message = MrkdwnFormatter()(message)
    if thread is not None:
        return await say(text=message, thread_ts=thread)
    else:
        return await say(text=message)


@app.event("app_mention")
async def app_mention_handler(event: dict, say: Callable, logger: logging.Logger) -> None:
    """Handles app mention in a message. Available handler args are: slack_bolt.kwargs_injection.async_args"""
    try:
        # query = event.get("text")
        user = event.get("user")

        # Post message to already existing thread (id = thread_ts) or start new thread (id = ts)
        thread_id = event.get("thread_ts", None) or event.get("ts", None)

        # chat_history = await api_client.get_chat_history(application=config.APPLICATION, thread_id=thread_id)

        if not event.get("thread_ts", None):
            await send_message(
                say=say,
                message=config.INTRO_MESSAGE.format(user=user),
                thread=thread_id,
            )

        # # process the query through the api
        # api_response = await api_client.query(
        #     question=query,
        #     chat_history=chat_history,
        #     language=config.bot_language,
        #     application=config.APPLICATION,
        # )
        # response = format_response(
        #     config,
        #     None,
        #     config.OUTRO_MESSAGE,
        # )

        # send the response
        sent_message = await send_message(
            say=say, message="I don't have anything for you now.", thread=thread_id
        )

        await app.client.reactions_add(
            channel=event["channel"],
            timestamp=sent_message["ts"],
            name="thumbsup",
            token=config.SLACK_BOT_TOKEN,
        )
        await app.client.reactions_add(
            channel=event["channel"],
            timestamp=sent_message["ts"],
            name="thumbsdown",
            token=config.SLACK_BOT_TOKEN,
        )

        #  save the question answer to the database
        # await api_client.create_question_answer(
        #     thread_id=thread_id,
        #     question_answer_id=sent_message["ts"],
        #     language=config.bot_language,
        #     **api_response.model_dump(),
        # )

    except Exception as e:
        logger.error(f"Error posting message: {e}")


def parse_reaction_into_rating(reaction: str) -> int:
    if reaction == "+1":
        return 1
    elif reaction == "-1":
        return -1
    else:
        return 0


@app.event("reaction_added")
async def reaction_added_handler(event: dict) -> None:
    """Handles the event when a reaction is added to a message"""
    message_ts = event["item"]["ts"]
    rating = parse_reaction_into_rating(event["reaction"])

    await api_client.create_feedback(
        feedback_id=event["event_ts"],
        question_answer_id=message_ts,
        rating=rating,
    )


async def main():
    handler = AsyncSocketModeHandler(app, config.SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
