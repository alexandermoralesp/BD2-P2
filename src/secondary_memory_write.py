"""
Secondary Memory Write

Description:
------------

"""



class Block:
    def __init__(self, term : str, values: []) -> None:
        self.term = term
        self.values = values
        self.next = -1
    def write(self, output_filename):
        file = open(output_filename, "wb")


class Hash:
    def __init__(self) -> None:
        self.dictionary = {"": []}
        self.sorted = []

    def add(self, token: str, value: int):
        if token not in self.dictionary:
            self.dictionary[token] = [value]
        else:
            self.dictionary[token].append(value)

    def remove(self, token, value):
        if token not in self.dictionary:
            return
        else:
            self.dictionary[token].remove(value)

    def sorted(self):
        self.sorted = sorted(self.dictionary)

    def write_block_to_disk(self, output_filename):
        for (key, values) in self.dictionary.items():
            block = Block(key=key, values=values)
            block.write(output_filename=output_filename)

def spimi_invert(inverted_index):
    outputfile = open("newfile.bin", "wb")
    dictionary = Hash()
    for (token, value) in inverted_index:
        dictionary.add(token=token, value=value)
    dictionary.sorted()
    dictionary.write_block_to_disk()
    return outputfile


if __name__ == "__main__":
    print("Secondary Memory Write")

    L = 5
    inverted_index = [
        ("data1.txt", 12),
        ("data2.txt", 13),
        ("data3.txt", 14),
        ("data4.txt", 15),
        ("data5.txt", 16)
    ]
    print(len(inverted_index))
    document = [
        ("w1id", 1),
        ("w2id", 2),
        ("w2id", 1),
    ]
    document = [
        ("W1ID", [1, 3]),
        ("W2ID", [1, 2, 3]),
        ("W3ID", [4]),
        ("W1ID", [1, 3]),
        ("W2ID", [1, 2, 3]),
        ("W3ID", [4]),
        ("W1ID", [1, 3]),
        ("W2ID", [1, 2, 3]),
        ("W3ID", [4]),
        ("W1ID", [1, 3]),
        ("W2ID", [1, 2, 3]),
        ("W3ID", [4]),
    ]

    # write to disk
