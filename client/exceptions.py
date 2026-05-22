class ClientError(Exception):
    pass


class NotFoundError(ClientError):
    pass


class ValidationError(ClientError):
    pass


class ServerError(ClientError):
    pass
