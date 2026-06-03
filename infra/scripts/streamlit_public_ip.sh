#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <ecs_cluster_name> <ecs_service_name>" >&2
  exit 1
fi

CLUSTER="$1"
SERVICE="$2"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-us-east-1}}"

TASK_ARN="$(aws ecs list-tasks \
  --cluster "$CLUSTER" \
  --service-name "$SERVICE" \
  --desired-status RUNNING \
  --query 'taskArns[0]' \
  --output text \
  --region "$REGION")"

if [[ -z "$TASK_ARN" || "$TASK_ARN" == "None" ]]; then
  echo "No running tasks found for service ${SERVICE}." >&2
  exit 1
fi

ENI_ID="$(aws ecs describe-tasks \
  --cluster "$CLUSTER" \
  --tasks "$TASK_ARN" \
  --query "tasks[0].attachments[?type=='ElasticNetworkInterface'].details[?name=='networkInterfaceId'].value | [0][0]" \
  --output text \
  --region "$REGION")"

PUBLIC_IP="$(aws ec2 describe-network-interfaces \
  --network-interface-ids "$ENI_ID" \
  --query 'NetworkInterfaces[0].Association.PublicIp' \
  --output text \
  --region "$REGION")"

if [[ -z "$PUBLIC_IP" || "$PUBLIC_IP" == "None" ]]; then
  echo "Task is running but has no public IP. Check streamlit_assign_public_ip and VPC routing." >&2
  exit 1
fi

echo "$PUBLIC_IP"
echo "Streamlit URL: http://${PUBLIC_IP}:8501"
