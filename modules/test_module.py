import threading

class Test:
    def __init__(self, function, expect_return, *args):
        self.function = function
        self.args = args
        self.expect_return = expect_return

    def start(self) -> bool:
        return_value = self.function(self.args)
        if (self.expect_return == return_value):
            return True
        else:
            return False

def test_flask_server(app, host, port):
    def decorator(function):
        def wrapper():
            app_thread = threading.Thread(target=app.run, kwargs={"host": host, "port": port})
            app_thread.setDaemon(True)
            app_thread.start()

            function()
            
            raise RuntimeError("Shuttin down server")
        return wrapper
    return decorator
