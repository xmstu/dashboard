# -*- coding: utf-8 -*-
# import threading

from server import app
# from server.resources.message_push import election


# def inner():
#     t = threading.Thread(target=election.start, args=())
#     t.start()
#     app.run(host='127.0.0.1', port=2333)


if __name__ == '__main__':
    # from werkzeug._reloader import run_with_reloader
    # run_with_reloader(inner)
    app.run(host='127.0.0.1', port=2333)
