# -*- coding: utf-8 -*-
__author__ = 'yuyang'

from Gyrfalcon.Globals import *
import os
def start_shell(filename, command="shell"):
	shellString = "cd "+django_path+";"+"python3 ./manage.py {command} ".format(command=command)
	signal = os.system(shellString)
	if signal != 0:
		print("请输入\'./{filename} help\'查看如何使用".format(filename=filename))

if __name__ == '__main__':
	if len(sys.argv) >= 3:
		commandString=sys.argv[2]
		if len(sys.argv) > 3:
			commandString += " "+sys.argv[3]
		start_shell(os.path.basename(sys.argv[1]), commandString)
	else:
		start_shell(os.path.basename(sys.argv[1]))
