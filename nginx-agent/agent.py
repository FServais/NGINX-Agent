#!flask/bin/python

from __future__ import print_function

import subprocess
import sys
import argparse
import pam

from flask import Flask, request, jsonify
from flask.ext.restful import Api, Resource, reqparse, abort
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

from Exceptions import get_exception_dict, SiteListNotAvailable, SiteNotFound, UnableToPushConfiguration
from IO.IO import IO

app = Flask(__name__)
api = Api(app, errors=get_exception_dict())

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    # The credentials <User; Password> will be the same as the system on which the Agent is run.
    return pam.authenticate(username, password, service='system-auth')


def reload_nginx():
    p = subprocess.Popen(["sudo service nginx restart"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    pass


class PingAPI(Resource):

    def get(self):
        """
        @api {get} / Ping the agent

        @apiName PingAgent
        @apiDescription Send a request to the agent to test the connectivity.
        @apiGroup Agent

        @apiExample Example:
            GET /

        @apiSuccessExample Success response
            HTTP/1.1 200 OK
        """
        return 'Reached!'



class SiteListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('allAvailable', type=str, location='args')
        super(SiteListAPI, self).__init__()

    def get(self):
        """
        @api {get} /config/site Get the list of the sites.

        @apiName GetListSites
        @apiDescription Get the list of the sites on the Agent, either activated (= in 'enabled' directory) or not (= in 'available' directory).
        @apiGroup Sites

        @apiParam {Boolean} [allAvailable=False] Should list all the available (not necessarily enabled) sites.

        @apiSuccess (200) {List}    sites        List of the available or enabled sites.
        @apiSuccess (200) {Boolean} allAvailable Copy of the paramater 'allAvailable' received in the query.

        @apiExample Example:
            GET /config/site?allAvailable=True

        @apiSuccessExample Success response, retrieving all the sites
            HTTP/1.1 200 OK
            {
                'sites': ['default', 'site1', 'site2'],
                'allAvailable': true
            }

        @apiSuccessExample Success response, retrieving only the enabled sites
            HTTP/1.1 200 OK
            {
                'sites': ['default'],
                'allAvailable': false
            }
        """
        args = self.reqparse.parse_args()

        list_all_sites_available = args['allAvailable']
        if list_all_sites_available is not None:
            list_all_sites_available = list_all_sites_available.lower() == 'true'
        else:
            list_all_sites_available = False

        status, sites = IO.list_available_sites() if list_all_sites_available else IO.list_enabled_sites()

        if status is False:
            raise SiteListNotAvailable()

        return {'sites': sites,
                 'allAvailable': list_all_sites_available}


class SiteConfigAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('config', type=str, location='json')
        self.reqparse.add_argument('enable', type=str, location='json')
        super(SiteConfigAPI, self).__init__()

    def get(self, site_name):
        """
        @api {get} /config/site/:site_name Get a configuration.

        @apiName GetSiteConfig
        @apiDescription Retrieve the configuration of a site.
        @apiGroup Configuration

        @apiParam {String} site_name Name of the site.

        @apiSuccess (200) {String} config   Configuration of the site.

        @apiExample Example:
            GET /config/site/default

        @apiSuccessExample Success response
            HTTP/1.1 200 OK
            {
                'config': "Configuration of the site"
            }

        @apiError SiteNotFound The configuration does not exist.

        @apiErrorExample {json} Error-Response:
         HTTP/1.1 404 Not Found
         {
           "status": 404
           "message": "Site not found."
         }

        """

        status, config = IO.site_config(site_name)

        if status is False:
            raise SiteNotFound()

        return {'config': config}

    def post(self, site_name):
        """
        @api {post} /config/site/:site_name Push a configuration.

        @apiName PushSiteConfig
        @apiDescription Create a configuration for a site.
        @apiGroup Configuration

        @apiParam {String} site_name Name of the site.
        @apiParam {String}   config    Configuration of the site.
        @apiParam {String}   enable    Activate the configuration.

        @apiSuccess (200) {int} state   Status of the operation, 1 if everything went well.

        @apiExample Example:
            POST /config/site/default

        @apiParamExample {json} Configuration example:
            {
                'config': "Configuration...",
                'enable': "True"
            }

        @apiSuccessExample Success response
            HTTP/1.1 200 OK
            {
                'state': 1
            }

        """
        args = self.reqparse.parse_args()

        config = args['config']
        enable = args['enable']

        if enable is not None:
            enable = (enable.lower() == "true")
        else:
            enable = False

        result = IO.create_site_config(site_name, config)
        if result is not True:
            raise UnableToPushConfiguration()

        if enable:
            IO.enable_config(site_name)
        else:
            IO.disable_config(site_name)

        reload_nginx()

        return {'state': 1}

    def put(self, site_name):
        """
        @api {put} /config/site/:site_name Update a configuration.

        @apiName UpdateSiteConfig
        @apiDescription Replace a configuration for a site.
        @apiGroup Configuration

        @apiParam {String} site_name Name of the site.
        @apiParam {String}   config    Configuration of the site.
        @apiParam {String}   enable    Activate the configuration.

        @apiSuccess (200) {int} state   Status of the operation, 1 if everything went well.

        @apiExample Example:
            PUT /config/site/default

        @apiParamExample {json} Configuration example:
            {
                'config': "Configuration...",
                'enable': "True"
            }

        @apiSuccessExample Success response
            HTTP/1.1 200 OK
            {
                'state': 1
            }

        """
        args = self.reqparse.parse_args()
        config = args['config']
        enable = args['enable']

        if enable is not None:
            enable = enable.lower() == "true"
        else:
            enable = False

        result = IO.update_site_config(site_name, config)
        if result is not True:
            raise UnableToPushConfiguration()

        print(enable)
        if enable:
            IO.enable_config(site_name)
        else:
            IO.disable_config(site_name)

        reload_nginx()

        return {'state': 1}


class ConfigDirAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('path', type=str, location='json')
        super(ConfigDirAPI, self).__init__()

    def put(self, site_name):
        default_path = "/etc/nginx"
        args = self.reqparse.parse_args()
        path = args['path']

        if path is None:
            path = default_path

        IO.set_nginx_dir(path)

        return { 'state': 1 }


class GetIPAPI(Resource):
    def get(self):
        return {'ip': request.remote_addr}


api.add_resource(PingAPI, '/')
api.add_resource(SiteListAPI, '/config/site')
api.add_resource(SiteConfigAPI, '/config/site/<site_name>')
api.add_resource(ConfigDirAPI, '/config/nginx/directory')
api.add_resource(GetIPAPI, '/ip')


def run_agent(ip, https=False):
    if https:
        app.run(debug=True, host=ip, ssl_context=('server.crt', 'server.key'))
    else:
        app.run(debug=True, host=ip)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the agent for the NGINX device package.")
    parser.add_argument('--ip', action='store', help='ip of the agent', default='127.0.0.1')
    parser.add_argument('--https', action='store_true', default=False, help='use HTTPS')

    args = parser.parse_args()

    run_agent(args.ip, args.https)