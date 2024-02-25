# conn_string = "host='eximsimplee-uat.czadhpxedfpe.ap-south-1.rds.amazonaws.com'
# dbname='postgres' user='postgres' password='eximsimplee' port=5432 sslmode='require'"

DB_CREDS = {
    "host": "eximsimplee-uat.czadhpxedfpe.ap-south-1.rds.amazonaws.com",
    "dbname": "postgres",
    "user": "postgres",
    "password": "eximsimplee",
    "port": 5432,
    "sslmode": "require"
}



# save to s3 bucket 
# s3://fashinza/zara/
# acess key AKIA6FXCAGDV2MIIAONJ
# secret key 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


# os.environ['S3_PREFIX'] = 'zara'
# os.environ['AWS_ACCESS_KEY_ID']='AKIA6FXCAGDV2MIIAONJ'
# os.environ['AWS_SECRET_ACCESS']='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'

S3_CREDS = {
    "S3_PREFIX": "zara",
    "AWS_ACCESS_KEY_ID": "AKIA6FXCAGDV2MIIAONJ",
    "AWS_SECRET_ACCESS": "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"
}