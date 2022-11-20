import threading

class ChainedMethodsPipe:
    def __init__(self, name, cmp_func):
        self.name = name
        self.cmp_func = cmp_func

    def run(self):
        print("CMP start:", self.name)
        thread_locals = threading.local()
        thread_locals.ChainedMethodPipe_curr_cmp_name = self.name
        ret = self.cmp_func()
        print("cmp end:", self.name)
        return ret
        
def call_cmp(cmp_name, cmp_func):
    return ChainedMethodsPipe(cmp_name, cmp_func).run()

