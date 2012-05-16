import subprocess
from bash import *

class PrintCmdHandler(OutHandler):
    def action(self, input, returncode, frame):
        cmd = " ".join(frame.currentCommand().cmd)
        print "PrintCmdHandler:", cmd
        return cmd 

class DoublePrintCmdHandler(OutHandler):
    def action(self, input, returncode, frame):
        cmd = " ".join(frame.currentCommand().cmd)
        print "DoublePrintCmdHandler:", cmd, cmd
        return cmd 

class FixedOutputHandler(OutHandler):
    def action(self, input, returncode, frame):
        print "FixedOutputHandler:", "This text will never change."
        return "This text will never change." 

class CallAgainHandler(OutHandler):
    def finish(self, output, returncode, frame):
        print "CallAgainHandler:", "Calling the PipeSegment again"
        frame.state['ps'].execute(output, frame)

class GoToOutHandler(ErrHandler):
    def action(self, input, returncode, frame):
        print "Error encountered. Executing output handlers."
        return None

    def finish(self, output, returncode, frame):
        frame.currentCommand().out_handlers[0].run(output, returncode, frame)
        return None

def debug_info(e, a):
    if e == a:
        print "Test passed.\n"
    else:
        print "Test failed.\n"
        print "Expected:"
        print e
        print "Actual:"
        print a + "\n"

if __name__ == '__main__':
    print "***Testing Command with just a command***\n"
  
    cmd = "ls -l"
    print "Command:", cmd
    c = Command(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = c.execute()
    debug_info(output, result)

    cmd = "grep print handlers.py"
    print "Command:", cmd
    c = Command(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = c.execute()
    debug_info(output, result)
    
    print "***Testing Command with a handler***\n"
 
    cmd = "ls -l"
    print "Command:", cmd
    c = Command(cmd)
    h = PrintCmdHandler()
    c.attachHandler(h)
    output = " ".join(c.cmd)
    result = c.execute()
    debug_info(output, result)
  
    print "***Testing PipeSegment with single commands***\n"
    
    cmd = "ls -l"
    print "Command:", cmd
    ps = PipeSegment(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = ps.execute()
    debug_info(output, result)
  
    cmd = "ls -a .."
    print "Command:", cmd
    ps = PipeSegment(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = ps.execute()
    debug_info(output, result)
  
    print "***Testing PipeSegment with single commands with multiple handlers***\n"

    cmd = "ls -l"
    print "Command:", cmd
    ps = PipeSegment()
    h1 = PrintCmdHandler()
    h2 = FixedOutputHandler()
    ps.addCmd(cmd, [h1, h2])
    output = "This text will never change."
    result = ps.execute()
    debug_info(output, result)
 
    print "***Testing PipeSegment with piped commands***\n"
    
    cmd = "ls -l | wc -l"
    print "Command:", cmd
    ps = PipeSegment(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = ps.execute()
    debug_info(output, result)

    cmd = "cat bash.py | sort | wc -m"
    print "Command:", cmd
    ps = PipeSegment(cmd)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    result = ps.execute()
    debug_info(output, result)

    print "***Testing PipeSegment with piped commands with multiple handlers***\n"
    
    cmd = "cat bash.py | sort | wc -m"
    print "Command:", cmd
    ps = PipeSegment(cmd)
    h1 = PrintCmdHandler()
    h2 = DoublePrintCmdHandler()
    h3 = FixedOutputHandler()
    ps.cmds[0].attachHandler([h1, h2])
    ps.cmds[1].attachHandler([h1, h2])
    ps.cmds[2].attachHandler([h1, h2, h3])
    output = "This text will never change."
    result = ps.execute()
    debug_info(output, result)

    cmd = "ls -l | wc -l"
    print "Command:", cmd
    ps = PipeSegment(cmd)
    h1 = PrintCmdHandler()
    h2 = DoublePrintCmdHandler()
    h3 = FixedOutputHandler()
    h4 = GoToOutHandler()
    ps.cmds[0].attachHandler([h1])
    ps.cmds[0].attachHandler([h4], "err")
    ps.cmds[1].attachHandler([h2, h3])
    ps.cmds[1].attachHandler(h4, "err")
    output = "This text will never change." 
    result = ps.execute()
    debug_info(output, result)
 
    """
    print "***Testing PipeSegment with piped commands with multiple handlers and testing state***\n"
    
    # Warning this will cause infinite recursion
    cmd = "ls -l | wc -l"
    print "Command:", cmd
    f = Frame()
    ps = PipeSegment(cmd)
    f.state = {'ps':ps}
    h1 = PrintCmdHandler()
    h2 = CallAgainHandler()
    ps.cmds[0].attachHandler([h1])
    ps.cmds[1].attachHandler([h1, h2])
    ps.execute(frame=f)
    """
   
    
    