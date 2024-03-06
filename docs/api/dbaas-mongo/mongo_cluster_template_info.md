# mongo_cluster_template_info

This is a simple module that supports listing existing Mongo Cluster Templates

## Example Syntax


```yaml
name: List Mongo Cluster Templates
ionoscloudsdk.ionoscloud.mongo_cluster_template_info: null
register: mongo_cluster_templates_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "mongo_cluster_templates": [
        {
            "type": "template",
            "id": "3a199f09-9699-4493-a858-82d9f55a382e",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business 4XL",
                "edition": "business",
                "cores": 32,
                "ram": 131072,
                "storage_size": 1280
            }
        },
        {
            "type": "template",
            "id": "ea320e28-b973-457a-86c5-68c19dd06d3d",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business 4XL_S",
                "edition": "business",
                "cores": 32,
                "ram": 131072,
                "storage_size": 2048
            }
        },
        {
            "type": "template",
            "id": "609f3099-ff0d-456a-8ac7-4dd379a6ee14",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business L",
                "edition": "business",
                "cores": 6,
                "ram": 16384,
                "storage_size": 320
            }
        },
        {
            "type": "template",
            "id": "8c2c51c7-f1f8-4f44-bf3e-6e5cc8e50f07",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business M",
                "edition": "business",
                "cores": 4,
                "ram": 8192,
                "storage_size": 160
            }
        },
        {
            "type": "template",
            "id": "d5d6aa0a-6db0-4440-a5ac-00cd42b00bb3",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business S",
                "edition": "business",
                "cores": 2,
                "ram": 4096,
                "storage_size": 80
            }
        },
        {
            "type": "template",
            "id": "7f646ba1-a739-485f-b5f6-1039958553d5",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business XL",
                "edition": "business",
                "cores": 8,
                "ram": 32768,
                "storage_size": 640
            }
        },
        {
            "type": "template",
            "id": "6b78ea06-ee0e-4689-998c-fc9c46e781f6",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business XS",
                "edition": "business",
                "cores": 1,
                "ram": 2048,
                "storage_size": 50
            }
        },
        {
            "type": "template",
            "id": "14d23a55-22d6-46f9-b884-2f864f3fda0f",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Business XXL",
                "edition": "business",
                "cores": 16,
                "ram": 65536,
                "storage_size": 960
            }
        },
        {
            "type": "template",
            "id": "33457e53-1f8b-4ed2-8a12-2d42355aa759",
            "metadata": {
                "created_date": null,
                "created_by": null,
                "created_by_user_id": null,
                "last_modified_date": null,
                "last_modified_by": null,
                "last_modified_by_user_id": null,
                "state": null,
                "health": null
            },
            "properties": {
                "name": "MongoDB Playground",
                "edition": "playground",
                "cores": 1,
                "ram": 2048,
                "storage_size": 50
            }
        }
    ],
    "failed": false,
    "changed": false
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
