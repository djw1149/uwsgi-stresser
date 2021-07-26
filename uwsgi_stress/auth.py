class noauth():
    def __init__(self, app):
        self.app = app

    def __call__(self, env, start_response):
        return self.app(env, start_response)
