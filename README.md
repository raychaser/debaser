# 🎲 🦜 Debaser 🎰 💬

Generate all the conversations, even some entertaining ones!

## Quickstart

Developed with Python 3.11 and Poetry. Should support any Python version >=3.
8.1. Install dependencies with `pip` or `poetry`. You will need to set your
OpenAI API key in the environment variable `OPENAI_API_KEY`.

### Using pip and virtualenv

Create a virtual environment and install dependencies. Then run a quick sanity
check using the `topic` command to make sure things are working properly.

Use the following on Linux or Mac.

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python3 debaser.py topic
```

You can use the `speak` command to create a conversation on a AI-generated topic
with the default bots.

```shell
python3 debaser.py speak
```

Use the following on Windows. Please make sure `python` is actually Python 3. If
unsure, check with `python --version`. 

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set OPENAI_API_KEY=sk-...
python debaser.py topic
```

```shell
python debaser.py speak
```

### Using poetry

Install dependencies with `poetry`. Make sure `poetry` is actually installed.
Then run a quick sanity check to make sure things are working properly.

```shell
poetry install
export OPENAI_API_KEY=sk-...
poetry run python debaser.py topic
```

You can use the `speak` command to create a conversation on a AI-generated topic
with the default bots.

```shell
poetry run python debaser.py speak
```

## Usage

### Basic structure

Debaser is using commands, just like `git`, or `docker`, or Your Mom:

- Command [speak](#speak) generates a conversation
- Command [topic](#topic) generates a topic

### Speak

This is the core of Debaser. It generates a conversation.

```shell
python3 debaser.py speak
```

```shell
poetry run python debaser.py speak
```

The `speak` command uses gpt-3.5-turbo by default, but you can
specify `--model gpt-4` instead.

```shell
python3 debaser.py speak --model gpt-4
```

```shell
poetry run python debaser.py speak --model gpt-4
```

A directory with bots can be specified with `--bots`. The default
is `bots/default`. Put your own bots anywhere you want. A possible place
is `bots/local` which is excluded from source control. Let's say you have 3 bots
of your own, in `bots/local/you_are_awesome/`, `maynard.toml`, `lars.toml`,
and `gene.toml`. The following shows how they can have a conversation.

```shell
python3 debaser.py speak --bots bots/local/you_are_awesome/
```

```shell
poetry run python debaser.py speak --bots bots/local/you_are_awesome/
```

If you want to prime the conversation with a topic, you can specify it
with `--topic`. If no topic is given, the selected model is used to generate
one.

```shell
python3 debaser.py speak --bots bots/local/you_are_awesome/ \
  --topic "Taylor Swift has done more for the rights of artists \
           than all of us dudes together"
```

```shell
poetry run python debaser.py speak --bots bots/local/you_are_awesome/ \
  --topic "Taylor Swift has done more for the rights of artists \
           than all of us dudes together"
```

There are more ways to customize the created conversation.

```shell
python3 debaser.py speak --help
```

```shell
poetry run python debaser.py speak --help
```

### Topic

Command [speak](#speak) either generates a topic for the generated conversation,
or accepts a topic as an argument. If you want to generate a topic on its own,
you can use the `topic` command. The use the `--model` option to specify the
model to use, just like for command [speak](#speak).

```shell
python3 debaser.py topic
```

```shell
poetry run python debaser.py topic
```

There are more ways to customize the created conversation.

```shell
python3 debaser.py topic --help
```

```shell
poetry run python debaser.py topic --help
```

### Help

Help is on the way.

In the meantime, you can use the `--help` flag to get help on any command.
Passing `--help` directly to Debaser shows all global options and lists all
commands.

```shell
python3 debaser.py --help
```

```shell
poetry run python debaser.py --help
```

## Plans

- [ ] Hook up post-commit hook
- [ ] Figure out auto-sizing of history
- [ ] Much tweaking to prompts
- [ ] Flesh out bot format, templatize it
- [ ] Add colored output
- [ ] Add logging options
- [ ] Figure out CLI completion
- [ ] Option to change bot order during conversation
- [ ] Support for non-Open AI bots
