#!/usr/bin/python
from bash import *

# Subclass OutHandler in order to supress print statements.
class SshErrHandler(OutHandler):
    def finish(self, output, retcode, frame):
        return -1

# Only need one instance of our new error handler
ssh_err = SshErrHandler()

# List of servers with '.cs.berkeley.edu' appended
servers = ['torus', 'quasar', 'rhombus', 'NOTASERVER', 'star', 'nova']
servers = map(lambda x: x + '.cs.berkeley.edu', servers)

best_server = (None, -1) # (Server Name, Number of Users)

for server in servers:
    # Create the PipeSegment
    cmd = "ssh cs164-bg@%s who | wc -l | tr -d ' '" % server
    ps = PipeSegment(cmd)

    # Attach our new error handler
    cmds = ps.getCommands()
    cmds[0].attachHandler(ssh_err, "err")

    # Execute the pipeline
    count = ps.execute()
    
    # Print status
    print "\n" + "Server:", server
    print "Status:",

    if count != -1: # Server query successful
        print count
        if best_server[1] == -1:
            # First server successfully contacted
            best_server = (server, count)
        elif count < best_server[1]:
            # Better server found
            best_server = (server, count)
    else: # Server query failed
        print "Unable to reach server.\n"

    print "-" * 10

# Print summary
print "SUMMARY\n"

if best_server[0] is None:
    print "Unable to reach any servers."
else:
    print "Best Server:", best_server[0]
    print "Status:", best_server[1]
