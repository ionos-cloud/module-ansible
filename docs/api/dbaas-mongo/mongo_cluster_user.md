# mongo_cluster_user

This is a module that supports creating and destroying Mongo Cluster Users

## Example Syntax


```yaml
- name: Create Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <password>
      user_roles:
        - role: read
          database: test
    register: mongo_user_response
  
- name: Update User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <newPassword>
      user_roles:
        - role: read
          database: test
        - role: readWrite
          database: test
      state: update
    register: mongo_user_response
  
- name: Delete Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
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

&nbsp;

&nbsp;

# state: **present**
```yaml
  - name: Create Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <password>
      user_roles:
        - role: read
          database: test
    register: mongo_user_response
  
```
### Available parameters for state **present**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | mongo_cluster<br /><span style="color:blue">\<str\></span> | True | The UUID or name of an existing Mongo Cluster. |
  | mongo_username<br /><span style="color:blue">\<str\></span> | True | The username of the user. |
  | mongo_password<br /><span style="color:blue">\<str\></span> | True | The password of the user. |
  | user_roles<br /><span style="color:blue">\<list\></span> | True | A list of mongodb user roles. A user role is represented as a dict containing 2 keys:'role': has one of the following values: 'read', 'readWrite' or 'readAnyDatabase''database': the name of the databse to which the role applies |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'update', 'absent'] |

&nbsp;

&nbsp;
# state: **update**
```yaml
  - name: Update User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
      mongo_password: <newPassword>
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

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | mongo_cluster<br /><span style="color:blue">\<str\></span> | True | The UUID or name of an existing Mongo Cluster. |
  | mongo_username<br /><span style="color:blue">\<str\></span> | True | The username of the user. |
  | mongo_password<br /><span style="color:blue">\<str\></span> | False | The password of the user. |
  | user_roles<br /><span style="color:blue">\<list\></span> | False | A list of mongodb user roles. A user role is represented as a dict containing 2 keys:'role': has one of the following values: 'read', 'readWrite' or 'readAnyDatabase''database': the name of the databse to which the role applies |
  | do_not_replace<br /><span style="color:blue">\<bool\></span> | False | Boolean indincating if the resource should not be recreated when the state cannot be reached in another way. This may be used to prevent resources from being deleted from specifying a different value to an immutable property. An error will be thrown instead<br />Default: False |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'update', 'absent'] |

&nbsp;

&nbsp;
# state: **absent**
```yaml
  - name: Delete Cluster User
    mongo_cluster_user:
      mongo_cluster: MongoClusterName
      mongo_username: testuser
    register: mongo_user_response
  
```
### Available parameters for state **absent**:
&nbsp;

  | Name | Required | Description |
  | :--- | :---: | :--- |
  | mongo_cluster<br /><span style="color:blue">\<str\></span> | True | The UUID or name of an existing Mongo Cluster. |
  | mongo_username<br /><span style="color:blue">\<str\></span> | True | The username of the user. |
  | api_url<br /><span style="color:blue">\<str\></span> | False | The Ionos API base URL. |
  | username<br /><span style="color:blue">\<str\></span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
  | password<br /><span style="color:blue">\<str\></span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
  | token<br /><span style="color:blue">\<str\></span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
  | wait<br /><span style="color:blue">\<bool\></span> | False | Wait for the resource to be created before returning.<br />Default: True<br />Options: [True, False] |
  | wait_timeout<br /><span style="color:blue">\<int\></span> | False | How long before wait gives up, in seconds.<br />Default: 600 |
  | state<br /><span style="color:blue">\<str\></span> | False | Indicate desired state of the resource.<br />Default: present<br />Options: ['present', 'update', 'absent'] |

&nbsp;

&nbsp;
