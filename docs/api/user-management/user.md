# user

This module allows you to create, update or remove a user.

## Example Syntax


```yaml
# Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: <email>
      user_password: <password>
      administrator: true
      state: present
  
# Update a user
  - name: Update user
    user:
      firstname: John II
      lastname: Doe
      email: <email>
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  
# Remove a user
  - name: Remove user
    user:
      user: <email>
      state: absent
  
```

&nbsp;

&nbsp;
## Returned object
```json
{
    "changed": true,
    "failed": false,
    "action": "create",
    "user": {
        "entities": null,
        "href": "https://api.ionos.com/cloudapi/v6/um/users/<USER_ID>",
        "id": "<USER_ID>",
        "metadata": {
            "created_date": "2023-05-31T13:41:25+00:00",
            "etag": "37a6259cc0c1dae299a7866489dff0bd",
            "last_login": null
        },
        "properties": {
            "active": true,
            "administrator": false,
            "email": "<EMAIL>",
            "firstname": "John2",
            "force_sec_auth": false,
            "lastname": "Doe",
            "s3_canonical_user_id": null,
            "sec_auth_active": false
        },
        "type": "user"
    }
}

```

&nbsp;

&nbsp;

# state: **present**
```yaml
  # Create a user
  - name: Create user
    user:
      firstname: John
      lastname: Doe
      email: <email>
      user_password: <password>
      administrator: true
      state: present
  
```
### Available parameters for state **present**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="150">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>firstname<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The first name of the user.</td>
  </tr>
  <tr>
  <td>lastname<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The last name of the user.</td>
  </tr>
  <tr>
  <td>email<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The email address of the user.</td>
  </tr>
  <tr>
  <td>user_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>A password for the user.</td>
  </tr>
  <tr>
  <td>administrator<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the user has admin rights.</td>
  </tr>
  <tr>
  <td>force_sec_auth<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if secure authentication should be forced on the user.</td>
  </tr>
  <tr>
  <td>groups<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups.</td>
  </tr>
  <tr>
  <td>sec_auth_active<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if secure authentication is active for the user.</td>
  </tr>
  <tr>
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **absent**
```yaml
  # Remove a user
  - name: Remove user
    user:
      user: <email>
      state: absent
  
```
### Available parameters for state **absent**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="150">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>user<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the user.</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
# state: **update**
```yaml
  # Update a user
  - name: Update user
    user:
      firstname: John II
      lastname: Doe
      email: <email>
      administrator: false
      force_sec_auth: false
      groups:
        - Developers
        - Testers
      state: update
  
```
### Available parameters for state **update**:
&nbsp;

<table data-full-width="true">
  <thead>
    <tr>
      <th width="150">Name</th>
      <th width="116.66666666666663" align="center">Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  <tr>
  <td>firstname<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The first name of the user.</td>
  </tr>
  <tr>
  <td>lastname<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The last name of the user.</td>
  </tr>
  <tr>
  <td>email<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>The email address of the user.</td>
  </tr>
  <tr>
  <td>user<br/><mark style="color:blue;">str</mark></td>
  <td align="center">True</td>
  <td>The ID or name of the user.</td>
  </tr>
  <tr>
  <td>user_password<br/><mark style="color:blue;">str</mark></td>
  <td align="center">False</td>
  <td>A password for the user.</td>
  </tr>
  <tr>
  <td>administrator<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if the user has admin rights.</td>
  </tr>
  <tr>
  <td>force_sec_auth<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if secure authentication should be forced on the user.</td>
  </tr>
  <tr>
  <td>groups<br/><mark style="color:blue;">list</mark></td>
  <td align="center">False</td>
  <td>A list of group IDs or names where the user (non-administrator) is to be added. Set to empty list ([]) to remove the user from all groups.</td>
  </tr>
  <tr>
  <td>sec_auth_active<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Indicates if secure authentication is active for the user.</td>
  </tr>
  <tr>
  <td>do_not_replace<br/><mark style="color:blue;">bool</mark></td>
  <td align="center">False</td>
  <td>Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False</td>
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
  <td>Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'absent', 'update']</td>
  </tr>
  </tbody>
</table>

&nbsp;

&nbsp;
