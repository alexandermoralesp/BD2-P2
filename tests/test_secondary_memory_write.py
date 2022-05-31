import src.secondary_memory_write as smw


def test_smw():
    print("Secondary Memory Write Test")
    document = [
        ("b", 5),
        ("b", 6),
        ("b", 7),
        ("a", 1),
        ("a", 2),
        ("a", 3),
        ("a", 4),
    ]
    spimi = smw.SinglePassInMemoryIndexing(
        output_filename="data/information.bin")
    spimi.add(document)
    file = open("data/information.bin", "rb")
    file.seek(0)
    assert(file.tell() == 0)
    file.close()