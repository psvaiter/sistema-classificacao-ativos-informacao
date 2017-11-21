"""A basic (single function) API written using hug"""

import hug


@hug.get('/happy_birthday')
def happy_birthday(name, age: hug.types.number = 1):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals())


@hug.get('/greet/{event}')
def greet(event: str):
    """Greets appropriately
    (from http://blog.ketchum.com/how-to-write-10-common-holiday-greetings/)"""
    greetings = "Happy"
    if event == "Christmas":
        greetings = "Merry"
    if event == "Kwanzaa":
        greetings = "Joyous"
    if event == "wishes":
        greetings = "Warm"

    return "{greetings} {event}!".format(**locals())


@hug.default_output_format()
def my_output_formatter(data):
    return "STRING:{0}".format(data)


@hug.get(output=hug.output_format.json)
def hello():
    return {'hello': 'world'}
