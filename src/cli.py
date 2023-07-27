import typer


cli = typer.Typer()


@cli.callback()
def callback():
    pass


@cli.command()
def fetch_data():
    import asyncio

    from app.cli.fetch_data import fetch_data

    asyncio.run(fetch_data())


if __name__ == "__main__":
    cli()
