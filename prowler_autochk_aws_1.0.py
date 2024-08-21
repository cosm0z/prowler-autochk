import boto3
import subprocess
import os

# AWS 계정 ID 목록
accounts = [
    "111111111111",
    "222222222222",
    "333333333333"
]

role_name = "audit-prowler-role"

def assume_role(account_id, role_name):
    sts_client = boto3.client('sts')
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="Cybersecurity"
    )
    
    return response['Credentials']

def run_prowler(credentials, account_id):
    # 임시 자격 증명을 환경 변수로 설정
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

    # Prowler 실행
    #command = f"prowler aws"
    #result = subprocess.run(command, text=True)
    result = subprocess.run(['prowler', 'aws', '-M', 'json-ocsf', 'html', '--compliance', 'cis_3.0_aws', '--severity', 'critical', 'high'], text=True)

def main():
    for account_id in accounts:
        print(f"Assuming role in account {account_id}")
        credentials = assume_role(account_id, role_name)
        run_prowler(credentials, account_id)

if __name__ == "__main__":
    main()
