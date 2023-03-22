FROM python:3.9-slim-bullseye

RUN pip install discord discord.py \
        openai python-dotenv sqlalchemy

WORKDIR /gpt-discord-bot

CMD ["python", "main.py"]
