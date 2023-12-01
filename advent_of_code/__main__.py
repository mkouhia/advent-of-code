import datetime
import click

from helpers import get_data

import y23


_functions = {
    2023: y23._day_functions,
}

_today = default=datetime.date.today()

@click.command
@click.option("--day", type=int, default=_today.day)
@click.option("--year", type=int, default=_today.year)
@click.option("--session-id")
def cli(year, day, session_id):
    if year not in _functions:
        raise NotImplementedError(f"Year {year}: not implemented")
    
    day_functions = _functions[year]
    if day not in day_functions:
        raise NotImplementedError(f"{year} day {day}: solution not implemented.")

    data = get_data(day=day, session_id=session_id)
    solution = day_functions[day](data)
    print(solution)


if __name__ == "__main__":
    cli()
