# dns_key_info

This is a simple module that supports listing DNS Keys.

## Example Syntax


```yaml

    - name: Get all DNS Keys in a Zone
      dns_key_info:
        zone: example.com
      register: dns_key_list_response

```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": false,
    "dns_keys": {
        "id": "ec04ab39-2a8f-5d37-b3a9-22f0e202cb1f",
        "type": "dnsseckeys",
        "href": "/zones/ec04ab39-2a8f-5d37-b3a9-22f0e202cb1f/keys",
        "metadata": {
            "zone_id": "ec04ab39-2a8f-5d37-b3a9-22f0e202cb1f",
            "items": [
                {
                    "key_tag": 56066,
                    "sign_algorithm_mnemonic": null,
                    "sign_algorithm_number": null,
                    "digest_algorithm_mnemonic": "SHA-256",
                    "digest_algorithm_number": null,
                    "digest": "<digest>",
                    "key_data": {
                        "flags": 257,
                        "protocol": null,
                        "alg": null,
                        "pub_key": "<pub_key>"
                    },
                    "composed_key_data": "<composed_key_data>"
                }
            ]
        }
    },
    "failed": false
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
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Zone. Will be prioritized if both this and secondary_zone are set.</td>
  </tr>
  <tr>
  <td>filters<br/><mark style="color:blue;">dict</mark></td>
  <td align="center">False</td>
  <td>Filter that can be used to list only objects which have a certain set of propeties. Filters should be a dict with a key containing keys and value pair in the following format:'properties.name': 'server_name'</td>
  </tr>
  <tr>
  <td>depth<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>The depth used when retrieving the items.<br />Default: 1</td>
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
