errors = {
    'ExpiredSignatureError': {
        'message': "Signature has expired",
        'status': 412,
    },
    'RevokedTokenError': {
        'message': "Token has been revoked",
        'status': 412,
    },
    'ConnectionRefusedError': {
        'message': "Backend services are not reachable",
        'status': 500,
    },
    'ServiceUnavailable': {
        'message': "Backend services are not ready",
        'status': 500,
    }
}
