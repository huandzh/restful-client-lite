# restful-client-lite

A lite client for RESTFul APIs.

WIP.

## Installation

pipenv:

```shell
pipenv install -e git+https://github.com/huandzh/restful-client-lite#egg=restful-client-lite
```

pip:

```shell
pip install -e git+https://github.com/huandzh/restful-client-lite#egg=restful-client-lite
```

## Usage

Assume that we have a restful api requiring `Authorization:<token>` in the header and using etag to control writes.

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

Patch url:

```python
res_patch = api.patch("<url>", "<etag>", data={"<key>": "<value>"})
```

Patch url (fetch etag automatically in advance):

```python
res_patch = api.patch_auto_etag("<url>", data={"<key>": "<value>"})
```

Delete url:

```python
res_delete = api.delete("<url>", "<etag>")
```

Delete url (fetch etag automatically in advance):

```python
res_delete = api.delete_auto_etag("<url>")
```
