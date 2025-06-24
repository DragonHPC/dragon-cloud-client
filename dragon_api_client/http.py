import requests
from requests.exceptions import HTTPError
from .config import settings


def _request(method: str, path: str, **kwargs) -> dict | list | str:
    """
    Send an HTTP request to BASE_URL + path.
    Raises on non-2xx. Returns parsed JSON.
    """
    url = settings.base_url.rstrip("/") + path
    headers = {"Content-Type": "application/json"}
    # if settings.token:
    #     headers["Authorization"] = f"Bearer {settings.token}"

    # Ingress basic authentication credentials
    auth = (settings.username, settings.psw)
    try:
        resp = requests.request(
            method, url, headers=headers, timeout=settings.timeout, auth=auth, **kwargs
        )

        resp.raise_for_status()
        text = resp.text.strip()

        # if not text:
        #     # truly empty response
        #     return None

        return resp.json()
    except HTTPError as err:
        if err.response.status_code == 401:
            print(
                "Authorization Required. Please make sure you have set up the credentials properly.",
                flush=True,
            )
        elif err.response.status_code == 503:
            print(
                "Ingress authentication is not set up properly. Please make sure that the Ingress Secret is created.",
                flush=True,
            )
        elif err.response.status_code == 404:
            return err.response.status_code
        else:
            return err
    except ValueError:
        # not valid JSON, return raw text
        return text


def list_notebooks() -> list | str:
    """List all available notebook kernels.

    Returns:
        list | str: a list of notebooks; each notebook is a dict with keys "id" and "url" or the error text
    """
    return _request("GET", "/api/jupyter/")


def get_notebook(notebook_id: str) -> dict | str:
    """Get a single notebook by ID.

    Args:
        notebook_id (str): unique identifier for each notebook provided by the api server after creating the notebook

    Returns:
        dict | str: the requested notebook as a dict object with keys "id" and "url" or the error text
    """
    return _request("GET", f"/api/jupyter/{notebook_id}")


def create_notebook(options: dict = None, jupyter_token: str = None) -> dict | str:
    """POST /api/jupyter/ to create a new Jupyter kernel.

    Args:
        options (dict, optional): the JSON body for the Flask view. Defaults to None.
        jupyter_token (str, optional): jupyter token. Defaults to None.

    Returns:
        dict | str: the newly created notebook object with keys "id" and "url" or the error text
    """
    body = options or {}
    params = {"token": jupyter_token} if jupyter_token else None

    return _request("POST", "/api/jupyter/", params=params, json=body)


def delete_notebook(notebook_id: str) -> dict | str:
    """Delete a jupyter notebook by ID.

    Args:
        notebook_id (str): unique identifier for each notebook provided by the api server after creating the notebook

    Returns:
        dict | str: the deleted notebook as a dict object with keys "id" and "url" or the error text
    """
    return _request("DELETE", f"/api/jupyter/{notebook_id}")
