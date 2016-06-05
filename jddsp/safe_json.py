import json


def string_xor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def load_xor_json(json_file, xor_key):
    print string_xor(open(json_file).read().encode("ascii"), xor_key.encode("ascii"))
    return json.loads(string_xor(open(json_file).read().encode("ascii"), xor_key.encode("ascii")))


def save_xor_json(object_to_json, xor_key, json_file="default.json", append=False, **kwargs):
    print object_to_json
    print string_xor(json.dumps(object_to_json, **kwargs), xor_key)

    open(json_file, ("a" if append else "w")).write(
        string_xor(json.dumps(object_to_json, **kwargs), xor_key))
