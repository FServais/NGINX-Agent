from werkzeug.exceptions import HTTPException

def get_exception_dict():
    exceptions = {}

    exceptions["SiteListNotAvailable"] = {'status': 500,
                                          'message': 'Not possible to retrieve the list of the sites.'}

    exceptions["SiteNotFound"] = {'status': 404,
                                  'message': 'Site not found.'}

    exceptions["UnableToPushConfiguration"] = {'status': 500,
                                               'message': "Unable to push configuration."}

    return exceptions


class SiteListNotAvailable(HTTPException):
    pass

class SiteNotFound(HTTPException):
    pass

class UnableToPushConfiguration(HTTPException):
    pass