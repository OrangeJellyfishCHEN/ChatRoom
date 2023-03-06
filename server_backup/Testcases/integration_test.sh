#!/bin/bash
coverage run ../server.py 8080 &
coverage report
coverage run -a client.py 8080 integration_test.in
coverage run -a client1.py 8080 integration_test1.in
kill -9 `jobs -p`
coverage report -m