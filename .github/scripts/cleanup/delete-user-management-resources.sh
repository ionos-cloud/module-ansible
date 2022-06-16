#!/usr/bin/env bash

# ENV Vars:
# IONOS_USERNAME - username for IONOS Cloud APIs
# IONOS_PASSWORD - password for IONOS Cloud APIs

delete_all_args='--all --force'

function delete_user_management_resources() {

  group_list=$(ionosctl group list --cols GroupId --no-headers)

  for group in $group_list; do
    echo_sub_step "deleting all resources from ${group} group"

    echo_info "[INFO] deleting all shares"
    ionosctl share delete --group-id $group $delete_all_args -w

    echo_info "[INFO] removing all the users from the group"
    ionosctl group user remove --group-id $group $delete_all_args

    echo_info "[INFO] deleting group ${group_id}"
    ionosctl group delete --group-id $group -w --force

  done

  echo_sub_step "deleting all users"
  ionosctl user delete $delete_all_args

  echo_step_completed
}
