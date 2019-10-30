
import types

from pivy_trackers.trait.publisher import Publisher
from pivy_trackers.trait.subscriber import Subscriber

MESSAGES = [1, 2, 4, 8]

def create_message(message_type, data, sender):
    """
    Generate a SimpleNameSpace object for messaging
    """

    _result = types.SimpleNamespace()

    _result.message_type = message_type
    _result.data = data
    _result.sender = sender

    return _result

class MyPublisher(Publisher):

    def __init__(self):
        """
        Constructor
        """

        super().__init__()

class MySubscriber(Subscriber):

    def __init__(self):
        """
        Constructor
        """

        super().__init__()

    def notify(self, event_type, message, verbose=True):
        """
        Notify callback
        """

        super().notify(event_type, message, verbose)

my_pub = MyPublisher()
my_subs = []

for _i in range(0, 7):
    my_subs.append(MySubscriber())

for _i in range(0, 4):
    my_pub.register(my_subs[_i], MESSAGES[_i])

my_pub.register(my_subs[4], [MESSAGES[0], MESSAGES[2]])
my_pub.register(my_subs[5], [MESSAGES[1], MESSAGES[2], MESSAGES[3]])

my_pub.register(
    my_subs[6], [MESSAGES[0], MESSAGES[1], MESSAGES[2], MESSAGES[3]]
)

test_messages = [
    MESSAGES[0],
    MESSAGES[1],
    [MESSAGES[0], MESSAGES[3]]
]

for _msg in test_messages:
    data = 'TEST_MESSAGE_' + str(_msg)
    my_pub.dispatch(create_message(_msg, data, my_pub), _msg, True)
