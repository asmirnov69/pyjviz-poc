curr_pipe_name = "none"

def get_curr_pipe_name():
    return curr_pipe_name

def pipe(pipe_name, pb):
    print("pipe start:", pipe_name)
    globals()['curr_pipe_name'] = pipe_name
    ret = pb()
    print("pipe end:", pipe_name)
    return ret

