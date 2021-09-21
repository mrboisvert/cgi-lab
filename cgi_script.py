#!/usr/bin/env python3

import os, json, secret

try:
    from cgi import escape #v3.7
except:
    from html import escape #v3.8

logged_in = False

def _wrapper(page):
    """
    Wraps some text in common HTML.
    """
    return ("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 24em;
                margin: auto;
                color: #333;
                background-color: #fdfdfd
            }

            .spoilers {
                color: rgba(0,0,0,0); border-bottom: 1px dashed #ccc
            }
            .spoilers:hover {
                transition: color 250ms;
                color: rgba(36, 36, 36, 1)
            }

            label {
                display: flex;
                flex-direction: row;
            }

            label > span {
                flex: 0;
            }

            label> input {
                flex: 1;
            }

            button {
                font-size: larger;
                float: right;
                margin-top: 6px;
            }
        </style>
    </head>
    <body>
    """ + page + """
    </body>
    </html>
    """)

def secret_page(username=None, password=None):
    """
    Returns the HTML for the page visited after the user has logged-in.
    """
    if username is None or password is None:
        raise ValueError("You need to pass both username and password!")

    return _wrapper("""
    <h1> Welcome, {username}! </h1>

    <p> <small> Pst! I know your password is
        <span class="spoilers"> {password}</span>.
        </small>
    </p>
    """.format(username=escape(username.capitalize()),
               password=escape(password)))

def login_page():
    """
    Returns the HTML for the login page.
    """

    return _wrapper(r"""
    <h1> Welcome! </h1>

    <form method="POST" action="login.py">
        <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
        <label> <span>Password:</span> <input type="password" name="password"></label>

        <button type="submit"> Login! </button>
    </form>
    """)

print("Content-type:text/html\r\n\r\n")
print("<h1>Hello World!</h1>")

environ = dict(os.environ)
json_environ = json.dumps(environ)
#print(json_environ)

for key in environ:
    if key == "QUERY_STRING":
        print("\r\n\r\n")
        print("<h1>Query Parameters: </h1>")
        print(environ[key])
    elif key == "HTTP_USER_AGENT":
        print("\r\n\r\n")
        print("<h1>Web Browser: </h1>")
        print(environ[key])
    elif key == "HTTP_COOKIE":
        cookies = environ[key]
        if "password=%s" % secret.password in cookies and "username=%s" % secret.username in cookies:
            cookies = cookies.split(";")
            password = cookies[0].split("=")[1]
            username = cookies[1].split("=")[1]
            print(secret_page(username=username, password=password))

print(login_page())