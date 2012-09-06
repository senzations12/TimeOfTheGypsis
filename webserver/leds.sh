#!/bin/bash
echo -e -n \\x0$2 | ./coap-client -m put coap://[fecb::$1]:61616/l -T 3a -t binary -f -
