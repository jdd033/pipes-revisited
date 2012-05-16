import shlex
from handlers import *
from frame import *
from subprocess import Popen, PIPE

class Command:
    """
    Wrapper class for a bash command. User defined handlers may be attached to
    each command. A command can be reused by different PipeSegment instances. 
    """
    # Set up the default OutHandler and ErrHandler
    default_OutHandler = OutHandler()
    default_ErrHandler = ErrHandler()
    
    def __init__(self, cmd):
        """
        Takes in a bash command in string format and tokenizes it with shlex.
        Example: 
            Command("ls -l") -> self.cmd = ['ls', '-l']
        """
        self.cmd = shlex.split(cmd)
        self.out_handlers = []
        self.err_handlers = []
        
        # If the user enters an empty string as a command, either by itself or
        # in a pipe, print error message and exit.
        if self.cmd == []:
            print "Illegal command: You've entered an empty command somewhere"
            sys.exit(1)
  
    def execute(self, input=None, frame=None):
        """
        Execute the command with subprocess and capture output, then call the
        output handler if exit code was zero and the error handler if the exit
        code was non-zero.
        """
        if frame is None:
            frame = Frame()
            frame.addCommand(self)

        try:
            p = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            result = p.communicate(input)
            retcode = p.returncode
        except OSError:
            result = ("", "Invalid command: {cmd}".format(cmd=" ".join(self.cmd)))
            retcode = 1
        
        if retcode != 0:
            handlers = self.err_handlers
            default_handler = Command.default_ErrHandler
        else: # return code is 0
            handlers = self.out_handlers
            default_handler = Command.default_OutHandler

        # Call the first handler in the list
        if handlers:
            frame.addHandler(handlers)
            return handlers[0].run(result, retcode, frame)
        else:
            frame.addHandler(default_handler)
            return default_handler.run(result, retcode, frame)

    def attachHandler(self, handler, handler_type='out', index=None):
        """
        Adds a handler or list of handlers to the command represented by this
        object. The handler can be an output handler or an error handler. If 
        the optional parameter index is specified, insert the handler or the
        list of handlers into the command handlers at that index position.
        """
        if handler_type == "out":
            handlers = self.out_handlers
        else:
            handlers = self.err_handlers

        index = len(handlers) if index is None else index
        
        if type(handler) == type([]):
            handler = list(handler)
            handler.reverse()
        else:
            handler = [handler]
        map(lambda x: handlers.insert(index, x), handler)

