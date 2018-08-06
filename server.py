# -*- coding: utf-8 -*-

from server import socketio, app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2333)
    # socketio.run(app=app, host='127.0.0.1', port=2333)
