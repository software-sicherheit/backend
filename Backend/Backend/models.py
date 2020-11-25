from djongo import models


class User(models.Model):
    uuid = models.IntegerField(unique=True, primary_key=True)
    creation_time = models.DateTimeField()
    username = models.CharField(max_length=1024, unique=True)
    password_hash = models.JSONField()
    symmetricKey = models.CharField(max_length=1024)
    privateKey_PSS = models.CharField(max_length=1024)
    publicKey_PSS = models.CharField(max_length=1024)
    privateKey_OAEP = models.CharField(max_length=1024)
    publicKey_OAEP = models.CharField(max_length=1024)
    minio_path = models.CharField(max_length=1024)

    objects = models.DjongoManager()

    class Meta():

        unique_together = [['uuid', 'password_hash']]






