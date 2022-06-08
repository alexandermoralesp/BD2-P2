"""
Secondary Memory Write

Description:
------------

"""

class Hash:
    """
    Hash Table

    dictionary: {token: [value1, value2, value3, value4]}
    sorted_hash: [(token, [value1, value2, value3, value4])]
    """

    def __init__(self) -> None:
        self.dictionary = {}
        self.sorted_hash = []

    # Add token to hash table
    def add(self, token: str, value: int):
        if token not in self.dictionary:
            self.dictionary[token] = [value]
        else:
            self.dictionary[token].append(value)

    # Remove token from hash table
    def remove(self, token, value):
        if token not in self.dictionary:
            return
        else:
            self.dictionary[token].remove(value)

    # Sort hash table by value and token
    def sorted(self):
        self.sorted_hash = sorted(
            self.dictionary.items(), key=lambda kv: (kv[1], kv[0]))

    # Write hash table to file
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


class SinglePassInMemoryIndexing:
    """
    Single Pass in Memory Indexing
    ------------------------------
    output_filaname: output file name
    stream_token: list of tokens and values
    """

    def __init__(self, output_filename: str) -> None:
        self.output_filename = output_filename
        self.dictionary = Hash()
    # Write tokens to file

    def add(self, stream_token):
        for token, value in stream_token:
            self.dictionary.add(token, value)
        self.dictionary.sorted()
        self.dictionary.write_block_to_disk(self.output_filename)