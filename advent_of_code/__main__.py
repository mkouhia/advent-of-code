"""Advent of Code command line interface runner.

Run functions against downloaded input files.
"""

import datetime
import importlib
import pyclbr
import webbrowser
from pathlib import Path

import click

from . import __version__
from .base import Puzzle
from .util import get_data, create_new_template


_today = default = datetime.date.today()


def import_solution(year: int, day: int):
    """Import puzzle class by year and day.

    Raises:
        ModuleNotFoundError: Module for day and year is not found.
        UserWarning: Class that inherits Puzzle is not found in module.
    """
    module_name = f"advent_of_code.y{year - 2000}.day{day:02}"
    day_module = importlib.import_module(module_name)

    for name in pyclbr.readmodule(module_name):
        cls_ = getattr(day_module, name)
        if issubclass(cls_, Puzzle):
            return cls_

    raise UserWarning(f"No puzzle found in {module_name}")


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
    try:
        puzzle_cls = import_solution(year, day)
        data = get_data(year=year, day=day)
        puzzle = puzzle_cls(data)
    except (ModuleNotFoundError, UserWarning) as err:
        click.echo(str(err), err=True)
        return

    solution = puzzle.part1() if part == 1 else puzzle.part2()
    click.echo(solution)


@cli.command(name="list")
def list_puzzles():
    """List all puzzle solutions."""
    module_ = pyclbr.readmodule_ex("advent_of_code")
    mod_path = Path(module_["__path__"][0])
    for child in sorted(
        mod_path.rglob("y??/day??.py"), key=lambda p: p.parent.name + p.name
    ):
        print(child.relative_to(mod_path))


@cli.command
@day_option
@year_option
def new(year: int, day: int):
    """Create puzzle template for today."""
    click.echo(f"Creating new test and development files for {year=}, {day=}:")
    dev, test = create_new_template(year, day)
    click.echo(f"- {dev}")
    click.echo(f"- {test}")


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
