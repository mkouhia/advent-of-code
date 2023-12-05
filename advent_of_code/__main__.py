"""Advent of Code command line interface runner.

Run functions against downloaded input files.
"""

import datetime
import webbrowser

import click

from . import __version__
from .helpers import get_data, create_new_template

from .y21 import solutions as solutions_21
from .y23 import solutions as solutions_23


_functions = {
    2021: solutions_21,
    2023: solutions_23,
}

_today = default = datetime.date.today()


year_option = click.option(
    "--year",
    type=int,
    default=_today.year,
    help=f"Event year. Default: this year ({_today.year}).",
)
day_option = click.option(
    "--day",
    type=int,
    default=_today.day,
    help=f"Event day. Default: today (day={_today.day}).",
)


@click.group()
@click.version_option(__version__)
def cli():
    """Advent of Code solution command line interface."""
    return


@cli.command()
@day_option
@year_option
@click.option(
    "--part",
    type=click.IntRange(min=1, max=2),
    default=1,
    help="Puzzle part. Default: 1.",
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

    solution = (
        day_functions[day](data).part1()
        if part == 1
        else day_functions[day](data).part2()
    )

    click.echo(solution)


@cli.command(name="list")
def list_puzzles():
    """List all puzzle solutions."""
    for year, func_dict in _functions.items():
        click.echo(f"# {year}")
        for day, cls_ in func_dict.items():
            click.echo(f"{day:2d} {cls_.__name__}")


@cli.command
@day_option
@year_option
def new(year: int, day: int):
    """Create puzzle template for today."""
    click.echo(f"Creating new test and development files for {year=}, {day=}:")
    dev, test = create_new_template(year, day)
    click.echo(f"- {dev}")
    click.echo(f"- {test}")
    click.echo(f"Remember to add import into {dev.parent /'__init__.py'}")


@cli.command
@day_option
@year_option
def show_input(year: int, day: int):
    """Display input data for the given day."""
    try:
        data = get_data(year=year, day=day)
        click.echo(data)
    except UserWarning as err:
        click.echo(err, err=True)


@cli.command("open")
@day_option
@year_option
def open_webpage(year: int, day: int):
    """Open Advent of Code webpage for given day."""
    url = f"https://adventofcode.com/{year}/day/{day}"
    webbrowser.open(url)


if __name__ == "__main__":
    cli()
