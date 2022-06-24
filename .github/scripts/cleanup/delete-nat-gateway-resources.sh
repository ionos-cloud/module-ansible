#!/usr/bin/env bash

# ENV Vars:
# IONOS_USERNAME - username for IONOS Cloud APIs
# IONOS_PASSWORD - password for IONOS Cloud APIs

delete_all_args='--all --force'

function delete_nat_gateway_resources() {
  dc_list=$(ionosctl datacenter list --no-headers --cols DatacenterId)

  for datacenter in $dc_list; do

    natgateway_list=$(ionosctl natgateway list --datacenter-id $datacenter --no-headers --cols NatGatewayId)
    for natgateway in $natgateway_list; do
      echo_sub_step "deleting all resources from ${natgateway} NAT Gateway, ${datacenter} datacenter"

      echo_info "[INFO] deleting flowlogs"
      ionosctl natgateway flowlog delete --datacenter-id $datacenter --natgateway-id $natgateway $delete_all_args

      echo_info "[INFO] deleting rules"
      ionosctl natgateway rule delete --datacenter-id $datacenter --natgateway-id $natgateway $delete_all_args

      echo_info "[INFO] deleting natgateway"
      ionosctl natgateway delete --datacenter-id $datacenter --natgateway-id $natgateway --force

    done
  done

  echo_step_completed
}
