import sys
import os
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2


def get_prediction( project_id, model_id):
    enviroment = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:\\Users\\sari\\Documents\\IDetectsari.json.json'
    with open(file_path, 'rb') as ff:
        content = ff.read()
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content}}
    params = {}
    request = prediction_client.predict(name, payload, params)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = enviroment
    return request  # waits till request is returned


if __name__ == '__main__':
    file_path = 'C:\\Users\\sari\\Pictures\\passport\\023f17b873a7714f35dfbf3e798e3dda.jpg'
    project_id = 'idetectsari'
    model_id = 'ICN1559144570408409826'

    print(get_prediction( project_id, model_id))
