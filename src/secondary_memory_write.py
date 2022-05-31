"""
Secondary Memory Write

Description:
------------

"""


class Block:
    def __init__(self, term: str, values: list[int]) -> None:
        self.term = term
        self.values = values
        self.next = -1

    def write(self, output_filename):
        file = open(output_filename, "wb")


class Hash:
    def __init__(self) -> None:
        # self.dictionary = {"": []}
        self.dictionary = {}
        self.sorted_hash = []

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
        self.sorted_hash = sorted(
            self.dictionary.items(), key=lambda kv: (kv[1], kv[0]))

    def write_block_to_disk(self, output_filename):
        file = open(output_filename, "ab")
        if len(self.sorted_hash) == 0:
            return
        for (key, values) in self.sorted_hash:
            file.write(key.encode())
            file.write(" ".encode())
            for i in range(4):
                if i >= len(values):
                    file.write(str("0 ").encode())
                else:
                    file.write(str(f"{values[i]} ").encode())
                
            file.write(b"\n")
        file.close()

    def print_unsorted(self):
        for (key, values) in self.dictionary.items():
            print(key, values)

    def print_sorted(self):
        for (key, value) in self.sorted_hash:
            print(key, value)


def spimi_invert(stream_token):
    outputfile = open("newfile.bin", "wb")
    dictionary = Hash()
    for (token, value) in stream_token:
        dictionary.add(token=token, value=value)
    dictionary.sorted()
    dictionary.write_block_to_disk()
    return outputfile


if __name__ == "__main__":
    print("Secondary Memory Write")
    document = [
        ("b", 5),
        ("b", 6),
        ("b", 7),
        ("a", 1),
        ("a", 2),
        ("a", 3),
        ("a", 4),
    ]
    dictionary = Hash()
    for (token, value) in document:
        dictionary.add(token=token, value=value)
    dictionary.print_unsorted()
    dictionary.sorted()
    print()
    dictionary.print_sorted()
    dictionary.write_block_to_disk("data/information.bin")
