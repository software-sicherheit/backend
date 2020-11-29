from minio import Minio
from minio.error import ResponseError, BucketAlreadyExists
import os
from environs import Env
import json

class MinioManagement:

    def __init__(self, access, secret):

        # Read from .env?
        self.bucket_name = "e2e-cloud-storage"

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
    def put_object(self, uuid, file_name, blob, size_of_data):
        if not self.client.bucket_exists(self.bucket_name):
            try:
                self.client.make_bucket(self.bucket_name)
            except ResponseError as identifier:
                raise
        try:
                con_filename = str(uuid) + '/' + str(file_name)
                print("Shouldgivethefilenamehere: ")
                print(con_filename)
                self.client.put_object(
                    self.bucket_name,
                    con_filename,
                    blob,
                    size_of_data
                )
        except ResponseError as identifier:
            raise

# Generates a string list and returns it, no given uuid => get whole bucket
# Generates a list of filenames, used to delete multiple files
    def generate_object_list(self, uuid=None):
        if self.client.bucket_exists(self.bucket_name):
            try:
                if uuid is None:
                    objects = self.client.list_objects(self.bucket_name, recursive=True)
                else:
                    # p1:bucketname,p2:prefix,p3:recursive?,p4:includeversion
                    objects = self.client.list_objects(self.bucket_name, prefix=uuid+'/', recursive=True)
                object_list = [x.object_name for x in objects]
                return object_list
            except ResponseError as identifier:
                raise

    # Generates a json list with all elements and returns it, no given uuid => get whole bucket
    def generate_object_list_json(self, uuid=None):
        if self.client.bucket_exists(self.bucket_name):
            try:
                if uuid is None:
                    objects = self.client.list_objects(self.bucket_name, recursive=True)
                else:
                    # p1:bucketname,p2:prefix,p3:recursive?,p4:includeversion
                    objects = self.client.list_objects(self.bucket_name, prefix=uuid, recursive=True)

                jsondata = []
                for x in objects:
                    jsondata.append(
                    {
                        'id':               uuid,                 # to be filled in views from jwt
                        'filename':         str(x.object_name).split('/')[1],
                        'contentType':      str(x.content_type),
                        'size':             int(x.size),
                        'lastModifiedDate': str(x.last_modified),
                    })
                return jsondata
            except ResponseError as identifier:
                raise

# Get file returns an object in the form of an httpResponse
    def get_file(self, uuid, file_name):
        try:
            path = uuid + "/" + file_name
            response = self.client.get_object(self.bucket_name, path)
            object = self.client.list_objects(self.bucket_name, prefix=path, recursive=False)

            x = object[0]

            jsondata={
                    'id': uuid,
                    'filename': str(x.object_name).split('/')[1],
                    'contentType': str(x.content_type),
                    'size': int(x.size),
                    'lastModifiedDate': str(x.last_modified),
                    'blob' : response.data.decode()
                }

            return jsondata
        except ResponseError as identifier:
            raise
        finally:
            response.close()
            response.release_conn()

    def  remove_file(self, uuid, object_name):
        if self.client.bucket_exists( self.bucket_name ):
            try:
                path = uuid+"/"+object_name
                self.client.remove_object(self.bucket_name, path)
            except ResponseError as identifier:
                raise

# Removes all objects given a list of strings and a bucket
    def remove_files(self, object_list):
        if self.client.bucket_exists(self.bucket_name):
            try:
                for del_err in self.client.remove_objects(self.bucket_name, object_list):
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

    def purge_user(self, uuid):
        #uuid_files_list = []
        uuid_files_list = self.generate_object_list(uuid)
        print(uuid_files_list)
        self.remove_files(uuid_files_list)
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
