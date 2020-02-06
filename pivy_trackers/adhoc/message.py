
from pivy_trackers.trait.message import Message
from pivy_trackers.trait.message_types import MessageTypes
from pivy_trackers.trait.message_data import MessageData

class MyMessager(Message):

    def __init__(self, name):
        """
        Constructor
        """

        super().__init__()
        self.name = name

    def notify(self, event, message):
        """
        Generic notification callback
        """

        super().notify(event, message)

_type_one = MessageTypes.create('MY_FIRST_CUSTOM_MESSAGE')
_type_two = MessageTypes.create('MY_SECOND_CUSTOM_MESSAGE')
_type_three = MessageTypes.create('MY_THIRD_CUSTOM_MESSAGE')

first_messager = MyMessager('first messager')
second_messager = MyMessager('second messager')
third_messager = MyMessager('third messager')
fourth_messager = MyMessager('fourth messager')

#register the second and third messagers with the first.
#use the MessageTypes.CUSTOM object directly
first_messager.register(
    second_messager, MessageTypes.CUSTOM.MY_FIRST_CUSTOM_MESSAGE)

first_messager.register(
    third_messager, MessageTypes.CUSTOM.MY_SECOND_CUSTOM_MESSAGE)

first_messager.register(
    fourth_messager, 
    [
        MessageTypes.CUSTOM.MY_FIRST_CUSTOM_MESSAGE, 
        MessageTypes.CUSTOM.MY_SECOND_CUSTOM_MESSAGE
    ]
)
#create the message data objects.
#use the _type_one and _type_two references to the CUSTOM attributes
first_message = MessageData(first_messager, _type_one, (1,2,3))
second_message = MessageData(first_messager, _type_two, (4,5,6))
third_message = MessageData(first_messager, [_type_one, _type_three], (7,8,9))

#dispatch messages using the MessageData objects
#using the MessageType.CUSTOM references stored in the message data
print('\n\t=====FIRST MESSAGE TEST====\n')
first_messager.dispatch(first_message, first_message.message_type, True)

print('\n\t=====SECOND MESSAGE TEST====\n')
first_messager.dispatch(second_message, second_message.message_type, True)

print('\n\t=====THIRD MESSAGE TEST====\n')
first_messager.dispatch(third_message, third_message.message_type, True)
