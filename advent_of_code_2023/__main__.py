import click

from helpers import get_data
from day01 import calibrate_document


__day_functions = {
    1: calibrate_document,
}


@click.command
@click.option("--day", type=int)
@click.option("--session-id")
def cli(day, session_id):
    if day not in __day_functions:
        raise NotImplemented("Day %s: solution not implemented.")
    data = get_data(day=day, session_id=session_id)
    solution = __day_functions[day](data)
    print(solution)


if __name__ == "__main__":
    cli()
