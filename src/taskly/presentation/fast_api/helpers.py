from starlette.requests import Request


def get_client_ip(request: Request) -> str:

    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()

    x_real_ip = request.headers.get('X-Real-Ip')

    if x_real_ip:
        return x_real_ip

    return request.client.host