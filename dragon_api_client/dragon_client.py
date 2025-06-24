from .http import (
    list_notebooks,
    get_notebook,
    create_notebook,
    delete_notebook,
)
from requests.exceptions import HTTPError


class DragonAPIClient:
    """Dragon API client for submitting requests to the kubernetes dragon cluster server
    for managing Jupyter notebooks.
    """

    def list(self) -> list | str:
        """List all available notebooks.

        Returns:
            list | str: a list of notebooks; each notebook is a dict with keys "id" and "url" or an error text or the error text
        """
        try:
            return list_notebooks()
        except HTTPError as e:
            return self._http_error_handler(e)

    def get(self, notebook_id: str) -> dict | str:
        """Get a single notebook by ID.

        Args:
            notebook_id (str): unique identifier for each notebook provided by the api server after creating the notebook

        Returns:
            dict | str: the requested notebook as a dict object with keys "id" and "url" or the error text
        """
        try:
            return get_notebook(notebook_id)
        except HTTPError as e:
            return self._http_error_handler(e)

    def create(self, **options) -> dict | str:
        """Create a new notebook.

        Returns:
            dict | str: the newly created notebook object with keys "id" and "url" or the error text
        """
        jupyter_token = options.pop("jupyter_token", None)
        try:
            return create_notebook(options or {}, jupyter_token)
        except HTTPError as e:
            return self._http_error_handler(e)

    def delete(self, notebook_id: str) -> dict | str:
        """Delete a jupyter notebook by ID.

        Args:
            notebook_id (str): unique identifier for each notebook provided by the api server after creating the notebook

        Returns:
            dict | str: the deleted notebook object with keys "id" and "url" or the error text
        """
        try:
            return delete_notebook(notebook_id)
        except HTTPError as e:
            return self._http_error_handler(e)

    def _http_error_handler(self, e: HTTPError):
        code = e.response.status_code
        text = e.response.text
        print(f"Error {code}: {text}", flush=True)
