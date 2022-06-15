"""
Process communication example

Covers:

- Resources: Store

Scenario:
  This example shows how to interconnAect simulation model elements
  together using :class:`~simpy.resources.store.Store` for one-to-one,
  and many-to-one asynchronous processes. For one-to-many a simple
  BroadCastPipe class is constructed from Store.

When Useful:
  When a consumer process does not always wait on a generating process
  and these processes run asynchronously. This example shows how to
  create a buffer and also tell is the consumer process was late
  yielding to the event from a generating process.

  This is also useful when some information needs to be broadcast to
  many receiving processes

  Finally, using pipes can simplify how processes are interconnAected to
  each other in a simulation model.

Example By:
  Keith Smith

"""
import random
import time

from cairo import Region
from helper_methods import *
from sla_script import *

import simpy

mode = 0
RANDOM_SEED = 42
SIM_TIME = 300



class BroadcastPipe(object):
    """A Broadcast pipe that allows one process to send messages to many.

    This construct is useful when message consumers are running at
    different rates than message generators and provides an event
    buffering to the consuming processes.

    The parameters are used to create a new
    :class:`~simpy.resources.store.Store` instance each time
    :meth:`get_output_connA()` is called.

    """
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []

    def put(self, value):
        """Broadcast a *value* to all receivers."""
        if not self.pipes:
            raise RuntimeError('There are no output pipes.')
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)  # Condition event for all "events"

    def get_output_connA(self):
        """Get a new output connAection for this broadcast pipe.

        The return value is a :class:`~simpy.resources.store.Store`.

        """
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe


def message_generator(name, env, out_pipe):
    """A process which randomly generates messages."""
    while True:
        # wait for next transmission
        # yield env.timeout(random.randint(6, 10))
        yield env.timeout(2)

        # messages are time stamped to later check if the consumer was
        # late getting them.  Note, using event.triggered to do this may
        # result in failure due to FIFO nature of simulation yields.
        # (i.e. if at the same env.now, message_generator puts a message
        # in the pipe first and then message_consumer gets from pipe,
        # the event.triggered will be True in the other order it will be
        # False
        
        opt = ""
        toss = random.randint(0, 3)
        val = random.randint(1, 15)
        
        if toss == 0:
            opt = "Dec"
        else:
            opt = "Inc"

        msg = (env.now, '%s sends %d at time %d as %s' % (name, val, env.now, opt))
        out_pipe.put(msg)


def message_consumer(name, env, in_pipe, value, trust_dict, c, conn):
    """A process which consumes messages."""
    
    while True:
        # Get event for message pipe
        msg = yield in_pipe.get()

        #region Comment
        # if msg[0] < env.now:
        #     # if message was already put into pipe, then
        #     # message_consumer was late getting to it. Depending on what
        #     # is being modeled this, may, or may not have some
        #     # significance
        #     print('LATE Getting Message: at time %d: %s received message: %s' %
        #           (env.now, name, msg[1]))

        # else:
        #     # message_consumer is synchronized with message_generator
        #     print('at time %d: %s received message: %s.' %
        #           (env.now, name, msg[1]))
        #endregion

        split = msg[1].split(" ")
        current_value = value
        requester = split[1]
        req_value = split[3]
        req_time = split[6]
        opt_type = split[8]
        receive_time = env.now
        

        if mode == 1:
            # Simulation with trust
            trust = trust_dict[requester]
            req_trust = trust
            # delta = abs(int(req_value) - value)
            # time_freq = env.now - int(req_time)

            # decision, up_trust = SLA_Old(float(trust), delta) 
            decision, up_trust = sla(trust, int(req_value)) 

            
            if decision == "Accepted":
                if opt_type == "Inc":
                    value += int(req_value)
                else:
                    if value >= int(req_value):
                        value -= int(req_value)
                    else:
                        decision = "Ignored"
                        up_trust -= 10

            trust_dict[requester] = up_trust

            print('%s| Current Trust %f' %(msg[1], trust))
            print('%s received message at time %d' %(name, env.now))
            print('Type %s| Decision %s| Updated Trust %f' %(opt_type, decision, trust_dict[requester]))
            print(trust_dict)
            print('Final Value %s' %(value))
            print('\n')

            db_insert(c, conn, requester, current_value, req_value, opt_type,
            req_trust, up_trust, req_time, receive_time, decision, value)
        else:
            # Simulation without trust
            if opt_type == "Inc":
                value += int(req_value)
            else:
                if value >= int(req_value):
                    value -= int(req_value)
            decision = "Accepted"
            
            print('%s received message at time %d' %(name, env.now))
            print('Merged Value %s' %(value))
            print('\n')

            db_insert(c, conn, requester, current_value, req_value, opt_type,
            "", "", req_time, receive_time, decision, value)

            # region txt file
            # fileName.write('%s| Current Trust %f\n' %(msg[1], trust))
            # fileName.write('%s received message at time %d\n' %(name, env.now))
            # fileName.write('Delta %d| Decision %s| Updated Trust %f\n' %(delta, decision, trust_dict[requester]))
            # fileName.write('%s\n' %(trust_dict))
            # fileName.write('Final Value = %s\n' %(value))
            # fileName.write('\n')
        #else:
            # print('Self Generated Value = %s\n' %(req_value))
            # print('\n')
            # fileName.write('Self Generated Value = %s\n' %(req_value))
            # fileName.write('\n')
            #endregion


        time.sleep(0.5)
        # Process does some other work, which may result in missing messages
        # yield env.timeout(random.randint(4, 8))
        yield env.timeout(3)


# Setup and start the simulation

# Generate Replica Output files
# fA, fB, fC, fD = file_generator()
cA, connA, cB, connB, cC, connC, cD, connD = db_generatoor()

print('\nProcess communication\n')
random.seed(RANDOM_SEED)

# region One to One communication
# env = simpy.Environment()

# # For one-to-one or many-to-one type pipes, use Store
# pipe = simpy.Store(env)
# env.process(message_generator('Generator A', env, pipe))
# env.process(message_consumer('Consumer A', env, pipe))

# print('\nOne-to-one pipe communication\n')
# env.run(until=SIM_TIME)

# For one-to many use BroadcastPipe
# (Note: could also be used for one-to-one,many-to-one or many-to-many)
#endregion

env = simpy.Environment()
bc_pipe = BroadcastPipe(env)

env.process(message_generator('Replica A', env, bc_pipe))
env.process(message_generator('Replica B', env, bc_pipe))
env.process(message_generator('Replica C', env, bc_pipe))
env.process(message_generator('Replica D', env, bc_pipe))

env.process(message_consumer('Replica A', env, bc_pipe.get_output_connA(), 0, {'A' : 50, 'B' : 50, 'C' : 50, 'D' : 50}, cA, connA))
env.process(message_consumer('Replica B', env, bc_pipe.get_output_connA(), 0, {'A' : 50, 'B' : 50, 'C' : 50, 'D' : 50}, cB, connB))
env.process(message_consumer('Replica C', env, bc_pipe.get_output_connA(), 0, {'A' : 50, 'B' : 50, 'C' : 50, 'D' : 50}, cC, connC))
env.process(message_consumer('Replica D', env, bc_pipe.get_output_connA(), 0, {'A' : 50, 'B' : 50, 'C' : 50, 'D' : 50}, cD, connD))

# print('\nOne-to-many pipe communication\n')
env.run(until=SIM_TIME)

