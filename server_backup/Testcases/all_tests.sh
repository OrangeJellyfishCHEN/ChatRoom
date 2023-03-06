sh integration_test.sh
diff register_login_test.out register_login_test_expected.out|wc -l| cat > testcases.txt
diff join_channels_test.out join_channels_test_expected.out|wc -l| cat >> testcases.txt
diff create_channel_test_expected.out create_channel_test.out|wc -l|cat >> testcases.txt
diff say_test.out say_test_expected.out|wc -l| cat >> testcases.txt
diff more_client_test.out more_client_test_expected.out|wc -l| cat >> testcases.txt
