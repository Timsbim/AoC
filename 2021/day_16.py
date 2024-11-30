# Day 16
from pprint import pprint
from math import prod
from operator import gt, lt, eq


DAY = 16
EXAMPLE = False


# Preparation
file_name = f"2021/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Reading input
with open(file_name, "r") as file:
    msg = file.read().strip()


# Helper functions

encoding = {
    s: f"{bin(i)[2:]:0>4}"
    for i, s in enumerate("0123456789ABCDEF")
}


def hex_to_bits(hex_string):
    return "".join(encoding[c] for c in hex_string)


# Part 1
print("\nPart 1:")


def decode_flat(bits):
    if len(bits) == 0:
        return []
    packet = {
        "version": int("0b" + bits[0:3], 2),
        "type_id": int("0b" + bits[3:6], 2)
    }
    bits = bits[6:]
    if packet["type_id"] == 4:
        number = ""
        while True:
            block = bits[0:5]
            bits = bits[5:]
            number += block[1:5]
            if block[0] == "0":
                break
        packet["value"] = int("0b" + number, 2)
        if bits.count("0") == len(bits):
            bits = ""
    else:
        len_type_id = int(bits[0])
        bits = bits[1:]
        if len_type_id == 0:
            packet["ttl_len"] = int("0b" + bits[:15], 2)
            bits = bits[15:]
        else:
            packet["num_subs"] = int("0b" + bits[:11], 2)
            bits = bits[11:]
    packets = [packet] + decode_flat(bits)
    return packets


bits = hex_to_bits(msg)
packets = decode_flat(bits)
print(f"Version-sum: {sum(packet['version'] for packet in packets)}")

# 955


# Part 2
print("\nPart 2:")


def decode_nested(bits):
    packets = []
    counted = []
    counting = new_counting = 0
    while bits:
        packet = {}
        packet["ID"] = int("0b" + bits[3:6], 2)
        bits = bits[6:]
        if packet["ID"] == 4:
            number = ""
            while True:
                block = bits[0:5]
                bits = bits[5:]
                number += block[1:5]
                if block[0] == "0":
                    break
            packet["value"] = int("0b" + number, 2)
        else:
            len_type_id = int(bits[0])
            bits = bits[1:]
            if len_type_id == 0:
                ttl_len = int(bits[:15], 2)
                bits = bits[15:]
                packet["packets"] = decode_nested(bits[:ttl_len])
                bits = bits[ttl_len:]
            else:
                num_subs = int(bits[:11], 2)
                bits = bits[11:]
                packet["packets"] = []
                new_packets = packet["packets"]
                new_counting = num_subs
        packets.append(packet)
        if counting:
            counting -= 1
            if not counting:
                packets, counting = counted.pop()
        if new_counting:
            counted.append((packets, counting))
            packets, counting = new_packets, new_counting
            new_counting = 0
        if bits.count("0") == len(bits):
            bits = ""

    return packets


agg_funcs = {0: sum, 1: prod, 2: min, 3: max, 5: gt, 6: lt, 7: eq}


def agg(packets):
    ID = packets["ID"]
    if ID == 4:
        return packets["value"]
    func = agg_funcs[ID]
    if ID < 4:
        return func(agg(packet) for packet in packets["packets"])
    if ID > 4:
        return int(
            func(*(agg(packet) for packet in packets["packets"]))
        )


bits = hex_to_bits(msg)
packets = decode_nested(bits)[0]
print(f"Evaluation: {agg(packets)}")

# 1581_3542_3448
