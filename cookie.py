
def get_cookie_value(cookies, cookie_name):
    # Cookie check
    if not cookies:
        return

    cookies_elements = cookies.split('; ')
    cookie_obj = {}
    for cookie in cookies_elements:
        cookie = cookie.split('=')
        cookie_obj[cookie[0]] = cookie[1]

    return cookie_obj.get(cookie_name, None)


def create_cookie_header(auth_token, cookie_name, expiration_date):
    return('Set-Cookie',cookie_name + '=' +
           auth_token +
           '; Expires=' +
           expiration_date +
           '; secure; HttpOnly; SameSite=Strict')

