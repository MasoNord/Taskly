import click


from taskly.bootstrap.fast_api import run_api


@click.command()
@click.option("--reload", is_flag=True)
def run(reload: bool = False) -> None:
    """Simple function that runs a server using gunicorn."""

    if reload:
        run_api(reload=True)
    else:
        run_api(reload=False)

if __name__ == "__main__":
    run()
