#!/usr/bin/env python3
import boto3
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

# How old (days) before deletion
AGE_THRESHOLD_DAYS = 30

def get_all_regions(ec2_client):
    """Return a list of all AWS regions."""
    return [r["RegionName"] for r in ec2_client.describe_regions()["Regions"]]

def delete_old_unattached_volumes():
    ec2_client = boto3.client("ec2")
    cutoff = datetime.now(timezone.utc) - timedelta(days=AGE_THRESHOLD_DAYS)
    total_deleted = 0

    for region in get_all_regions(ec2_client):
        print(f"\n Checking region {region}...")
        ec2 = boto3.resource("ec2", region_name=region)
        filters = [{"Name": "status", "Values": ["available"]}]
        
        # Initialize paginator for describe_volumes
        paginator = ec2_client.get_paginator('describe_volumes')
        page_iterator = paginator.paginate(Filters=filters)

        for page in page_iterator:
            for vol in page['Volumes']:
                create_time = vol['CreateTime']
                if create_time < cutoff:
                    try:
                        volume = ec2.Volume(vol['VolumeId'])
                        volume.delete()
                        print(f"✅ Deleted {vol['VolumeId']} (created {create_time.date()})")
                        total_deleted += 1
                    except ClientError as e:
                        print(f"❌ {vol['VolumeId']}: {e}")
    print(f"\n🧹 Finished — total volumes deleted: {total_deleted}")

if __name__ == "__main__":
    delete_old_unattached_volumes()
