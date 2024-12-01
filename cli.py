from typing import Callable, List, Optional, Tuple

import typer


def create_day_cli(
    day_number: int,
    input_parser: Callable[[str], Tuple[List[int], List[int]]],
    part1: Callable[[List[int], List[int]], int],
    part2: Callable[[List[int], List[int]], int],
) -> typer.Typer:
    """
    Creates a Typer app for a specific day with a 'run' command.

    Args:
        day_number (int): The day number.
        input_parser (Callable): Function to parse the input file.
        part1 (Callable): Function to execute Part 1.
        part2 (Callable): Function to execute Part 2.

    Returns:
        typer.Typer: The Typer app instance.
    """
    app = typer.Typer(name=f"Day {day_number}")

    @app.command()
    def run(
        part: Optional[int] = typer.Option(
            None,
            "--part",
            "-p",
            help="Part to run (1 or 2). Defaults to running both.",
        ),
        file: Optional[str] = typer.Option(
            None,
            "--file",
            "-f",
            help=f"Path to input file. Defaults to 'data/day{day_number}.txt'.",
            metavar="FILE",
        ),
    ):
        """
        Run one (or both) parts of that day's challenge.
        """
        if file is None:
            file = f"data/day{day_number}.txt"

        try:
            parsed_input = input_parser(file)
        except FileNotFoundError:
            typer.echo(f"Error: The file '{file}' was not found.", err=True)
            raise typer.Exit(code=1)
        except ValueError as ve:
            typer.echo(f"Error parsing input: {ve}", err=True)
            raise typer.Exit(code=1)

        if part is not None:
            if part not in (1, 2):
                typer.echo("Invalid part number. Choose 1 or 2.", err=True)
                raise typer.Exit(code=1)
            try:
                if part == 1:
                    result = part1(*parsed_input)
                    typer.echo(f"Day {day_number} Part 1 result = {result}")
                elif part == 2:
                    result = part2(*parsed_input)
                    typer.echo(f"Day {day_number} Part 2 result = {result}")
            except Exception as e:
                typer.echo(f"Error executing Part {part}: {e}", err=True)
                raise typer.Exit(code=1)
        else:
            try:
                result1 = part1(*parsed_input)
                typer.echo(f"Day {day_number} Part 1 result = {result1}")
            except Exception as e:
                typer.echo(f"Error executing Part 1: {e}", err=True)
                raise typer.Exit(code=1)

            try:
                result2 = part2(*parsed_input)
                typer.echo(f"Day {day_number} Part 2 result = {result2}")
            except Exception as e:
                typer.echo(f"Error executing Part 2: {e}", err=True)
                raise typer.Exit(code=1)

    return app
