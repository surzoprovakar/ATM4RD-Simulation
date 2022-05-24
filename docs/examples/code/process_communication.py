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

import simpy


RANDOM_SEED = 42
SIM_TIME = 20


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


def message_generator(name, env, out_pipe, trust, prev_val):
    """A process which randomly generates messages."""
    while True:
        # wait for next transmission
        yield env.timeout(random.randint(6, 10))

        # messages are time stamped to later check if the consumer was
        # late getting them.  Note, using event.triggered to do this may
        # result in failure due to FIFO nature of simulation yields.
        # (i.e. if at the same env.now, message_generator puts a message
        # in the pipe first and then message_consumer gets from pipe,
        # the event.triggered will be True in the other order it will be
        # False
        res = ""
        val = random.randint(1, 20)
        delta = val - prev_val
        if abs(delta) <= 10 and trust >= 0.5:
            res = "Accepted"
            trust += 0.1
        else:
            res = "Ignored"
            if trust >= 0.1:
                trust -= 0.1
    
        msg = (env.now, '%s sends %d at time %d: delta = %d trust = %f decision = %s' % (name, val, env.now, delta, trust, res))
        out_pipe.put(msg)

        prev_val = val


def message_consumer(name, env, in_pipe, val):
    """A process which consumes messages."""
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
        val = split[3]
        if (name[8] != split[1]):
            print('%s\n%s received message at time %d: Value %s\n.' %(msg[1], name, env.now, val))
            
            
        
        time.sleep(0.5)
        # Process does some other work, which may result in missing messages
        yield env.timeout(random.randint(4, 8))


# Setup and start the simulation
print('\nProcess communication\n')
random.seed(RANDOM_SEED)
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

env.process(message_generator('Replica A', env, bc_pipe, 0.5, 0))
env.process(message_generator('Replica B', env, bc_pipe, 0.5, 0))
env.process(message_generator('Replica C', env, bc_pipe, 0.5, 0))
env.process(message_generator('Replica D', env, bc_pipe, 0.5, 0))
env.process(message_consumer('Replica A', env, bc_pipe.get_output_conn(), 0))
env.process(message_consumer('Replica B', env, bc_pipe.get_output_conn(), 0))
env.process(message_consumer('Replica C', env, bc_pipe.get_output_conn(), 0))
env.process(message_consumer('Replica D', env, bc_pipe.get_output_conn(), 0))

# print('\nOne-to-many pipe communication\n')
env.run(until=SIM_TIME)
