"""Advent of Code command line interface runner.

Run functions against downloaded input files.
"""

import datetime
import click

from . import __version__
from .helpers import get_data
from .base import Puzzle

from .y23 import solutions as solutions_23


_functions = {
    2023: solutions_23,
}

_today = default = datetime.date.today()


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
@click.option(
    "--day",
    type=int,
    default=_today.day,
    help=f"Event day. Default: today (day={_today.day}).",
)
@click.option(
    "--year",
    type=int,
    default=_today.year,
    help=f"Event year. Default: this year ({_today.year}).",
)
@click.option(
    "--part",
    type=click.IntRange(min=1, max=2),
    default=1,
    help=f"Puzzle part. Default: 1.",
)
def run(year: int, day: int, part: int):
    """Run developed functions on Advent of Code data."""
    if year not in _functions:
        click.echo(f"Year {year}: not implemented", err=True)
        return

    day_functions = _functions[year]
    if day not in day_functions:
        click.echo(f"{year} day {day}: solution not implemented.", err=True)
        return

    try:
        data = get_data(year=year, day=day)
    except UserWarning as err:
        click.echo(err, err=True)

    match part:
        case 1:
            solution = day_functions[day].part1(data)
        case 2:
            solution = day_functions[day].part2(data)
        case _:
            click.echo("")

    click.echo(solution)


@cli.command
def list():
    """List all puzzle solutions."""
    for year in _functions:
        click.echo(f"# {year}")
        for day, cls_ in _functions[year].items():
            click.echo(f"{day:2d} {cls_.__name__}")


if __name__ == "__main__":
    cli()
