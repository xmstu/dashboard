# -*- coding: utf-8 -*-

from server import app, socketio

if __name__ == '__main__':
    socketio.run(app=app, host='127.0.0.1', port=2333)
    # app.run(host='127.0.0.1', port=2333)
