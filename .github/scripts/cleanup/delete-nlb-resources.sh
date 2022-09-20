#!/usr/bin/env bash

# ENV Vars:
# IONOS_USERNAME - username for IONOS Cloud APIs
# IONOS_PASSWORD - password for IONOS Cloud APIs

delete_all_args='--all --force'

function delete_nlb_resources() {
  dc_list=$(ionosctl datacenter list --no-headers --cols DatacenterId)

  for datacenter in $dc_list; do

    nlb_list=$(ionosctl networkloadbalancer list --datacenter-id $datacenter --no-headers --cols NetworkLoadBalancerId)
    for networkloadbalancer in $nlb_list; do
      echo_sub_step "deleting all resources from ${networkloadbalancer} networkloadbalancer, ${datacenter} datacenter"

      echo_info "[INFO] deleting flowlogs"
      ionosctl networkloadbalancer flowlog delete --datacenter-id $datacenter --networkloadbalancer-id $networkloadbalancer $delete_all_args

      echo_info "[INFO] deleting rules"
      ionosctl networkloadbalancer rule delete --datacenter-id $datacenter --networkloadbalancer-id $networkloadbalancer $delete_all_args

      echo_info "[INFO] deleting networkloadbalancer ${networkloadbalancer}"
      ionosctl networkloadbalancer delete --datacenter-id $datacenter --networkloadbalancer-id $networkloadbalancer --force
    done
  done

  echo_step_completed
}
