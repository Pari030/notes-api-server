from typing import Any

from flask import request
from werkzeug.exceptions import BadRequest


def get_param(param: str) -> Any:
    try:
        return request.json[param]
    except KeyError:
        raise ValueError(f'Missing {param} parameter')
    except BadRequest:
        raise TypeError('Invalid JSON')
