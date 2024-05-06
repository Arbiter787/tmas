#!/usr/bin/python

import digital

if __name__ == "__main__":
    port = "/dev/serial0"
    salinity_info = digital.read_data(port)

    print("Salinity", salinity_info)

