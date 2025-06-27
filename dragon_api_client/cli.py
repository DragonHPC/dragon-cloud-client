import sys
import os
import click
from .dragon_client import DragonAPIClient
import subprocess


client = DragonAPIClient()


@click.group()
def cli():
    """DragonAPI command-line interface."""
    pass


@cli.group()
def jupyter():
    """CLI for managing a jupyter notebook resource."""
    pass


@jupyter.command(name="get")
@click.argument("notebook_id")
def get_notebook(notebook_id):
    """Get and display a notebook kernel by ID.

    Args:
        notebook_id (string): unique identifier for each notebook provided by the api server after creating the notebook
    """
    try:
        response = client.get(notebook_id)
        if response == 404:
            click.echo(f"Notebook {notebook_id} not found.")
        elif response is not None:
            click.echo(f"ID: {response.get('id')}")
            click.echo(f"URL: {response.get('url')}")
    except Exception as e:
        click.echo(f"Error {e.response.status_code}: {e.response.text}", err=True)
        sys.exit(1)


@jupyter.command(name="list")
def list_all_notebooks():
    """List all available notebook kernels."""
    try:
        response = client.list()
        if response == 404:
            click.echo(
                "No notebooks were found. Please make sure you're trying to access a valid deployed dragon cluster."
            )
        elif response is not None:
            click.echo(f"Found {len(response)} notebooks.")
            for notebook in response:
                click.echo(f"ID: {notebook.get('id')} --- URL: {notebook.get('url')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@jupyter.command("create")
@click.option("--jupyter-token", help="Jupyter auth token, if required.")
def create_notebook(jupyter_token):
    """Create a new notebook kernel.

    Args:
        jupyter_token (string): the token for the jupyter kernel login
    """
    try:
        response = client.create(jupyter_token=jupyter_token)
        if response == 404:
            click.echo(
                "The notebook was not created. Please make sure you're trying to access a valid deployed dragon cluster."
            )
        elif response:
            click.echo("Created notebook:")
            click.echo(f"ID: {response.get('id')}")
            click.echo(f"URL: {response.get('url')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@jupyter.command(name="delete")
@click.argument("notebook_id")
def delete_notebook(notebook_id):
    """Delete a notebook by ID.

    Args:
        notebook_id (string): unique identifier for each notebook provided by the api server after creating the notebook
    """
    try:
        response = client.delete(notebook_id)
        if response == 404:
            click.echo(f"Notebook {notebook_id} not found.")
        elif response:
            click.echo(f"Deleted notebook {notebook_id}.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
