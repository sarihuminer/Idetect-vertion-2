import json
from flask import Flask, escape, request
import detect_id
from flask_cors import CORS
import pre_ocr_api
import connect_to_datastoresql
import detect_type_card
import os
import yaml

app = Flask('helloworld')
CORS(app)
cnt = 0
print(cnt)


# @app.route('/')
# def hello():
#    return 'Hello, World!'

@app.route('/api/args', methods=["GET", "POST"])
# for local running
def detect_type(request):
    print("detect card id {}".format(request))
    if request.method == 'OPTIONS':
        print('in options')
        cors_enabled_function_auth(request)
    if request.method == "POST":
        print(request.form)
        user = request.form.get('user')
        image = request.form.get('image')
        if user is None:
            return {"error": "no user"}, 400, get_headers()
        # enviroment = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        # p = yaml.safe_load(data)
        # p = yaml.safe_load('env.yaml')
        # file('env.yaml', 'w')

        # print(p['GOOGLE_APPLICATION_CREDENTIALS'])
        # with open('evn.yaml') as config_file:
        # json_file = json.load(config_file)
        # print(type(json_file), json_file)
        enviroment = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

        project_id = 'idetectsari'
        model_id = 'ICN1559144570408409826'
        print("before coming to automl image {} project_id {} model_id {} enviroment {}")
        print("image {}".format(image))
        print("image {}".format(project_id))
        print("image {}".format(model_id))
        print("image {}".format(enviroment))
        automl_response = detect_type_card.get_prediction(image, project_id, model_id, enviroment)
        print("automl_response {}".format(automl_response))
        score = automl_response.payload[0].classification.score
        type_certificate = automl_response.payload[0].display_name
        if score > 0.66:
            if type_certificate == "passportCard":
                jsonfile = "pasport_card_config.json"
            else:
                if type_certificate == "visaUsa":
                    jsonfile = "visa_united_state.json"
                else:
                    if type_certificate == "greenCard":
                        jsonfile = "green_card_config.json"
            fields = connect_to_datastoresql.get_config(user, type_certificate)
            result = detect_id.detect_id(image, jsonfile)
            response = {'result': result, 'fields': fields}
            return response, 200, get_headers()

        else:
            return {"error": "the picture is not clear"}, 400, get_headers()


# @app.route('/api/args', methods=["GET", "POST"])  # for prodaction
# def detectImg(request):
#     if request.method == 'OPTIONS':
#         print('in options')
#         cors_enabled_function_auth(request)
#     if request.method == "POST":
#         print(request.form)
#         user =req uest.form.get('user')
#         image = request.form.get('image')
#         if user is None:
#             return {"error": "no user"}, 400, get_headers()
#         fields = connect_to_datastoresql.get_config(user)
#         result = detect_id.detect_id(image, 'pasport_card_config.json')
#         response = {'result': result, 'fields': fields}
#         return response, 200, get_headers()


@app.route('/api/addConfig', methods=["GET", "POST"])  # for local running
def add_site_Config(request):
    print("add_site_config {}".format(request))
    if request.method == 'OPTIONS':
        cors_enabled_function_auth(request)
    if request.method == "POST":
        print(request.form)
        site = request.form.get('adress')
        con = request.form.get('configurationsite')
        # site = request.args.get('adress')
        # con = request.args.get('configurationsite')
        print("site {} his config {}".format(site, con))
        connect_to_datastoresql.connect_to_sql(site, con)
        return '', 200, get_headers()


# @app.route('/api/addConfig', methods=["GET", "POST"])  # for prodaction
# def addConfig(request):
#     if request.method == 'OPTIONS':
#         cors_enabled_function_auth(request)
#     if request.method == "POST":
#         print(request.form)
#         site = request.form.get('adress')
#         con = request.form.get('configurationsite')
#         # site = request.args.get('adress')
#         # con = request.args.get('configurationsite')
#         print("site {} his config {}".format(site, con))
#         connect_to_datastoresql.connect_to_sql(site, con)
#         return '', 200, get_headers()

@app.route('/api/hasConfig', methods=["GET", "POST"])  # for local
def has_configuration_site(request):
    print("has_configuration_site request{}".format(request))
    if request.method == 'OPTIONS':
        cors_enabled_function_auth(request)
    if request.method == "GET":
        site = request.args['user']
        print("site")
        if connect_to_datastoresql.check_sql(site) == 'true':
            return 'true', 200, get_headers()
        # with open('installation_fields.json') as config_file:
        # with open('C:\\Users\\sari\\Documents\\IDetectaml\\server\\installation_fields.json') as config_file:
        # json_file = json.load(config_file)
        # print(type(json_file),json_file)
        with open('installation_fields.json') as config_file:
            json_file = json.load(config_file)
            print(type(json_file), json_file)
        return json_file, 200, get_headers()


# @app.route('/api/hasConfig', methods=["GET", "POST"])#for prodaction
# def hasConfig(request):
#     if request.method == 'OPTIONS':
#         cors_enabled_function_auth(request)
#     if request.method == "GET":
#         site = request.args['user']
#         if connect_to_datastoresql.check_sql(site) == 'true':
#           return 'true', 200, get_headers()
#     with open('pasport_card_config.json') as config_file:
#         return json.loads(config_file.read()), 200, get_headers()


def cors_enabled_function_auth(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Authorization',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return '', 204, headers


def get_headers():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }
    return headers


if __name__ == '__main__':
    # app.run(threaded=True,ssl_context='adhoc')
    app.run(threaded=True)
