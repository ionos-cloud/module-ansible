# registry_artifact_info

This is a simple module that supports listing existing Artifacts

## Example Syntax


```yaml

    - name: List Artifacts
        registry_artifact_info:
            registry: "RegistryName"
            repository: "repositoryName"
        register: artifacts_response

    - name: Show Artifacts
        debug:
            var: artifacts_response.result

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "href": "<base_url>/registries/0d6fd999-9bf9-462c-a148-951198ebca8f/artifacts",
    "id": "artifacts",
    "items": [
        {
            "href": "<base_url>/registries/0d6fd999-9bf9-462c-a148-951198ebca8f/repositories/image-test/artifacts/<digest>",
            "id": "<digest>",
            "metadata": {
                "created_by": null,
                "created_by_user_id": null,
                "created_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "last_modified_date": null,
                "last_pulled_at": null,
                "last_pushed_at": "<datetime>",
                "last_scanned_at": "<datetime>",
                "pull_count": 0,
                "push_count": 1,
                "resource_urn": null,
                "vuln_fixable_count": 45,
                "vuln_max_severity": "critical",
                "vuln_total_count": 57,
                "vuln_total_score": 389.39993
            },
            "properties": {
                "digest": "<digest>",
                "media_type": "application/vnd.docker.distribution.manifest.v2+json",
                "repository_name": "image-test",
                "tags": [
                    "latest"
                ]
            },
            "type": "artifact"
        }
    ],
    "limit": 100,
    "links": {
        "next": null,
        "prev": null,
        "var_self": "<base_url>/registries/0d6fd999-9bf9-462c-a148-951198ebca8f/artifacts?limit=100&offset=100&orderBy=-pullCount"
    },
    "offset": 0,
    "type": "collection"
}

```

&nbsp;

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
  <td>repository<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The name of an existing Repository.</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format: 'properties.name': 'server_name'</td>
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
