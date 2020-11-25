from minio import Minio 
from minio.error import ResponseError, BucketAlreadyExists
import os

def getMinioClient(access, secret):
    return Minio(
            'localhost:9010',
            access_key=access,
            secret_key=secret,
            secure=False
    )

#   user_id=bucket_name=user_name(?), file_id=file_name->stored in MonogDB
def putObject( user_id, file_id, file_path):
    
    if (not minioClient.bucket_exists( user_id )):
            try:
                minioClient.make_bucket( user_id )
            except ResponseError as identifier:
                raise
    try: 
        with open( file_path,'rb') as user_file:
            statdata = os.stat('/tmp/test.txt')
            minioClient.put_object(
                    user_id,
                    file_id,
                    user_file,
                    statdata.st_size
            )
    except ResponseError as identifier:
        raise

def deleteObject():
    pass


if __name__ == '__main__':
    minioClient = getMinioClient('accesskey','secretkey')
    putObject("name_of_the_file", "testbucket", "pathnotusedjet")





#    if (not minioClient.bucket_exists('testbucket')):
#            try:
#                minioClient.make_bucket('testbucket')
#            except ResponseError as identifier:
#                raise

#    try: 
#        with open('/tmp/test.txt','rb') as testfile:
#            statdata = os.stat('/tmp/test.txt')
#            minioClient.put_object(
#                    'testbucket',
#                    'miniotest.txt',
#                    testfile,
#                    statdata.st_size
#            )
#    except ResponseError as identifier:
#        raise

#    try:                 #_bucket('testbucket')
#        minioClient.remove_object('testbucket','miniotest.txt')
#    except ResponseError as identifier:
#        raise


