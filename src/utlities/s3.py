import boto3
import os
import logging
from config import S3_CREDS
logging.getLogger('botocore.endpoint').setLevel(logging.CRITICAL)
logging.getLogger('botocore.hooks').setLevel(logging.CRITICAL)
logging.getLogger('botocore.loaders').setLevel(logging.CRITICAL)
logging.getLogger('botocore.parsers').setLevel(logging.CRITICAL)

class S3Handler:

    def __init__(self):
        self.bucket = "fashinza"
        self.s3_path = S3_CREDS['S3_PREFIX']
        self.access_key = S3_CREDS['AWS_ACCESS_KEY_ID']
        self.secret_key = S3_CREDS['AWS_SECRET_ACCESS']
        self.s3_client = self.get_s3_client()
        self.s3_resource = self.get_s3_resource()
        self.s3_bucket = self.get_s3_bucket()

    def get_s3_client(self):
        return boto3.client('s3',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key)
    
    def get_s3_resource(self):
        return boto3.resource('s3',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key)
    
    def get_s3_bucket(self):
        return self.s3_resource.Bucket(self.bucket)
    
    def s3_upload(self,data,key):
        self.s3_client.put_object(Body=data, Bucket=self.bucket, Key=key)
        logging.info(f"Data uploaded to s3://{self.bucket}/{self.s3_path}")

    def get_s3_object(self,key):
        return self.s3_resource.Object(self.bucket, key)
    
    def get_s3_objects(self,prefix):
        objs = self.s3_bucket.objects.filter(Prefix=prefix)
        return objs
    
    def s3_download(self,key):
        self.s3_bucket.download_file(key, key)
        logging.info(f"Data downloaded from s3://{self.bucket}/{self.s3_path}")

    def s3_delete(self,key):
        self.s3_client.delete_object(Bucket=self.bucket, Key=key)
        logging.info(f"Data deleted from s3://{self.bucket}/{self.s3_path}")

    def s3_list(self,objects):
        return [obj.key for obj in objects]
    
    def s3_delete_all(self):
        for key in self.s3_list():
            self.s3_delete(key)
        logging.info(f"All data deleted from s3://{self.bucket}/{self.s3_path}")

    def s3_download_all(self):
        for key in self.s3_list():
            self.s3_download(key)
        logging.info(f"All data downloaded from s3://{self.bucket}/{self.s3_path}")

    def s3_upload_all(self,data):
        for key in data.keys():
            self.s3_upload(data[key],key)
        logging.info(f"All data uploaded to s3://{self.bucket}/{self.s3_path}")
    