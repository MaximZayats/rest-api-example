from typing import Any, Dict, Union


class Response:
    _default_200 = {'description': 'OK'}

    _default_404 = {
        'description': 'Not Found',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Object does not exist'
                }
            }
        }
    }

    _default_409 = {
        'description': 'Conflict',
        'content': {
            'application/json': {
                'example': {
                    'detail': [
                        {
                            'loc': [],
                            'msg': '<Error message>',
                            'type': 'IntegrityError'
                        }
                    ]
                }
            }
        }
    }

    GET_LIST: Dict[Union[int, str], Dict[str, Any]] = \
        {200: _default_200}
    GET_BY_ID: Dict[Union[int, str], Dict[str, Any]] = \
        {200: _default_200,
         404: _default_404}

    POST: Dict[Union[int, str], Dict[str, Any]] = \
        {201: {'description': 'Created'},
         409: _default_409}
    PUT: Dict[Union[int, str], Dict[str, Any]] = \
        {204: {'description': 'No Data'},
         404: _default_404}
    PATCH: Dict[Union[int, str], Dict[str, Any]] = \
        {200: _default_200,
         404: _default_404}
    DELETE: Dict[Union[int, str], Dict[str, Any]] = \
        {204: {'description': 'No Data'},
         404: _default_404}
