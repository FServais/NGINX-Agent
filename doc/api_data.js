define({ "api": [  {    "type": "get",    "url": "/",    "title": "Ping the agent",    "name": "PingAgent",    "description": "<p>Send a request to the agent to test the connectivity.</p> ",    "group": "Agent",    "examples": [      {        "title": "Example:",        "content": "GET /",        "type": "json"      }    ],    "success": {      "examples": [        {          "title": "Success response",          "content": "HTTP/1.1 200 OK",          "type": "json"        }      ]    },    "version": "0.0.0",    "filename": "./agent.py",    "groupTitle": "Agent"  },  {    "type": "get",    "url": "/config/site/:site_name",    "title": "Get a configuration.",    "name": "GetSiteConfig",    "description": "<p>Retrieve the configuration of a site.</p> ",    "group": "Configuration",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "site_name",            "description": "<p>Name of the site.</p> "          }        ]      }    },    "success": {      "fields": {        "200": [          {            "group": "200",            "type": "<p>String</p> ",            "optional": false,            "field": "config",            "description": "<p>Configuration of the site.</p> "          }        ]      },      "examples": [        {          "title": "Success response",          "content": "HTTP/1.1 200 OK\n{\n    'config': \"Configuration of the site\"\n}",          "type": "json"        }      ]    },    "examples": [      {        "title": "Example:",        "content": "GET /config/site/default",        "type": "json"      }    ],    "version": "0.0.0",    "filename": "./agent.py",    "groupTitle": "Configuration"  },  {    "type": "post",    "url": "/config/site/:site_name",    "title": "Push a configuration.",    "name": "PushSiteConfig",    "description": "<p>Create a configuration for a site.</p> ",    "group": "Configuration",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "site_name",            "description": "<p>Name of the site.</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "config",            "description": "<p>Configuration of the site.</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "enable",            "description": "<p>Activate the configuration.</p> "          }        ]      },      "examples": [        {          "title": "Configuration example:",          "content": "{\n    'config': \"Configuration...\",\n    'enable': \"True\"\n}",          "type": "json"        }      ]    },    "success": {      "fields": {        "200": [          {            "group": "200",            "type": "<p>int</p> ",            "optional": false,            "field": "state",            "description": "<p>Status of the operation, 1 if everything went well.</p> "          }        ]      },      "examples": [        {          "title": "Success response",          "content": "HTTP/1.1 200 OK\n{\n    'state': 1\n}",          "type": "json"        }      ]    },    "examples": [      {        "title": "Example:",        "content": "POST /config/site/default",        "type": "json"      }    ],    "version": "0.0.0",    "filename": "./agent.py",    "groupTitle": "Configuration"  },  {    "type": "put",    "url": "/config/site/:site_name",    "title": "Update a configuration.",    "name": "UpdateSiteConfig",    "description": "<p>Replace a configuration for a site.</p> ",    "group": "Configuration",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "site_name",            "description": "<p>Name of the site.</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "config",            "description": "<p>Configuration of the site.</p> "          },          {            "group": "Parameter",            "type": "<p>String</p> ",            "optional": false,            "field": "enable",            "description": "<p>Activate the configuration.</p> "          }        ]      },      "examples": [        {          "title": "Configuration example:",          "content": "{\n    'config': \"Configuration...\",\n    'enable': \"True\"\n}",          "type": "json"        }      ]    },    "success": {      "fields": {        "200": [          {            "group": "200",            "type": "<p>int</p> ",            "optional": false,            "field": "state",            "description": "<p>Status of the operation, 1 if everything went well.</p> "          }        ]      },      "examples": [        {          "title": "Success response",          "content": "HTTP/1.1 200 OK\n{\n    'state': 1\n}",          "type": "json"        }      ]    },    "examples": [      {        "title": "Example:",        "content": "PUT /config/site/default",        "type": "json"      }    ],    "version": "0.0.0",    "filename": "./agent.py",    "groupTitle": "Configuration"  },  {    "type": "get",    "url": "/config/site",    "title": "Get the list of the sites.",    "name": "GetListSites",    "description": "<p>Get the list of the sites on the Agent, either activated (= in 'enabled' directory) or not (= in 'available' directory).</p> ",    "group": "Sites",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "<p>Boolean</p> ",            "optional": true,            "field": "allAvailable",            "defaultValue": "False",            "description": "<p>Should list all the available (not necessarily enabled) sites.</p> "          }        ]      }    },    "success": {      "fields": {        "200": [          {            "group": "200",            "type": "<p>List</p> ",            "optional": false,            "field": "sites",            "description": "<p>List of the available or enabled sites.</p> "          },          {            "group": "200",            "type": "<p>Boolean</p> ",            "optional": false,            "field": "allAvailable",            "description": "<p>Copy of the paramater 'allAvailable' received in the query.</p> "          }        ]      },      "examples": [        {          "title": "Success response, retrieving all the sites",          "content": "HTTP/1.1 200 OK\n{\n    'sites': ['default', 'site1', 'site2'],\n    'allAvailable': true\n}",          "type": "json"        },        {          "title": "Success response, retrieving only the enabled sites",          "content": "HTTP/1.1 200 OK\n{\n    'sites': ['default'],\n    'allAvailable': false\n}",          "type": "json"        }      ]    },    "examples": [      {        "title": "Example:",        "content": "GET /config/site?allAvailable=True",        "type": "json"      }    ],    "version": "0.0.0",    "filename": "./agent.py",    "groupTitle": "Sites"  },  {    "success": {      "fields": {        "Success 200": [          {            "group": "Success 200",            "optional": false,            "field": "varname1",            "description": "<p>No type.</p> "          },          {            "group": "Success 200",            "type": "<p>String</p> ",            "optional": false,            "field": "varname2",            "description": "<p>With type.</p> "          }        ]      }    },    "type": "",    "url": "",    "version": "0.0.0",    "filename": "./doc/main.js",    "group": "_Users_fservais_Projects_Nginx_Agent_doc_main_js",    "groupTitle": "_Users_fservais_Projects_Nginx_Agent_doc_main_js",    "name": ""  }] });