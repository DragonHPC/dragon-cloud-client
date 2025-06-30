import os
import sys
from pathlib import Path
import yaml
from urllib.parse import urljoin


class ClusterSettings:

    def __init__(self):
        self.namespace = None
        self.release_name = None
        self.domain_name = None
        self.username = None
        self.psw = None

        # if the user provides a config yaml file, use it for configuration
        yaml_file = os.getenv("CONFIG_YAML_FILE")
        if yaml_file:
            try:
                self._load_from_file(yaml_file)
            except Exception as e:
                sys.exit(f"Failed to load the config file: {e}")
        else:
            self.namespace = os.getenv("CLUSTER_NAMESPACE", "default")
            self.release_name = os.getenv("RELEASE_NAME")
            self.domain_name = os.getenv("DOMAIN_NAME")
            self.username = os.getenv("AUTH_USERNAME")
            self.psw = os.getenv("AUTH_PASSWORD")

        if (
            not self.release_name
            and not self.domain_name
            and not self.username
            and not self.psw
        ):
            sys.exit(
                "You need to provide values for the following variables: RELEASE_NAME, DOMAIN_NAME, AUTH_USERNAME and AUTH_PASSWORD. Exiting ..."
            )
        self.dns_domain = f"{self.release_name}.{self.domain_name}"

        self.timeout = 20  # seconds
        self.base_url = self._get_url()

    def _load_from_file(self, yaml_file):
        config_path = Path(yaml_file)
        if not config_path.exists():
            sys.exit(
                "You didn't provide a valid yaml path or the file does not exist. Exiting ..."
            )
        with config_path.open("r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)

                if not isinstance(data, dict):
                    raise ValueError(
                        f"Expected top-level dict in the config file and got {type(data).__name__}."
                    )

                if data:
                    self.namespace = data.get("namespace", "default")
                    self.release_name = data.get("release_name")
                    self.domain_name = data.get("domain_name")
                    self.username = data.get("auth_username")
                    self.psw = data.get("auth_password")
                else:
                    sys.exit(
                        "You have chosen to use a yaml file for configuration, but you haven't provided values for the needed variables. Exiting ..."
                    )
            except yaml.YAMLError as e:
                raise yaml.YAMLError(
                    f"Error parsing YAML config file at {config_path}: {e}"
                )

    def _get_url(self, *args):
        return urljoin(f"https://{self.dns_domain}/", "/".join(map(str, args)))


settings = ClusterSettings()
