import boto3

bucket_name = 'dataset-kagami'
folder_name = 'penguins'

s3 = boto3.resource('s3')
bucket = s3.Bucket('dataset-kagami')

for obj in bucket.objects.filter(Prefix=folder_name):
    if not os.path.exists(os.path.dirname(local_directory + obj.key)):
        os.makedirs(os.path.dirname(local_directory + obj.key))
    bucket.download_file(obj.key, local_directory + obj.key)
