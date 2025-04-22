#!/usr/bin/python3
from skillnecting import create_app, db
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
'''
sentry_sdk.init(
        dsn="https://a6a69e9eb04440b59d3a51712d98e85c@sentry.io/1321576",
        integrations=[FlaskIntegration()]
    )
'''
app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
