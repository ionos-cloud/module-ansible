# dns_key

This is a module that supports creating or destroying DNS Zone Keys

## Example Syntax


```yaml
- name: Create Zone Key
    dns_key:
      zone: example.com
      validity: 100
      algorithm: RSASHA256
      ksk_bits: 4096
      zsk_bits: 2048
      nsec_mode: NSEC
      nsec3_iterations: 2
      nsec3_salt_bits: 64
    register: key_response
  
- name: Delete Zone Keys
    dns_zone:
      zone: example.com
      wait: true
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "action": "create",
    "changed": true,
    "zone_key": {
        "id": "6bf01f6d-6792-5c90-9a16-64fc5cd5d1ee",
        "type": "dnsseckeys",
        "href": "/zones/6bf01f6d-6792-5c90-9a16-64fc5cd5d1ee/keys",
        "metadata": {
            "zoneId": "6bf01f6d-6792-5c90-9a16-64fc5cd5d1ee"
        },
        "properties": {
            "keyParameters": {
                "algorithm": "RSASHA256",
                "kskBits": 4096,
                "zskBits": 2048
            },
            "nsecParameters": {
                "nsec3Iterations": 2,
                "nsec3SaltBits": 64,
                "nsecMode": "NSEC"
            },
            "validity": 100
        }
    },
    "failed": false
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Zone Key
    dns_key:
      zone: example.com
      validity: 100
      algorithm: RSASHA256
      ksk_bits: 4096
      zsk_bits: 2048
      nsec_mode: NSEC
      nsec3_iterations: 2
      nsec3_salt_bits: 64
    register: key_response
  
```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>validity<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>Signature validity in days</td>
  </tr>
  <tr>
  <td>algorithm<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>Algorithm used to generate signing keys (both Key Signing Keys and Zone Signing Keys).</td>
  </tr>
  <tr>
  <td>ksk_bits<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>Key signing key length in bits. kskBits &gt;= zskBits</td>
  </tr>
  <tr>
  <td>zsk_bits<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>Zone signing key length in bits.</td>
  </tr>
  <tr>
  <td>nsec_mode<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>NSEC mode.</td>
  </tr>
  <tr>
  <td>nsec3_iterations<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>Number of iterations for NSEC3. (between 0 and 50)</td>
  </tr>
  <tr>
  <td>nsec3_salt_bits<br/><mark style="color:blue;">int</mark></td>
  <td align="center">True</td>
  <td>Salt length in bits for NSEC3. (between 64 and 128, multiples of 8)</td>
  </tr>
  <tr>
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Zone.</td>
  </tr>
  <tr>
  <td>allow_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Delete Zone Keys
    dns_zone:
      zone: example.com
      wait: true
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="70">Name</th>
      <th width="40" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>zone<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of an existing Zone.</td>
  </tr>
  <tr>
  <td>api_url<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The Ionos API base URL.</td>
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
  <tr>
  <td>wait<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False]</td>
  </tr>
  <tr>
  <td>wait_timeout<br/><mark style="color:blue;">int</mark></td>
  <td align="center">False</td>
  <td>How long before wait gives up, in seconds.<br />Default: 600</td>
  </tr>
  <tr>
  <td>state<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
