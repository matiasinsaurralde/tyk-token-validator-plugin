from tyk.decorators import *
from gateway import TykGateway as tyk

import json, requests

@Hook
def ExternalTokenValidatorMiddleware(request, session, metadata, spec):

    token = request.get_header('Authorization')

    if token is None:
        return request, session

    targetUrl = 'https://auth.sipsynergy.co.uk/oauth/token'

    try:
        r = requests.post(targetUrl, headers={'Authorization': token})

        if r.status_code > 299:
            print("The authentication failed")
            request.object.return_overrides.response_code = 401
            request.object.return_overrides.response_error = 'Not authorized by Auth Server'
            return request, session, metadata
    except Exception as e:
        print("An error occured:", e)
        return request, session, metadata

    print("The authentication was successful!")
    session.rate = 1000.0
    session.per = 1.0
    metadata["token"] = "47a0c79c427728b3df4af62b9228c8ae"

    return request, session, metadata
