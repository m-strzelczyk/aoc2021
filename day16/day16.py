# https://adventofcode.com/2021/day/16
from dataclasses import dataclass


@dataclass
class ValuePacket:
    version: int
    type: int
    value: int

    def eval(self):
        return self.value


@dataclass
class OpPacket:
    version: int
    type: int
    subpackets: list

    def eval(self):
        if self.type == 0:
            s = 0
            for subpack in self.subpackets:
                s += subpack.eval()
            return s
        elif self.type == 1:
            p = 1
            for subpack in self.subpackets:
                p *= subpack.eval()
            return p
        elif self.type == 2:
            return min(subpack.eval() for subpack in self.subpackets)
        elif self.type == 3:
            return max(subpack.eval() for subpack in self.subpackets)
        elif self.type == 5:
            return int(self.subpackets[0].eval() > self.subpackets[1].eval())
        elif self.type == 6:
            return int(self.subpackets[0].eval() < self.subpackets[1].eval())
        elif self.type == 7:
            return int(self.subpackets[0].eval() == self.subpackets[1].eval())


def parse_literal(inpt: str) -> (int, str):
    i = 0
    val = []
    while True:
        end, *hex_val = inpt[5*i:5*(i+1)]
        val.append("".join(hex_val))
        i += 1
        if end == '0':
            break
    val = int("".join(val), 2)
    # print(f"Got literal {inpt[:i*5]}, decoded to: {val}")
    return val, inpt[i*5:]


def parse(inpt: str):
    version, typ = inpt[0:3], inpt[3:6]
    if typ == '100':
        literal_value, inpt = parse_literal(inpt[6:])
        return ValuePacket(version=int(version, 2), type=int(typ, 2), value=literal_value), inpt
    else:
        length_type = inpt[6]
        if length_type == "1":
            # next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
            packet_count = int(inpt[7:18], 2)
            packet = OpPacket(version=int(version, 2), type=int(typ, 2), subpackets=[])
            inpt = inpt[18:]
            # print(f"Processing {packet_count }subpacks: {inpt}")
            for _ in range(packet_count):
                subpacket, inpt = parse(inpt)
                packet.subpackets.append(subpacket)
            return packet, inpt
        else:
            # next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            subpack_len = int(inpt[7:22], 2)
            packet = OpPacket(version=int(version, 2), type=int(typ, 2), subpackets=[])
            sub_inpt = inpt[22:22+subpack_len]
            # print(f"Processing subpacks with length {subpack_len}: {sub_inpt}")
            while sub_inpt:
                subpacket, sub_inpt = parse(sub_inpt)
                packet.subpackets.append(subpacket)
            return packet, inpt[22+subpack_len:]


def pack_print(packet, indent=0):
    if isinstance(packet, ValuePacket):
        print(" "*indent + f"value: {packet.value}")
    elif isinstance(packet, OpPacket):
        print(" "*indent + f"operation: {packet.version} {packet.type}")
        for subp in packet.subpackets:
            pack_print(subp, indent+2)


def sum_versions(packet):
    if isinstance(packet, ValuePacket):
        return packet.version
    ret = packet.version
    for subpacket in packet.subpackets:
        ret += sum_versions(subpacket)
    return ret


def p1(inpt: str) -> int:
    packet, rest = parse(inpt)
    return sum_versions(packet)


def p2(inpt: str) -> int:
    packet, rest = parse(inpt)
    return packet.eval()


if __name__ == "__main__":
    with open('input.txt') as infile:
        data = infile.read()
    bin_inpt = bin(int(data, 16))[2:]
    bin_inpt = "0" * ((4 - (len(bin_inpt) % 4)) % 4) + bin_inpt
    # print(f"Binary: {bin_inpt}, length: {len(bin_inpt)}")
    print("P1:", p1(bin_inpt))
    print("P2:", p2(bin_inpt))
