import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2024-09-06-14-33-14-226'

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(
        endpoint_name=ENDPOINT
        )

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences = predictor.predict(image)

    # We return the data back to the Step Function
    event["body"]["inferences"] = json.loads(inferences)

    return {
        'statusCode': 200,
        'body': event["body"]
    }

#{
#   "statusCode": 200,
#   "body": {
#     "s3_bucket": "sagemaker-us-east-1-481249975987",
#     "s3_key": "test/bicycle_s_000513.png",
#     "image_data": "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",
#     "inferences": []
#   }
# }
