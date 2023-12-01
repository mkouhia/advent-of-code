"""Advent of Code command line interface runner.

Run functions against downloaded input files.
"""

import datetime
import click

from helpers import get_data

import y23


_functions = {
    2023: y23._day_functions,
}

_today = default = datetime.date.today()


@click.command
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
def cli(year: int, day: int):
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
    solution = day_functions[day](data)
    click.echo(solution)


if __name__ == "__main__":
    cli()
