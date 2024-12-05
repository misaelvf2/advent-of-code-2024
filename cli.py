from typing import Any, Callable, Optional

import typer


def create_day_cli(
    day_number: int,
    input_parser: Callable[..., Any],
    part1: Callable[..., Any],
    part2: Callable[..., Any],
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

        def execute_part(part_func: Callable[..., Any], part_num: int):
            try:
                # Determine how to call the part function
                if isinstance(parsed_input, (list, tuple)):
                    result = part_func(*parsed_input)
                elif isinstance(parsed_input, dict):
                    result = part_func(**parsed_input)
                else:
                    result = part_func(parsed_input)
                typer.echo(f"Day {day_number} Part {part_num} result = {result}")
            except TypeError as te:
                typer.echo(
                    f"TypeError executing Part {part_num}: {te}. "
                    f"Check the number and type of arguments.",
                    err=True,
                )
                raise typer.Exit(code=1)
            except Exception as e:
                typer.echo(f"Error executing Part {part_num}: {e}", err=True)
                raise typer.Exit(code=1)

        if part is not None:
            if part not in (1, 2):
                typer.echo("Invalid part number. Choose 1 or 2.", err=True)
                raise typer.Exit(code=1)
            if part == 1:
                execute_part(part1, 1)
            elif part == 2:
                execute_part(part2, 2)
        else:
            execute_part(part1, 1)
            execute_part(part2, 2)

    return app
