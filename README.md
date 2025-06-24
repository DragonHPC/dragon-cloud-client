# Dragon REST Python API Client and CLI


REST API client and CLI for a Dragon cluster. It is implemented with `requests` and
`click` python packages.


## Installation

To install the client and CLI package:

```bash
pip install https://github.com/DragonHPC/dragon-cloud-client.git
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



### Start using the client: make http requests

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