#!/usr/bin/env bash

# ENV Vars:
# IONOS_USERNAME - username for IONOS Cloud APIs
# IONOS_PASSWORD - password for IONOS Cloud APIs
# IONOS_TOKEN    - token for IONOS Cloud APIs

delete_all_args='--all --force'

function delete_dataplatform_resources() {
  ionosctl dataplatform nodepool delete $delete_all_args
  ionosctl dataplatform cluster delete $delete_all_args

  echo_step_completed
}
