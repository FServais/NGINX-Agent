#!flask/bin/python

from __future__ import print_function

import sys
from flask import Flask, request
from flask.ext.restful import Api, Resource, reqparse

from IO.IO import IO

app = Flask(__name__)
api = Api(app)


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

        return


class SiteListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('allAvailable', type=str, location='args')
        super(SiteListAPI, self).__init__()

    def get(self):
        """
        @api {get} /config/site Retrieve the list of the sites.

        @apiName GetListSites
        @apiDescription Get the list of the sites on the Agent, either activated (= in 'enabled' directory) or not (= in 'available' directory).
        @apiGroup Sites

        @apiParam {Boolean} [allAvailable=False] Should list all the available (not necessarily enabled) sites.

        @apiSuccess (200) {List} sites List of the available or enabled sites.
        @apiSuccess (200) {Boolean} allAvailable Copy of the paramater 'allAvailable' received in the query.

        @apiExample Example:
            GET /config/site?allAvailable=True

        @apiSuccessExample Success response
            HTTP/1.1 200 OK
            {
                'sites': ['default', 'site1', 'site2'],
                'allAvailable': True
            }
        """

        args = self.reqparse.parse_args()

        list_all_sites_available = args['allAvailable']
        if list_all_sites_available is not None:
            list_all_sites_available = list_all_sites_available.lower() == 'true'
        else:
            list_all_sites_available = False

        return { 'sites': IO.list_available_sites() if list_all_sites_available else IO.list_enabled_sites(),
                 'allAvailable': list_all_sites_available}

class SiteConfigAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('config', type=str, location='json')
        super(SiteConfigAPI, self).__init__()

    def get(self, site_name):
        return { 'config': IO.site_config(site_name) }

    def post(self, site_name):
        args = self.reqparse.parse_args()
        config = args['config']

        IO.create_site_config(site_name, config)

        return { 'state': 1 }


api.add_resource(PingAPI, '/')
api.add_resource(SiteListAPI, '/config/site')
api.add_resource(SiteConfigAPI, '/config/site/<site_name>')

if __name__ == "__main__":
    ip = "127.0.0.1"

    if len(sys.argv) > 1:
        ip = sys.argv[1]

    app.run(debug=True, host=ip)