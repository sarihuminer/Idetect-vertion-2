import sys
import os
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
import base64
import binascii
import struct


# import binascii


def get_prediction(pictutre, project_id, model_id, enviroment):
    print("get_prediction automl sari huminer")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'IDetectsari.json'
    # with open(file_path, 'rb') as ff:
    # content = ff.read()
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    binstr = b"thisisunreadablebytes"

    # encoded = binascii.b2a_base64(binstr)
    # print(encoded + '/n')
    # print(binascii.a2b_base64(encoded))

    # ba = bytearray(binstr)
    # print(list(ba))

    # print(binascii.b2a_hex(binstr) + '/n')
    # print(struct.unpack("21B", binstr) + '/n')

    # content = binascii_a2b_base64(pictutre)
    # pictutre = pictutre.encode('utf8')
    #    import base64
    pic = base64.b64decode(pictutre)
    # pictutre = base64.b64encode(pictutre.encode())
    payload = {'image': {'image_bytes': pic}}
    # payload={pictutre}
    params = {}
    request = prediction_client.predict(name, payload, params)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = enviroment
    return request  # waits till rqeuest is returned


if __name__ == '__main__':
    # file_path = sys.argv[1]
    # project_id = sys.argv[2]
    # model_id = sys.argv[3]

    file_path = sys.argv[1]
    project_id = sys.argv[2]
    model_id = sys.argv[3]
    enviroment = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    print(file_path + project_id + model_id)

    print(get_prediction(project_id, model_id, enviroment))
