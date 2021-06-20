from enum import IntEnum, Enum

from common.const_str import RESPONSE_CODE, RESPONSE_TEXT


class Status(IntEnum):
    SUCCESS = 200
    INVALID_PASSWORD = 400
    RE_LOG_IN = 401


def status_text(code):
    status_message = {
        Status.SUCCESS: "Ok",
        Status.INVALID_PASSWORD: "Invalid password",
        Status.RE_LOG_IN: "Please log in agent"
    }
    return status_message.get(code, "Undefined error")


def response_msg(code):
    return {
        RESPONSE_CODE: code.value,
        RESPONSE_TEXT: status_text(code)
    }
