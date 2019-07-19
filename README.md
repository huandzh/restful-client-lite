# restful-client-lite

A lite client for RESTFul APIs.

WIP.

## Installation (this branch)

pipenv:

```shell
pipenv install -e git+https://github.com/huandzh/restful-client-lite@init#egg=restful-client-lite
```

pip:

```shell
pip install -e git+https://github.com/huandzh/restful-client-lite@init#egg=restful-client-lite
```

## Usage

Create an API client:

```python
from restful_client_lite import APIClient
api = APIClient("<api_root>", {"token": "<token>"})
```

Get from url:

```python
res_get = api.get("<url>")
```

Post to url:

```python
res_post = api.post("<url>", data={"<key>": "<value>"})
```

Patch to url:

```python
res_patch = api.patch("<url>", "<etag>", data={"<key>": "<value>"})
```

Patch to url (fetch etag automatically in advance):

```python
res_patch = api.patch_auto_etag("<url>", data={"<key>": "<value>"})
```
