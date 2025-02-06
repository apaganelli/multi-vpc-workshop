#
# Necessita da permissão AmazonEC2FullAccess ser adicionada ao Instance Profile.
#
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Busca instâncias com a tag AutoTerminate=true
    instances = ec2.describe_instances(Filters=[
        {'Name': 'tag:TerminatedByLambda', 'Values': ['true']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])

    # Percorre a lista Reservations, cada reservation pode ter uma lista de instâncias
    instance_ids = [
        i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']
    ]
    
    if instance_ids:
        print(f"Encerrando instâncias: {instance_ids}")
        ec2.terminate_instances(InstanceIds=instance_ids)
    else:
        print("Nenhuma instância para encerrar.")

    return {"status": "completed", "terminated_instances": instance_ids}
