from io import StringIO

# how many chunks to send
NUM_CHUNKS = 100000

# the contents of each chunk
# 4096 bytes total
contents = '0123456789abcde\n' * 256


class STRESS:
    def __init__(self):
        pass

    def __call__(self, env, start_response):
        ''' This is called by auth.py code like: return self.app(env, start_response)
        '''
        return Lookup(start_response)

class Lookup:
    def __init__(self, start_response):
        self.start_response = start_response

    def __iter__(self):
        self.start_response("200 OK", [('Content-Type', "text/plain")])

        buf = StringIO()
        for chunk in range(NUM_CHUNKS):
            buf.write(contents)
            yield buf.getvalue().encode('utf-8')
            buf = StringIO()

        yield "done\n".encode('utf-8')
