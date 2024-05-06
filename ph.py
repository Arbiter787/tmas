#!/usr/bin/python

import digital

if __name__ == "__main__":
    port = "/dev/serial0"
    ph_info = digital.read_data(port)

    print("PH", ph_info)

