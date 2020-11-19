from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    #It should create the same hash with arguments of different data types
    # in any order

    assert crypto_hash(1, [2], 'three') == crypto_hash('three', 1, [2])
    assert crypto_hash('foo') == 'e06200c48b1436de6c71819e441237ef3fea7d4f228c51b3b41c5d5d10f3bbd0'