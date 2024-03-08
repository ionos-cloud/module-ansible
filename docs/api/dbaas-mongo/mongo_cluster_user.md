# mongo_cluster_user

This is a module that supports creating and destroying Mongo Cluster Users

## Example Syntax


```yaml
name: Create Cluster User
ionoscloudsdk.ionoscloud.mongo_cluster_user:
  mongo_cluster: ''
  mongo_username: testuser
  mongo_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  user_roles:
  - role: read
    database: test
register: mongo_user_response

name: Update User
ionoscloudsdk.ionoscloud.mongo_cluster_user:
  mongo_cluster: ''
  mongo_username: testuser
  mongo_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  user_roles:
  - role: read
    database: test
  - role: readWrite
    database: test
  state: update
register: mongo_user_response

name: Delete Cluster User
ionoscloudsdk.ionoscloud.mongo_cluster_user:
  mongo_cluster: ''
  mongo_username: testuser
  state: absent
register: mongo_user_response

```

&nbsp;
&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "mongo_cluster_user": {
        "type": "user",
        "metadata": {
            "created_date": "2023-05-30T14:20:09+00:00",
            "created_by": "<USER_EMAIL>",
            "created_by_user_id": "<USER_ID>"
        },
        "properties": {
            "username": "testuser",
            "password": null,
            "roles": [
                {
                    "role": "read",
                    "database": "test"
                }
            ]
        }
    }
}

```

### For more examples please check out the tests [here](https://github.com/ionos-cloud/module-ansible/tree/master/tests/dbaas-mongo).
&nbsp;

&nbsp;

# state: **present**
```yaml
  name: Create Cluster User
ionoscloudsdk.ionoscloud.mongo_cluster_user:
  mongo_cluster: ''
  mongo_username: testuser
  mongo_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  user_roles:
  - role: read
    database: test
register: mongo_user_response

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
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>mongo_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the user.</td>
  </tr>
  <tr>
  <td>mongo_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The password of the user.</td>
  </tr>
  <tr>
  <td>user_roles<br/><mark style="color:blue;">list</mark></td>
  <td align="center">True</td>
  <td>A list of mongodb user roles. A user role is represented as a dict containing 2 keys:'role': has one of the following values: 'read', 'readWrite' or 'readAnyDatabase''database': the name of the databse to which the role applies</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'update', 'absent']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  name: Update User
ionoscloudsdk.ionoscloud.mongo_cluster_user:
  mongo_cluster: ''
  mongo_username: testuser
  mongo_password: '{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits') }}'
  user_roles:
  - role: read
    database: test
  - role: readWrite
    database: test
  state: update
register: mongo_user_response

```
### Available parameters for state **update**:
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
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>mongo_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the user.</td>
  </tr>
  <tr>
  <td>mongo_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The password of the user.</td>
  </tr>
  <tr>
  <td>user_roles<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>A list of mongodb user roles. A user role is represented as a dict containing 2 keys:'role': has one of the following values: 'read', 'readWrite' or 'readAnyDatabase''database': the name of the databse to which the role applies</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'update', 'absent']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  name: Delete Cluster User
ionoscloudsdk.ionoscloud.mongo_cluster_user:
  mongo_cluster: ''
  mongo_username: testuser
  state: absent
register: mongo_user_response

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
  <td>mongo_cluster<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The UUID or name of an existing Mongo Cluster.</td>
  </tr>
  <tr>
  <td>mongo_username<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The username of the user.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'update', 'absent']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
