# Authentication

Credentials can be supplied within a Playbook with the following parameters:

* **username** \(**subscription\_user** is a legacy alias\)
* **password** \(**subscription\_password** is a legacy alias\)
* **token** 

However, the module can also inherit the credentials from environment variables:

* `IONOS_USERNAME`
* `IONOS_PASSWORD`
* `IONOS_TOKEN`

Username and password can be substituted by the token. Usage of the token is not mandatory. For generating a token, see [this](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/token-generate)

> **_NOTE:_**  The API URL can be changed using the following parameter **api_url** in playbooks or using the `IONOS_API_URL` environment variable.

Storing credentials in environment variables is useful if you plan to store your PlayBooks using version control.

