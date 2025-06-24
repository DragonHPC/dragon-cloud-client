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


@cli.command(name="launch")
@click.argument("instance_name")
@click.option("--nnodes")
def launch_dragon_chart(instance_name, nnodes):
    """Install a helm chart for deploying a dragon cluster.
    Launch a subprocess that executes the helm install command.

    Args:
        instance_name (string): the chart's release name
        nnodes (int): number of backend nodes for the dragon chart

    Raises:
        click.Abort: if the subprocess returns an error code
    """
    domain_name = os.getenv("DOMAIN_NAME")

    cmd = [
        "helm",
        "install",
        instance_name,
        "../gpu-cloud-services",
        "--set",
        f"backend.nnodes={nnodes}",
        "--set",
        f"domain.name={domain_name}",
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        click.echo(f"Dragon launch failed with exit code {e.returncode}", err=True)
        raise click.Abort()

    cluster_name = domain_name.split(".", 1)[0]
    click.echo("\nA Dragon instance just deployed on the HPE GPU Cloud Service.\n")
    click.echo(f"Dragon instance name: {instance_name}")
    click.echo(f"Cluster name: {cluster_name}")
    click.echo(f"Number of nodes: {nnodes}")
    click.echo(f"DNS Name: {domain_name}\n")


@cli.command(name="teardown")
@click.argument("instance_name")
def uninstall_dragon_chart(instance_name):
    """Delete the dragon chart and clean everything up, by
    executing helm uninstall. Launch a subprocess that executes
    the helm uninstall command.

    Args:
        instance_name (string): the chart's release name

    Raises:
        click.Abort: if the subprocess returns an error code
    """
    cmd = ["helm", "uninstall", instance_name]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        click.echo(
            f"Uninstall of Dragon chart failed with exit code {e.returncode}", err=True
        )
        raise click.Abort()

    click.echo(
        f"Dragon instance '{instance_name}' is deleted and cleaned up successfully."
    )


if __name__ == "__main__":
    cli()
