import boto3
from pprint import pprint as pretty_print
import os
import json


class RekognitionAPI:
    @classmethod
    def from_file(cls, image_file_path, accountAWS):
        with open(image_file_path, "rb") as img_file:
            image = {"Bytes": img_file.read()}
        return cls(image, accountAWS)

    def __init__(self, image, accountAWS):
        awsCredentials = self.getAWSCredentials()
        self.client = boto3.client(
            "rekognition",
            aws_access_key_id=awsCredentials[accountAWS]["access key ID"],
            aws_secret_access_key=awsCredentials[accountAWS]["secret access key"],
            region_name="us-east-2",
        )
        self.image = image

    def getAWSCredentials(self):
        with open("aws credentials.txt", "r") as f:
            return json.loads(f.read())

    def detect_moderation_labels(self):
        try:
            response = self.client.detect_moderation_labels(
                Image=self.image,
                MinConfidence=51,
            )
            moderation_labels = response["ModerationLabels"]
            if moderation_labels:
                pretty_print(moderation_labels)
                print("Number of Modedration Labels Detected:", len(moderation_labels))
                return False
            else:
                print("No Moderation Labels Detected.")
                return True
        except Exception as exception:
            print(
                "Exception occured while detecting moderation labels:",
                type(exception).__name__,
            )
            return False



def image_validation(image_file_name, accountAWS):
    image_file_path = os.path.join(os.getcwd(), image_file_name)
    rekognition_object = RekognitionAPI.from_file(image_file_path, accountAWS)
    like = rekognition_object.detect_moderation_labels()
        
    return like
