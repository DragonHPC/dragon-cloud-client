# Dragon REST Python API Client and CLI


REST API client and CLI for a Dragon cluster. It is implemented with `requests` and
`click` python packages.


## Installation

The Dragon client currently requires a minimum python version of 3.10.
To install the client and CLI package:

```bash
pip install git+https://github.com/DragonHPC/dragon-cloud-client.git
```


#### Environment variables needed for configuration

In order to start using the CLI, we need to set the following environment variables for the api client:

```bash
export RELEASE_NAME=<release_name>
export DOMAIN_NAME=<domain_name>
export AUTH_USERNAME=<username>
export AUTH_PASSWORD=<psw>
```

The values for all the above variables will be provided by the administrator of the Dragon cluster.

Alternatively, a yaml file can be used. The full path of the file is provided by setting the following variable:

```bash
export CONFIG_YAML_FILE=path/filename.yaml
```

When the above variable is set to a non-empty value, then the code will use the provided file for configuration.
We provide an example file, `my_config.yaml`, you can use and update the values.


### Start using the client: make HTTP requests

Now, we're ready to make requests to the dragon api server.

Get info (id and url) of all the available jupyter notebooks:

```bash
dragon jupyter list
```

Create a new jupyter notebook:

```bash
dragon jupyter create
```

If the user does not provide a jupyter token, the system will create one for them and
use it to login automatically.

Query a specific notebook by providing its notebook id to get its url:

```bash
dragon jupyter get <notebook_id>
```

Delete a notebook by providing its notebook id:

```bash
dragon jupyter delete <notebook_id>
```
