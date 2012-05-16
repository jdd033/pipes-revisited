import sys

class Handler:
    """
    Base class for all handlers. Does nothing until subclassed.
    """
    def __init__(self):
        pass
    
    def run(self, input, retcode, frame):
        """
        Default behavior is to call action first to do whatever actions
        the user specifies in a custom handler, then finish to determine
        the next step (call next command, exit, etc...).
        
        Override this method to define custom behavior for a handler.  
        """
        out = self.action(input, retcode, frame)
        return self.finish(out, retcode, frame)
    
    def action(self, input, retcode, frame):
        print "You need to override this method to do anything useful."
    
    def finish(self, output, retcode, frame):
        print "You need to override this method to do anything useful."


class OutHandler(Handler):
    """
    Basic handler attached to a command to call the next command in the
    pipe. Subclass this and override the action method to create custom
    output handlers for your needs.
    """
    def __init__(self):
        """ Set the type of the handler """
        self.type = "out"
    
    def action(self, input, retcode, frame):
        """
        Does nothing but pass the stdout of the command into self.finish()
        """
        # print "stdout: {0}".format(input[0])
        return input[0]
    
    def finish(self, output, retcode, frame):
        """
        Flow control:
            If there are more handlers to be run, call the next handler
            Else if there is a next command, call next command with this output
            Otherwise, return the output.
        """ 
        if frame.hasHandler():
            handler = frame.nextHandler()
            return handler.run(output, retcode, frame)
        elif frame.hasCommand():
            cmd = frame.nextCommand()
            return cmd.execute(output, frame)
        else:
            return output


class ErrHandler(Handler):
    """
    Basic error handler attached to a command to define behavior in the
    case of an error occuring. Default behavior is to print the error and
    then exit the pipe. Subclass this and override action to define custom
    error handling behavior, and override finish if you don't want to exit
    upon error.
    """
    def __init__(self):
        """ Set the type of the handler """
        self.type = "err"
    
    def action(self, input, retcode, frame):
        """
        Print an error message with the command that errored, then print
        the stderr stream of the command. 
        """
        cmd = frame.currentCommand()
        print >> sys.stderr, "Error encountered in Command: {cmd}\n".format(cmd=" ".join(cmd.cmd))
        print >> sys.stderr, input[1]
        print >> sys.stderr, "exit code: {0}".format(retcode)
        return None
    
    def finish(self, output, retcode, frame):
        """
        Exit the pipe
        """
        sys.exit(retcode)
