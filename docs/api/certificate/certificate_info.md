# certificate_info

This is a simple module that supports listing uploaded Certificates

## Example Syntax


```yaml

    - name: List Certificates
        certificate_info:
        register: certificates_response
    - name: Show Certificates
        debug:
            var: certificates_response.result

```
### Available parameters:
&nbsp;

| Name | Required | Description |
| :--- | :---: | :--- |
| api_url<br /><span class="blue-span">str</span> | False | The Ionos API base URL. |
| username<br /><span class="blue-span">str</span> | False | The Ionos username. Overrides the IONOS_USERNAME environment variable. |
| password<br /><span class="blue-span">str</span> | False | The Ionos password. Overrides the IONOS_PASSWORD environment variable. |
| token<br /><span class="blue-span">str</span> | False | The Ionos token. Overrides the IONOS_TOKEN environment variable. |
