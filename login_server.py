import ssl
import os
import cgi
import json
import config as cfg
from http.server import HTTPServer, BaseHTTPRequestHandler
from cookie import get_cookie_value, create_cookie_header
from db import get_user, get_active_users, create_or_update_session
from hashing import matchHashedText, create_token, is_token_signature_validated
from urllib.parse import parse_qs
from exceptions import InvalidCredentialsException, RequestNotSupportedException, InvalidTokenException
from datetime import datetime, timedelta


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self._is_request_authenticated():
            self._handle_authenticated_request()
        else:
            self._handle_anonymous_request()

    def _handle_anonymous_request(self):
        if self.path == '/isAuthenticated':
            self._do_anonymous_api_request()
        else:
            self._do_anonymous_static_request()

    def _do_anonymous_api_request(self):
        response_obj = {
            "status": "Success",
            "isAuthenticated": False
        }
        self._send_response_object(response_obj)

    def _send_response_object(self, response_obj, code=200, headers=None):

        if headers is None:
            headers = [('Content-type', 'application/json')]

        self.send_response(code)
        for header in headers:
            self.send_header(header[0], header[1])
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response_obj), 'utf-8'))

    def _do_anonymous_static_request(self):
        if self.path == '/':
            filename = 'index.html'
        else:
            filename = self.path[1:]

        self._do_static_request(filename)

    def _handle_authenticated_request(self):

        if self.path == '/':
            self._do_static_request('various.html')

        elif '.' in self.path:
            self._do_static_request(self.path[1:])

        else:
            self._do_authenticated_api_request()

    def _is_request_authenticated(self):
        auth_token = get_cookie_value(self.headers['Cookie'], 'Auth')
        is_token_valid = False
        is_token_expired = True
        if auth_token:
            is_token_valid = is_token_signature_validated(auth_token, cfg.AUTH_KEY)
            is_token_expired = self._is_token_expired(auth_token)

        return is_token_valid and not is_token_expired

    @staticmethod
    def _is_token_expired(auth_token):
        expiration_date = auth_token.split(cfg.COOKIE_DELIMITER)[cfg.COOKIE_EXPIRATION_DATE_POSITION]
        is_token_expired = datetime.strptime(expiration_date, cfg.DATETIME_FORMAT) < datetime.now()
        return is_token_expired

    def _do_authenticated_api_request(self):
        response_code = 500
        response_obj = {
            "status": "Failed",
            "message": "Error"
        }
        headers = []
        try:
            response_obj = self._handle_request()

            response_code = 200
            renewed_session_cookie = self._get_renewed_session()
            if renewed_session_cookie:
                headers.append(renewed_session_cookie)
        except RequestNotSupportedException:
            response_code = 404
        except InvalidTokenException:
            response_code = 403
            # reset cookies
            headers.append(create_cookie_header('', 'Auth', datetime.min.strftime(cfg.DATETIME_FORMAT)))
            headers.append(create_cookie_header('', 'Session', datetime.min.strftime(cfg.DATETIME_FORMAT)))
            response_obj = self._make_response_object(message='Session Expired, please re-login', status='Failed')
        except Exception as e:
            import traceback
            print(traceback.print_exc())
            response_code = 500
        finally:
            headers.append(('Content-type', 'application/json'))
            self._send_response_object(response_obj, response_code, headers)

    def _handle_request(self):
        if self.path == '/isAuthenticated':
            response_obj = {
                "status": "Success",
                "isAuthenticated": True
            }
        elif self.path == '/getActiveUsers':
            response_obj = {
                "status": "Success",
                "users": get_active_users()
            }
        else:
            raise RequestNotSupportedException
        return response_obj

    def _do_static_request(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.send_response(200)
                if filename[-4:] == '.css':
                    self.send_header('Content-type', 'text/css')
                elif filename[-5:] == '.json':
                    self.send_header('Content-type', 'application/javascript')
                elif filename[-3:] == '.js':
                    self.send_header('Content-type', 'application/javascript')
                elif filename[-4:] == '.ico':
                    self.send_header('Content-type', 'image/x-icon')
                else:
                    self.send_header('Content-type', 'text/html')

                self.end_headers()
                self.wfile.write(file.read())

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('not found', 'utf-8'))

    def do_POST(self):

        payload = self._read_payload()
        form_email, form_password = bytes.decode(payload[b'email'][0]), bytes.decode(payload[b'password'][0])

        headers = []
        response_code = 500
        response_obj = {}

        try:
            user_record = get_user(form_email)

            if user_record is None or not matchHashedText(user_record[cfg.PASSWORD], form_password):
                raise InvalidCredentialsException

            auth_cookie = self._create_cookie(key=cfg.AUTH_KEY,
                                              text=user_record[cfg.EMAIL],
                                              expiration_time=(
                                                  datetime.now() + timedelta(days=cfg.AUTH_MAX_DAYS)).strftime(
                                                  cfg.DATETIME_FORMAT),
                                              cookie_name='Auth'
                                              )

            session_cookie = self._create_cookie(key=cfg.SESSION_KEY,
                                                 text=user_record[cfg.EMAIL],
                                                 expiration_time=(
                                                     datetime.now() + timedelta(
                                                         minutes=cfg.SESSION_MAX_MINUTES)).strftime(
                                                     cfg.DATETIME_FORMAT),
                                                 cookie_name='Session'
                                                 )

            headers.extend([auth_cookie, session_cookie])

            response_code = 200
            response_obj = self._make_response_object(message='Welcome ' + user_record[cfg.EMAIL] + ' !',
                                                      status='Success')

        except InvalidCredentialsException:
            response_code = 404
            response_obj = self._make_response_object(message='Invalid credentials',
                                                      status='failed')
        except Exception as e:
            print(e)
            response_code = 500
            response_obj = self._make_response_object(message='Internal Server Error',
                                                      status='failed')

        finally:
            headers.append(('Content-type', 'application/json'))
            self._send_response_object(response_obj, response_code, headers)

    def _read_payload(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        return postvars

    def _get_renewed_session(self):
        session_token = get_cookie_value(self.headers['Cookie'], 'Session')
        is_token_valid = is_token_signature_validated(session_token, cfg.SESSION_KEY)
        if is_token_valid:
            renewed_expiration_time = datetime.now() + timedelta(minutes=cfg.SESSION_MAX_MINUTES)
            session_id = session_token.split(cfg.COOKIE_DELIMITER)[cfg.COOKIE_ID_POSITION]
            renewed_session_token = create_token(cfg.SESSION_KEY, session_id, renewed_expiration_time.strftime(
                cfg.DATETIME_FORMAT))
            create_or_update_session(session_id, renewed_expiration_time)
            return renewed_session_token

        raise InvalidTokenException

    @staticmethod
    def _make_response_object(message, status):
        return {
            'message': message,
            'status': status
        }

    @staticmethod
    def _create_cookie(cookie_name,
                       text,
                       expiration_time,
                       key):
        hashed_token = create_token(key=key,
                                    text=text,
                                    expiration_time=expiration_time
                                    )
        return create_cookie_header(hashed_token, cookie_name, expiration_time)


# Changing working dir to 'static' folder to prevent outside source-code access
static_dir = os.path.join(os.path.dirname(__file__), 'static')
os.chdir(static_dir)

httpd = HTTPServer(('localhost', cfg.PORT_NUMBER), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               keyfile="../security/key.pem",
                               certfile='../security/cert.pem', server_side=True)

print('Started httpserver on port ', cfg.PORT_NUMBER)
httpd.serve_forever()
