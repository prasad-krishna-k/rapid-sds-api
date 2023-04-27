#!/usr/bin/env python
# encoding: utf-8
import json
import os
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS
from flask import jsonify
import pandas as pd

app = Flask(__name__)
CORS(app)
base_url = "/api/v1/rapid_insight/insight/"

dict_5 = {"paysafe": [{"name": "Production", "y": 100}, {"name": "Dev", "y": 70}, {"name": "QA", "y": 10},
                      {"name": "Staging", "y": 10}],
          "telstra": [{"name": "Production", "y": 70}, {"name": "Dev", "y": 700}, {"name": "QA", "y": 50}]}
dict_12 = {"paysafe": [{"name": "Disabled", "y": 60}, {"name": "Enabled", "y": 40}],
           "telstra": [{"name": "Disabled", "y": 80}, {"name": "Enabled", "y": 20}]}
dict_8 = {"paysafe": [{"name": "United States", "count": 5, "domains": ["paysafr.com", "paysafec.com", "paysafi.com"]},
                      {"name": "United Kingdom", "count": 1, "domains": ["paysave.com"]},
                      {"name": "India", "count": 2, "domains": ["paysage.com", "pagsafe.com"]}],
          "telstra": [{"name": "United States", "count": 2, "domains": ["telst.com", "telstraa.com"]},
                      {"name": "Australia", "count": 2, "domains": ["telsta.au", "ttelstra.com"]}]}

dict_10 = {"paysafe": [{"name": "3306", "y": 2}, {"name": "8000", "y": 10}, {"name": "8001", "y": 1}],
           "telstra": [{"name": "5432", "y": 10}, {"name": "8080", "y": 3}]}
dict_13 = {"paysafe": {"framework_name": "NIST CSF", "framework_code": "nist", "number_of_levels": 1, "components": [{
    "ceis": [
        {
            "cei_code": "1.1",
            "cei_description": "Active Devices without SSL Certificates",
            "control": "ID.AM1",
            "score": 80},
        {
            "cei_code": "1.2",
            "cei_description": "Security misconfigurations",
            "control": "ID.AM2",
            "score": 60}],
    "component_id": "id",
    "component_code": "ID",
    "component_name": "Identify",
    "component_type": "Function",
    "component_level": 1,
    "component_family": "",
    "component_type_code": "function",
    "component_weightage": 1,
    "component_description": "",
    "score": 70},
    {
        "ceis": [
            {
                "cei_code": "1.3",
                "cei_description": "Vulnerable ports are not made publicily available",
                "control": "PR.DS2",
                "score": 50}],
        "component_id": "pr",
        "component_code": "PR",
        "component_name": "Protect",
        "component_type": "Function",
        "component_level": 1,
        "component_family": "",
        "component_type_code": "function",
        "component_weightage": 1,
        "component_description": "",
        "score": 50},
    {
        "ceis": [
            {
                "cei_code": "1.6",
                "cei_description": "Certificate secured by unsecured algorithms",
                "control": "DE.AM3",
                "score": 100},
            {
                "cei_code": "1.7",
                "cei_description": "Certificate issues by untrusted authorities",
                "control": "DE.AM4",
                "score": 20}],
        "component_id": "de",
        "component_code": "DE",
        "component_name": "Detect",
        "component_type": "Function",
        "component_level": 1,
        "component_family": "",
        "component_type_code": "function",
        "component_weightage": 1,
        "component_description": "",
        "score": 60}]},
           "telstra": {"framework_name": "NIST CSF", "framework_code": "nist", "number_of_levels": 1, "components": [{
               "ceis": [
                   {
                       "cei_code": "1.1",
                       "cei_description": "Active Devices without SSL Certificates",
                       "control": "ID.AM1",
                       "score": 80},
                   {
                       "cei_code": "1.2",
                       "cei_description": "Security misconfigurations",
                       "control": "ID.AM2",
                       "score": 60}],
               "component_id": "id",
               "component_code": "ID",
               "component_name": "Identify",
               "component_type": "Function",
               "component_level": 1,
               "component_family": "",
               "component_type_code": "function",
               "component_weightage": 1,
               "component_description": "",
               "score": 70},
               {
                   "ceis": [
                       {
                           "cei_code": "1.3",
                           "cei_description": "Vulnerable ports are not made publicily available",
                           "control": "PR.DS2",
                           "score": 50}],
                   "component_id": "pr",
                   "component_code": "PR",
                   "component_name": "Protect",
                   "component_type": "Function",
                   "component_level": 1,
                   "component_family": "",
                   "component_type_code": "function",
                   "component_weightage": 1,
                   "component_description": "",
                   "score": 50},
               {
                   "ceis": [
                       {
                           "cei_code": "1.6",
                           "cei_description": "Certificate secured by unsecured algorithms",
                           "control": "DE.AM3",
                           "score": 100},
                       {
                           "cei_code": "1.7",
                           "cei_description": "Certificate issues by untrusted authorities",
                           "control": "DE.AM4",
                           "score": 20}],
                   "component_id": "de",
                   "component_code": "DE",
                   "component_name": "Detect",
                   "component_type": "Function",
                   "component_level": 1,
                   "component_family": "",
                   "component_type_code": "function",
                   "component_weightage": 1,
                   "component_description": "",
                   "score": 60}]}}

dict_7 = {"paysafe": [{"name": "MySQL 5.7.37", "count": 2}, {"name": "MongoDB 7.37", "count": 1}],
          "telstra": [{"name": "MySQL 5.7.37", "count": 5}, {"name": "MongoDB 5.37", "count": 2},
                      {"name": "Postgres 9", "count": 2}]}

dict_6 = {"paysafe": [{"name": "nginx 1.15.0", "count": 2}, {"name": "apache server 2.4.0", "count": 1}],
          "telstra": [{"name": "nginx 1.15.0", "count": 2}, {"name": "apache server 2.4.0", "count": 1}]}

dict_11 = {"paysafe": [{"name": "Disabled", "y": 75}, {"name": "Enabled", "y": 25}],
           "telstra": [{"name": "Disabled", "y": 60}, {"name": "Enabled", "y": 40}]}


@app.route('/')
def index():
    return json.dumps({'version': '1.0',
                       'state': 'Application is up and running'})


@app.route(base_url + "5")
def five():
    value = request.args.to_dict().get("client")
    return jsonify(dict_5.get(value))


@app.route(base_url + "8")
def eight():
    value = request.args.to_dict().get("client")
    return jsonify(dict_8.get(value))


@app.route(base_url + "12")
def twelve():
    value = request.args.to_dict().get("client")
    return jsonify(dict_12.get(value))


@app.route(base_url + "10")
def ten():
    value = request.args.to_dict().get("client")
    return jsonify(dict_10.get(value))


@app.route(base_url + "7")
def seven():
    value = request.args.to_dict().get("client")
    return jsonify(dict_7.get(value))


@app.route(base_url + "9")
def nine():
    value = request.args.to_dict().get("client")
    return jsonify(dict_13.get(value))


@app.route(base_url + "6")
def six():
    value = request.args.to_dict().get("client")
    return jsonify(dict_6.get(value))


@app.route(base_url + "11")
def eleven():
    value = request.args.to_dict().get("client")
    return jsonify(dict_11.get(value))


@app.route(base_url + "13")
def thirteen():
    value = request.args.to_dict().get("client")
    df = pd.read_csv("/home/krishnaprasad/Downloads/sample.csv").query(
        "client==" + "'" + value + "'")[
        ["ip_address", "hostname", "client", "open_ports", "security_header", "extract_ssl_info"]]
    dict_value = df.to_dict(orient='records')
    # print(dict_value)
    return jsonify(dict_value)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
