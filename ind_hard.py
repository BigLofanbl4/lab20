# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
from datetime import datetime

import click
from jsonschema import validate
from jsonschema.exceptions import ValidationError


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
@click.argument("surname")
@click.argument("name")
@click.argument("zodiac")
@click.argument("birthday")
def add(filename, surname, name, zodiac, birthday):
    if os.path.exists(filename):
        people = load_people(filename)
    else:
        people = []
    people = add_person(people, surname, name, zodiac, birthday)
    people.sort(
        key=lambda x: datetime.strptime(".".join(x["birthday"]), "%d.%m.%Y")
    )
    save_people(filename, people)


@cli.command()
@click.argument("filename")
def display(filename):
    people = load_people(filename)
    display_people(people)


@cli.command()
@click.argument("filename")
@click.argument("surname")
def select(filename, surname):
    people = load_people(filename)
    select_people(surname, people)


def validation(instance):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "surname": {"type": "string"},
                "name": {"type": "string"},
                "zodiac": {"type": "string"},
                "birthday": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minitems": 3,
                },
            },
            "required": ["surname", "name", "birthday"],
        },
    }
    try:
        validate(instance, schema=schema)
        return True
    except ValidationError as err:
        print(err.message)
        return False


def load_people(file_name):
    with open(file_name, "r") as f:
        people = json.load(f)

    if validation(people):
        return people


def save_people(file_name, people_list):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(people_list, f, ensure_ascii=False, indent=4)


def add_person(people, surname, name, zodiac, birthday):
    people.append(
        {
            "surname": surname,
            "name": name,
            "zodiac": zodiac,
            "birthday": birthday.split("."),
        }
    )
    return people


def display_people(people):
    """
    Отобразить список людей.
    """
    if people:
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 30, "-" * 20, "-" * 20
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^30} | {:^20} | {:^20} |".format(
                "№", "Фамилия", "Имя", "Знак зодиака", "Дата рождения"
            )
        )
        print(line)

        for idx, person in enumerate(people, 1):
            print(
                "| {:>4} | {:<30} | {:<30} | {:<20} | {:>20} |".format(
                    idx,
                    person.get("surname", ""),
                    person.get("name", ""),
                    person.get("zodiac", ""),
                    ".".join(person.get("birthday", "")),
                )
            )
        print(line)
    else:
        print("Список пуст")


def select_people(surname, people):
    """
    Выбрать людей с заданной фамилией.
    """
    result = []
    for i in people:
        if i.get("surname", "") == surname:
            result.append(i)
    return result


if __name__ == "__main__":
    cli()
