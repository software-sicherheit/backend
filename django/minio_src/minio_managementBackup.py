from minio import Minio
from minio.error import ResponseError, BucketAlreadyExists
import os
from environs import Env


class MinioManagement:

    def __init__(self, access, secret):

        # Read from .env?
        self.bucket_name = "s3storage-e2e-cloud-storage"

        try:
            self.client = Minio(
                'localhost:9010',
                access_key=access,
                secret_key=secret,
                secure=False
            )
            print("Connected to Minio Server!")
        except Exception as e:
            raise e

    # also creates a new one if there isn't one at the moment when an object is put in
    def switch_active_bucket(self, bucket_name):
        self.bucket_name = bucket_name

    #   user_id=bucket_name=user_name(?), file_id=file_name->stored in MonogDB
    # The uuid is the beginning of the filename uuid/file
    def put_object(self, uuid, file_name, byte_data_stream, size_of_data):
        if not self.client.bucket_exists(self.bucket_name):
            try:
                self.client.make_bucket(self.bucket_name)
            except ResponseError as identifier:
                raise
        try:
            with open(file_path, 'rb') as user_file:
                statdata = os.stat('/tmp/test.txt')
                self.client.put_object(
                    user_id,
                    file_name,
                    user_file,
                    statdata.st_size
                )
        except ResponseError as identifier:
            raise

# Generates a string list and returns it, mainly for  remove_files
    def generate_object_list(self, uuid):
        if self.client.bucket_exists(self.bucket_name):
            try:
                objects = self.client.list_objects(self.bucket_name)
                object_list = [x.object_name for x in objects]
                return object_list
            except ResponseError as identifier:
                raise

# Get file returns an object in the form of an httpResponse
    def get_file(self, bucket_name, file_name):
        try:
            response = self.client.get_object(bucket_name, file_name)
            print(response.data.decode())
            return response
        except ResponseError as identifier:
            raise
        finally:
            response.close()
            response.release_conn()

    def  remove_file(self, bucket_name, object_name, object_version_id):
        if self.client.bucket_exists( bucket_name ):
            try:
                self.client.remove_object(bucket_name, object_name) #add version id handeling if needed
            except ResponseError as identifier:
                raise

# Removes all objects given a list of strings and a bucket
    def remove_files(self, bucket_name, object_list):
        if self.client.bucket_exists(bucket_name):
            try:
                for del_err in self.client.remove_objects(bucket_name, object_list):
                    print("Deletion Error: {}".format(del_err))
            except ResponseError as identifier:
                raise

    def remove_empty_bucket(self, bucket_name):
        if self.client.bucket_exists(bucket_name):
            try:
                self.client.remove_bucket(bucket_name)
            except ResponseError as identifier:
                raise

# Empties bucket and deletes it !!Erases whole database!!
    def purge_bucket(self, bucket_name):
        if self.client.bucket_exists(bucket_name):
            try:
                self. remove_files(bucket_name, self.generate_object_list(bucket_name))
                self.remove_empty_bucket(bucket_name)
            except ResponseError as identifier:
                raise
        pass

    def purge_user(self, uuid):
        pass

#if __name__ == '__main__':
#    minioClient = MinioManagement('accesskey', 'secretkey')
#    minioClient.put_object('testbucket', 'nameoffile', '/tmp/test.txt')
#    minioClient.put_object('testbucket', 'nameofanotherfile', '/tmp/test.txt')
#    minioClient. remove_file('testbucket2', 'nameoffile', 'id')
#    minioClient.remove_empty_bucket('testbucket2')
#    minioClient.generate_object_list('testbucket')
#    minioClient.put_object('emptyb', 'nameoffile', '/tmp/test.txt')
#    minioClient.get_file('emptyb', 'nameoffile')
#   print(minioClient.generate_object_list('emptyb'))
