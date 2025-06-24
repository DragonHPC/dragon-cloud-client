import os
import sys
from pathlib import Path
import yaml
from urllib.parse import urljoin


class ClusterSettings:

    def __init__(self):
        # if the user provides a config yaml file, use it for configuration
        yaml_file = os.getenv("CONFIG_YAML_FILE")
        if yaml_file:
            self._load_from_file(yaml_file)
        else:
            self.namespace = os.getenv("CLUSTER_NAMESPACE", "default")
            self.release_name = os.getenv("RELEASE_NAME")
            self.domain_name = os.getenv("DOMAIN_NAME")
            self.username = os.getenv("AUTH_USERNAME")
            self.psw = os.getenv("AUTH_PASSWORD")

        if not self.release_name and not self.domain_name:
            sys.exit(
                "You need to provide values for both RELEASE_NAME and DOMAIN_NAME variables. Exiting ..."
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

        data = yaml.safe_load(config_path.open()) or {}
        self.namespace = data.get("namespace", "default")
        self.release_name = data.get("release_name")
        self.domain_name = data.get("domain_name")
        self.username = data.get("auth_username")
        self.psw = data.get("auth_password")

    def _get_url(self, *args):
        return urljoin(f"https://{self.dns_domain}/", "/".join(map(str, args)))


settings = ClusterSettings()
