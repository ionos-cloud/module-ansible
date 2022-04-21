#!/bin/bash

api_resp_raw=$( curl -s 'https://api.github.com/repos/ionos-cloud/module-ansible/actions/runs?status=in_progress' )
api_resp_only_name=$( echo "$api_resp_raw" | jq -r '.workflow_runs[]|"\(.name)"' )

running_banned_workflows=0
for banned_workflow in "$@"
do
  for i in ${api_resp_only_name[$name]}
  do
    if [ "$i" = "$banned_workflow" ]; then
      running_banned_workflows=$((running_banned_workflows+1))
    fi
  done
done

is_banned_running=false
if [ "$running_banned_workflows" -gt 1 ]; then
  is_banned_running=true
fi

echo "::set-output name=is_banned_running::$is_banned_running"
