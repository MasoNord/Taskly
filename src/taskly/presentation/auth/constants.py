from typing import Final

SESSION_ID_DELIVERED_VIA_COOKIE: Final[str] = (
    "Delivered auth session token via cookie."
)
SESSION_ID_INVALID_OR_EXPIRED: Final[str] = "Invalid or expired session"
SESSION_ID_MARKED_FOR_REMOVAL: Final[str] = (
    "Marked access token for removal in response."
)
SESSION_ID_NOT_FOUND_IN_COOKIE: Final[str] = "No session id found in cookie."
SESSION_ID_PAYLOAD_OF_INTEREST: Final[str] = "auth_session_id"

COOKIE_SESSION_ID_NAME = "session_id"
REQUEST_STATE_NEW_SESSION_ID_KEY = "new_session_id"
REQUEST_STATE_DELETE_SESSION_KEY = "delete_session"
REQUEST_STATE_COOKIE_PARAMS_KEY = "cookie_params"

