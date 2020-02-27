import math
import struct


def decode(data):
    messages = []
    return _process_packet(data, -1, messages)


def _process_packet(data, timestamp, messages):
    if data[0] == 35:  # if packet is a bundle ("#" = ASCII 35)
        timetag, contents = _process_bundle(data)
        timestamp = timetag / pow(2, 32)  # convert to seconds since January 1, 1900. See https://en.wikipedia.org/wiki/Network_Time_Protocol#Timestamps
        for content in contents:
            _process_packet(content, timestamp, messages)  # call recursively
    if data[0] == 47:  # if packet is a message ("#" = ASCII 47)
        message = _process_message(data)
        if timestamp != -1:
            message[0] = timestamp
        messages.append(message)
    return messages


def _process_bundle(data):
    timetag = int.from_bytes(data[8:16], byteorder='big')  # timetag is uint64 starting at index 8
    elements = data[16:]  # all remaining bytes are contiguous bundle elements
    contents = []
    while len(elements) > 0:
        size = int.from_bytes(elements[0:4], byteorder='big')  # element size is uint32 starting at index 0
        contents.append(elements[4: (size + 4)])  # follow size number of bytes are OSC contents
        elements = elements[(size + 4):]  # skip to next element
    return timetag, contents


def _process_message(data):
    message = [-1, data[0:data.index(0)].decode("utf-8")]  # timestamp = -1, get address as string up to "\0"
    remaining = data[data.index(44):]  # type tags and arguments start at ","
    type_tags = remaining[0:(remaining.index(0) + 1)].decode("utf-8")  # type tags end at "\0"
    arguments = remaining[(4 * math.ceil(len(type_tags) / 4)):]  # account for trailing "\0" characters
    for type_tag in type_tags:
        if type_tag == ",":  # first character of type tag string
            continue
        elif type_tag == "i":  # argument is uint32
            message.append(int.from_bytes(arguments[0:4], byteorder='big'))
            arguments = arguments[4:]
        elif type_tag == "f":  # argument is float
            float_bytes = bytearray(arguments[0:4])
            float_bytes.reverse()
            message.append(struct.unpack('f', float_bytes)[0])
            arguments = arguments[4:]
        elif type_tag == "\x00":  # last character of type tag string
            continue
        elif type_tag == "s" or type_tag == "S":  # argument is string
            message.append(arguments[0:arguments.index(0)].decode("utf-8"))
            arguments = arguments[(4 * math.ceil((len(message[-1]) + 1) / 4)):]  # account for trailing "\0" characters
        elif type_tag == "b":  # argument is blob
            size = int.from_bytes(arguments[0:4], byteorder='big')
            message.append(arguments[4:(4 + size)])
            arguments = arguments[4 + (4 * math.ceil(size / 4)):]  # account for trailing "\0" characters
        elif type_tag == "T":  # argument is True
            message.append(True)
        elif type_tag == "F":  # argument is False
            message.append(False)
        else:
            print("Argument type not supported.", type_tag)
            break
    return message
