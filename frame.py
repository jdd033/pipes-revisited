class Frame:

    def __init__(self, cmd_stack=[], cmd_index=0, handler_stack=[], 
            handler_index=0, state=None):
        self.cmd_stack = list(cmd_stack)
        self.cmd_index = cmd_index
        self.handler_stack = list(handler_stack)
        self.handler_index = handler_index
        self.state = state

    def hasHandler(self):
        return self.handler_index < (len(self.handler_stack) - 1)

    def currentHandler(self):
        try:
            return self.handler_stack[self.handler_index]
        except IndexError:
            return None

    def nextHandler(self):
        if not self.hasHandler():
            return None

        self.handler_index += 1
        return self.handler_stack[self.handler_index]

    def addHandler(self, handler):
        if handler is None:
            return None
        if type(handler) != type([]):
            handler = [handler]
        if self.handler_stack != []:
            self.handler_index += 1
        self.handler_stack.extend(handler)

    def hasCommand(self):
        return self.cmd_index < (len(self.cmd_stack) - 1)

    def currentCommand(self):
        try:
            return self.cmd_stack[self.cmd_index]
        except IndexError:
            return None

    def nextCommand(self):
        if not self.hasCommand():
            return None

        self.cmd_index += 1
        return self.cmd_stack[self.cmd_index]

    def addCommand(self, cmd):
        if cmd is None:
            return None
        if type(cmd) != type([]):
            cmd = [cmd]
        if self.cmd_stack != []:
            self.cmd_index += 1
        self.cmd_stack.extend(cmd)
