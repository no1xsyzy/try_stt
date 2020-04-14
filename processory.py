class Processor:
    def __init__(self):
        self.processes = {}

    def register(self, func):
        name = func.__name__
        if name in self.processes:
            raise ValueError("Subprocess `{name}' already registered. "
                             """Use `@processor.register_as(name="new_name")' instead""")
        self.processes[name] = func
        return func

    def process(self, command):
        try:
            cmd, *opts = command.split(" ")
            return self.processes[cmd](*filter(None, opts))
        except:
            return 'back_err', "error!"
