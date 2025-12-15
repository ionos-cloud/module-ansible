# registry_repository_info

This is a simple module that supports listing existing Repositories

## Example Syntax


```yaml

name: List Repositories
ionoscloudsdk.ionoscloud.registry_repository_info:
  registry: ''
register: repositories_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "href": "<base_url>/registries/0d6fd999-9bf9-462c-a148-951198ebca8f/repositories",
    "id": "repositories",
    "items": [
        {
            "href": "<base_url>/registries/0d6fd999-9bf9-462c-a148-951198ebca8f/repositories/image-test",
            "id": "image-test",
            "metadata": {
                "artifact_count": 1,
                "created_by": null,
                "created_by_user_id": null,
                "created_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "last_modified_date": null,
                "last_pulled_at": null,
                "last_pushed_at": "<datetime>",
                "last_severity": "critical",
                "pull_count": 0,
                "push_count": 1,
                "resource_urn": null
            },
            "properties": {
                "name": "image-test"
            },
            "type": "repository"
        }
    ],
    "limit": 100,
    "links": {
        "next": null,
        "prev": null,
        "var_self": "<base_url>/registries/0d6fd999-9bf9-462c-a148-951198ebca8f/repositories?limit=100&offset=100&orderBy=-lastPush"
    },
    "offset": 0,
    "type": "collection"
}

```

&nbsp;
### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/container-registry).

&nbsp;
### Available parameters:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="22.8vw">Name</th>
      <th width="10.8vw" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>registry<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Registry.</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of properties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
  </tr>
  <tr>
  <td>certificate_fingerprint<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API certificate fingerprint.</td>
  </tr>
  <tr>
  <td>username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos username. Overrides the IONOS_USERNAME environment variable.</td>
  </tr>
  <tr>
  <td>password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos password. Overrides the IONOS_PASSWORD environment variable.</td>
  </tr>
  <tr>
  <td>token<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos token. Overrides the IONOS_TOKEN environment variable.</td>
  </tr>
  </tbody>
</table>
