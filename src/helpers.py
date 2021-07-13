from texts import (
    bot_texts,
)


def get_relevant_message(day):

    if day not in [4, 5]:
        message = bot_texts['week_sun']
    else:
        message = bot_texts['fri_sut']

    return message



