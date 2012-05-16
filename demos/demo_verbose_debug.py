#!/usr/bin/python
from bash import *
import sys

# Subclass OutHandler to reuse its flow control.
class VerboseCmdErrHandler(OutHandler):

    # Dump the pipeline history to stderr
    def action(self, input, retcode, frame):
        print >> sys.stderr, "Pipeline\n"
        print >> sys.stderr, "#" * 10

        # Recall the results of each command from the state.
        for index, command in enumerate(frame.cmd_stack):
            if index == len(frame.cmd_stack) - 1:
                break

            print >> sys.stderr,"\nCommand:", command.cmd

            if frame.state is not None:
                out, rc = frame.state[index]
                print >> sys.stderr, "Output:", out
                print >> sys.stderr, "Return Code:", rc

            print >> sys.stderr, ""
            print >> sys.stderr, "#" * 10

        print >> sys.stderr, ""
        return input

class VerboseCmdOutHandler(OutHandler):

    # Record the results of the command in the state.
    def action(self, input, retcode, frame):
        if frame.state is None:
            frame.state = []
        
        frame.state.append((input[0], retcode))
        return input[0]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Enter a command!"
        sys.exit(1)

    # Get command from input.
    cmd = sys.argv[1]

    # Print the pipeline history before the default error handler.
    myEH = [VerboseCmdErrHandler(), ErrHandler()]
    myOH = VerboseCmdOutHandler()

    # Create the PipeSegment and attach the handlers
    ps = PipeSegment(cmd)
    ps.mapHandler(myEH, "err")
    ps.mapHandler(myOH, "out")

    # Execute the pipeline.
    print ps.execute()
