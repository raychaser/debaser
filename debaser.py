import logging
import os
import random
from logging.handlers import WatchedFileHandler

import tomli as tomli
import typer as typer
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel

# Set up logging
handler = logging.handlers.WatchedFileHandler(
    os.environ.get('LOGFILE', "debaser.log"))
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s')
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get('LOGLEVEL', 'DEBUG'))
root.addHandler(handler)

#
# Constants
#

SUPPORTED_MODELS = ['gpt-3.5-turbo', 'gpt-4']
DEFAULT_TOPIC_PROMPT = "You are a good and creative at suggesting highly " \
                       "interesting and potentially controversial topic for " \
                       "discussion, debate, and the exchange of different " \
                       "views."
DEFAULT_TOPIC_HINT = "Suggest an interesting topic of conversation."


#
# Classes
#

class History:
    def __init__(self, max):
        self.max = max
        self.queue = []

    def add(self, item):
        self.queue.append(item)
        if len(self.queue) > self.max:
            self.queue.pop(0)

    def get(self):
        return self.queue

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)


class BotDescription(BaseModel):
    name: str
    temperature: float = "1.0"
    prompt: str


class Bot:
    def __init__(self, model_name: str, bot_description: BotDescription):
        self.model_name = model_name
        self.description = bot_description
        self.system_message = SystemMessage(content=self.description.prompt)
        self.llm = ChatOpenAI(temperature=self.description.temperature,
                              model_name=model_name)

    def generate(self, prompts: list[str]):
        actual_prompts: list[SystemMessage | HumanMessage] = \
            [self.system_message]
        for item in prompts:
            actual_prompts.append(HumanMessage(content=item))
        return self.llm(actual_prompts)


#
# Helper Functions
#

def banner(model):
    print("This is DEBASER, made by raychaser. Please enjoy responsibly!")
    print("Model: {}".format(model))


def validate_model_name(model_name: str) -> None:
    if model_name not in SUPPORTED_MODELS:
        raise typer.BadParameter(
            "model_name must be one of: {}".format(SUPPORTED_MODELS))


def generate_topic(model_name: str, topic_prompt: str, topic_hint: str) -> str:
    bot_description = BotDescription(name="Topicbot", prompt=topic_prompt,
                                     temperature=1.0)
    topic_bot = Bot(model_name, bot_description)
    return topic_bot.generate([topic_hint]).content


#
# CLI Commands
#

app = typer.Typer()


@app.command()
def speak(model: str = 'gpt-3.5-turbo', bots: str = 'bots/default',
          topic: str = None, topic_prompt: str = DEFAULT_TOPIC_PROMPT,
          topic_hint: str = DEFAULT_TOPIC_HINT, rounds: int = 3,
          history_multiplier: int = 2, history: int = -1) -> None:
    """
    Create a conversation between bots.
    """

    validate_model_name(model)

    if not os.path.exists(bots):
        raise typer.BadParameter("Bot path does not exist: {}".format(bots))
    if not os.path.isdir(bots):
        raise typer.BadParameter("Bot path is not a directory: {}".format(bots))
    actual_bots = []
    for bot_filename in os.listdir(bots):
        if bot_filename.endswith(".toml"):
            bot_path = os.path.join(bots, bot_filename)
            with open(bot_path, "rb") as bot_file:
                bot_data = tomli.load(bot_file)
                bot_description = BotDescription(**bot_data)
                bot = Bot(model, bot_description)
                actual_bots.append(bot)
    if len(actual_bots) < 1:
        raise typer.BadParameter("No bots found in directory: {}".format(bots))
    random.shuffle(actual_bots)

    banner(model)

    actual_topic = topic
    if actual_topic is None:
        actual_topic = generate_topic(model, topic_prompt, topic_hint)
    print("Topic: {}".format(actual_topic))

    history_length = history
    if history < 0:
        history_length = len(actual_bots) * history_multiplier
    bot_names = [bot.description.name for bot in actual_bots]
    print("Bots: {}, history: {}".format(bot_names, history_length))
    print()
    actual_history = History(history_length)
    actual_history.add(actual_topic)

    for i in range(rounds):
        for bot in actual_bots:
            response = bot.generate(actual_history.get()).content
            # TODO: token counting for automatic history adjustment
            # response['usage']['total_tokens']
            actual_history.add(response)
            print(response)
            print()


@app.command()
def topic(model: str = 'gpt-3.5-turbo',
          topic_prompt: str = DEFAULT_TOPIC_PROMPT,
          topic_hint: str = DEFAULT_TOPIC_HINT) -> None:
    """
    Create a topic for inspiration and later use.
    """

    validate_model_name(model)

    banner(model)

    topic = generate_topic(model, topic_prompt, topic_hint)
    print("Topic: {}".format(topic))


#
# Main
#

# @app.callback()
# def main(ctx: typer.Context, verbose: bool = False):
#     if verbose:
#         print("Will write verbose output")


if __name__ == '__main__':
    app()
