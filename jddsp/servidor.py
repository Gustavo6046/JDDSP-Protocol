import socket
import time
from threading import Thread

import safe_json

# Modifiable parameters
ip = "127.0.0.1"
port = 1291
json_file = "db.spj"
json_password = "password"
max_connections = 2


def parse_received_data(data, client_ip, client_port):
    data_splits = data.split(" ")

    if len(data_splits) < 1:
        return "ERROR ERR_EMPTY_DATA"

    if not "{}:{}".format(client_ip, client_port) in safe_json.load_xor_json("registered.spj", json_password).keys():
        if data_splits[0].upper() == "REGISTER":
            if len(data_splits) < 2:
                return "ERR_INSUFFICIENT_ARGUMENTS"

            print safe_json.load_xor_json("registered.spj", json_password)

            result = safe_json.load_xor_json("registered.spj", json_password)
            result.update({"{}:{}".format(client_ip, client_port): {"email": data_splits[1]}})

            safe_json.save_xor_json(result, json_password, "registered.spj")

            return "INFO REGISTER :SUCCESS"

        return "ERROR CLIENT_NOT_REGISTERED"

    if data_splits[0].lower() == "getjson":
        if len(data_splits) < 4:
            return "ERROR ERR_INSUFFICIENT_GETJSON_ARGS"

        try:
            return "RESULT :" + safe_json.load_xor_json(json_file, data_splits[1])[data_splits[2]]

        except (IndexError, KeyError):
            return "ERROR ERR_INVALID_KEY_OR_INDEX"

    if data_splits[0].lower() == "savejson":
        if len(data_splits) < 2:
            return "ERROR ERR_INSUFFICIENT_ARGUMENTS"

        if data_splits[1] != json_password:
            return "ERROR ERR_INVALID_PASSWORD"

        try:
            safe_json.save_xor_json(json_file, data_splits[1])

        except BaseException as error:
            return "ERROR ERR_PYTHON_ERR :" + error.__class__.__name__.upper()

        return "SUCCESS"


def server_connection():
    print "Connection {} started!".format(connection_id)

    start_time = time.time()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(2)
    (client, (client_ip, client_port)) = sock.accept()

    client.sendall("INFO CONNECTION_SUCCESSFUL\n")
    print "Connection was succesfull!"

    while True:
        try:
            sock_error = False

            lines = [line.rstrip("\r") for line in client.recv(4096).split("\n") if line != "\r"]

            for line in lines:
                print "Parsing line \'{}\' at connection {}!".format(line, connection_id)
                client.sendall(parse_received_data(line, client_ip, client_port) + "\n")

        except socket.error:
            sock_error = True
            time.sleep(0.1)
            continue

        except KeyboardInterrupt:
            break

        except:
            print "Connection {} has run for {} seconds.".format(connection_id, time.time() - start_time)
            raise


for connection_id in xrange(1, max_connections):
    Thread(target=server_connection).start()
