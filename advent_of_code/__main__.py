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
def run(year: int, day: int):
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

    solution = day_functions[day].solve(data)
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
