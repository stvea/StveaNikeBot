import os
import time

def reconnect():
	cmd_str = "rasdial ADSL /disconnect"
	os.system(cmd_str)
	time.sleep()
	cmd_str = "rasdial ADSL 123ABC 123456"
	os.system(cmd_str)