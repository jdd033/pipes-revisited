# Main class for the bash module
from command import *
from frame import *

class PipeSegment:
    
    def __init__(self, cmds=None):
        if type(cmds) == type(''):
            cmds = cmds.split('|')

        #TODO: Check for shlex input

        if cmds is None:
            self.cmds = []
        else:
            self.cmds = map(lambda x: Command(x), cmds)

    def getCommands(self):
        return list(self.cmds)

    def addCmd(self, cmd, out_handlers=None, err_handlers=None):
        #TODO: Check for pipes
        #TODO: Check if handlers are actually handlers
        command = Command(cmd)
        if out_handlers:
            command.attachHandler(out_handlers, "out")
        if err_handlers:
            command.attachHandler(err_handlers, "err")
        self.cmds.append(command)

    def delCmd(self, cmd):
        #TODO: Command name delete.
        if cmd in self.cmds:
            self.cmds.remove(cmd)
        #TODO: Raise proper error if it doesn't exist
        
    def mapHandler(self, handler, handler_type="out"):
        for cmd in self.cmds:
            cmd.attachHandler(handler, handler_type)

    def execute(self, input=None, frame=None):
        if frame is None:
            frame = Frame()

        if self.cmds:
            frame.addCommand(self.cmds)
            return self.cmds[0].execute(input, frame)
        else:
            return input
