#!/usr/bin/python
from bash import *


class RedirectHandler(OutHandler):
    """
    Redirect stdout to a file and also pass on the output to the next command
    if there is one. This is intended to take the place of the > operator in 
    the shell since Popen does not support output redirection.
    """
    def __init__(self, outfile="stdout", errfile="stderr", redirect_err=False):
        """
        Sets the file to write stdout and stderr to and set a flag to indicate
        whether stderr should also be redirected into a file.
        """
        OutHandler.__init__(self)
        self.outfile = outfile
        self.errfile = errfile
        self.redirect_err = redirect_err
    
    def action(self, input, retcode, frame):
        """
        Write stdout into the file given in __init__()
        If self.redirect_err is True, write stderr to file as well.
        """
        stdout, stderr = input
        
        with open(self.outfile, 'w') as f:
            f.write(stdout)
            
        if self.redirect_err:
            with open(self.errfile, 'w') as f:
                f.write(stderr)
        
        return stdout
       

class SuppressErrorHandler(ErrHandler):
    """
    Suppresses any output that is printed to the console.
    """
    def action(self, input, retcode, frame):
        return None
    

ps = PipeSegment()
h1 = RedirectHandler("ls-output", "ls-error", redirect_err=True)
h2 = RedirectHandler("wc-output", "wc-error", redirect_err=True)

ps.addCmd("ls -l", h1, h1)
ps.addCmd("wc -x", h2, h2)

ps.execute()
