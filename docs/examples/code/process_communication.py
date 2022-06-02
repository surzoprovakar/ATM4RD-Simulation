"""
Process communication example

Covers:

- Resources: Store

Scenario:
  This example shows how to interconnect simulation model elements
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

  Finally, using pipes can simplify how processes are interconnected to
  each other in a simulation model.

Example By:
  Keith Smith

"""
import random
import time
import os

import simpy


RANDOM_SEED = 42
SIM_TIME = 1500

last_requester = ""
last_req_value = "" 


class BroadcastPipe(object):
    """A Broadcast pipe that allows one process to send messages to many.

    This construct is useful when message consumers are running at
    different rates than message generators and provides an event
    buffering to the consuming processes.

    The parameters are used to create a new
    :class:`~simpy.resources.store.Store` instance each time
    :meth:`get_output_conn()` is called.

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

    def get_output_conn(self):
        """Get a new output connection for this broadcast pipe.

        The return value is a :class:`~simpy.resources.store.Store`.

        """
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe


def file_generator():
    if os.path.exists('Replica A.txt') == False:
        fA = open("Replica A.txt", "a")
    else:
        os.remove('Replica A.txt')
        fA = open("Replica A.txt", "a")

    if os.path.exists('Replica B.txt') == False:
        fB = open("Replica B.txt", "a")
    else:
        os.remove('Replica B.txt')
        fB = open("Replica B.txt", "a")

    if os.path.exists('Replica C.txt') == False:
        fC = open("Replica C.txt", "a")
    else:
        os.remove('Replica C.txt')
        fC = open("Replica C.txt", "a")

    if os.path.exists('Replica D.txt') == False:
        fD = open("Replica D.txt", "a")
    else:
        os.remove('Replica D.txt')
        fD = open("Replica D.txt", "a")
    
    return fA, fB, fC, fD


def SLA(trust, delta):
    decision = ""
    updated_trust = 0.0
    if trust >= 0.9:
        # Very Trusty
        if delta <= 20: # and time_freq <= 20:
            decision = "Accepted"
            # Max trust value is 1.0
            if trust < 1.0:
                updated_trust = trust + 0.1
                if updated_trust > 1:
                    updated_trust = 1.0
            else:
                updated_trust = trust 
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.6 and trust < 0.9:
        # Medium Trusty
        if delta <= 15: # and time_freq <= 18:
            decision = "Accepted"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust >= 0.5 and trust < 0.6:
        # Low Trusty
        if delta <= 10: # and time_freq <= 12:
            decision = "Accepted"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    elif trust < 0.5 and trust >= 0.25:
        # Less Untrustworthy
        if delta <= 7: # and time_freq <= 0.8:
            decision = "Ignored"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            updated_trust = trust - 0.1
    else:
        # Very Untrustworthy
        if delta <= 3: # and time_freq <= 5:
            decision = "Ignored"
            updated_trust = trust + 0.1
        else:
            decision = "Ignored"
            if trust > 0.0:
                # Min trust value is 0.0
                updated_trust = trust - 0.1
            else:
                updated_trust = trust
    
    return decision, updated_trust

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

        val = random.randint(1, 15)
    
        msg = (env.now, '%s sends %d at time %d' % (name, val, env.now))
        out_pipe.put(msg)


def message_consumer(name, env, in_pipe, value, trust_dict, fileName):
    """A process which consumes messages."""
    global last_requester, last_req_value
    while True:
        # Get event for message pipe
        msg = yield in_pipe.get()

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
        split = msg[1].split(" ")

        requester = split[1]
        req_value = split[3]
        # req_time = split[6]
        last_requester = requester
        last_req_value = req_value
        if (name[8] != requester):
            # delta = abs(int(req_value) - value)
            # trust = trust_dict[requester]

            # decision = ""

            # if delta <= 10 and trust >= 0.5 and (env.now - int(req_time)) <= 15:
            #     decision = "Accepted"
            #     value = int(req_value)
            #     trust_dict[requester] += 0.1
            # else:
            #     decision = "Ignored"
            #     trust_dict[requester] -= 0.1

            trust = trust_dict[requester]
            delta = abs(int(req_value) - value)
            # time_freq = env.now - int(req_time)

            decision, up_trust = SLA(trust, delta) 
            trust_dict[requester] = up_trust
            if decision == "Accepted":
                value = int(req_value)

            print('%s| Current Trust %f' %(msg[1], trust))
            print('%s received message at time %d' %(name, env.now))
            print('Delta %d| Decision %s| Updated Trust %f' %(delta, decision, trust_dict[requester]))
            print(trust_dict)
            print('Final Value %s' %(value))
            print('\n')

            fileName.write('%s| Current Trust %f\n' %(msg[1], trust))
            fileName.write('%s received message at time %d\n' %(name, env.now))
            fileName.write('Delta %d| Decision %s| Updated Trust %f\n' %(delta, decision, trust_dict[requester]))
            fileName.write('%s\n' %(trust_dict))
            fileName.write('Final Value = %s\n' %(value))
            fileName.write('\n')
        #else:
            # print('Self Generated Value = %s\n' %(req_value))
            # print('\n')
            # fileName.write('Self Generated Value = %s\n' %(req_value))
            # fileName.write('\n')


        time.sleep(0.5)
        # Process does some other work, which may result in missing messages
        # yield env.timeout(random.randint(4, 8))
        yield env.timeout(3)


# Setup and start the simulation

# Generate Replica Output files
fA, fB, fC, fD = file_generator()

print('\nProcess communication\n')
# random.seed(RANDOM_SEED)
# env = simpy.Environment()

# # For one-to-one or many-to-one type pipes, use Store
# pipe = simpy.Store(env)
# env.process(message_generator('Generator A', env, pipe))
# env.process(message_consumer('Consumer A', env, pipe))

# print('\nOne-to-one pipe communication\n')
# env.run(until=SIM_TIME)

# For one-to many use BroadcastPipe
# (Note: could also be used for one-to-one,many-to-one or many-to-many)
env = simpy.Environment()
bc_pipe = BroadcastPipe(env)

env.process(message_generator('Replica A', env, bc_pipe))
env.process(message_generator('Replica B', env, bc_pipe))
env.process(message_generator('Replica C', env, bc_pipe))
env.process(message_generator('Replica D', env, bc_pipe))

env.process(message_consumer('Replica A', env, bc_pipe.get_output_conn(), 0, {'B' : 0.5, 'C' : 0.5, 'D' : 0.5}, fA))
env.process(message_consumer('Replica B', env, bc_pipe.get_output_conn(), 0, {'A' : 0.5, 'C' : 0.5, 'D' : 0.5}, fB))
env.process(message_consumer('Replica C', env, bc_pipe.get_output_conn(), 0, {'A' : 0.5, 'B' : 0.5, 'D' : 0.5}, fC))
env.process(message_consumer('Replica D', env, bc_pipe.get_output_conn(), 0, {'A' : 0.5, 'B' : 0.5, 'C' : 0.5}, fD))

# print('\nOne-to-many pipe communication\n')
env.run(until=SIM_TIME)


if last_requester == "A":
    fA.write('Self Generated Value = %s\n' %(last_req_value))
elif last_requester == "B":
    fB.write('Self Generated Value = %s\n' %(last_req_value))
elif last_requester == "C":
    fC.write('Self Generated Value = %s\n' %(last_req_value))
else:
    fD.write('Self Generated Value = %s\n' %(last_req_value))