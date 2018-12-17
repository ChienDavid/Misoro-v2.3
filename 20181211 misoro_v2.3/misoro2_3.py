#!/usr/bin/env python
# license removed for brevity
#******************************************************************
#***************************** david ******************************
#******************************************************************
# Author       : Chien Van Dang
# Executed file: moral_reasoner.soar
# Updated date : 11th Dec. 2018
#
# Application  : Soar Ethical Agent: top-down and bottom-up (3rd year)
#******************************************************************
#******************************************************************
#==================================================================
from misoro_sml import misoro_sml
import os
import rospy

cur_dir = os.path.dirname(os.path.realpath(__file__))
SOAR_PROGRAM_PATH = cur_dir+"/moral_reasoner.soar"

#==================================================================
if __name__ == '__main__':
	try:
		agent = misoro_sml('misoro',SOAR_PROGRAM_PATH)
		agent.runAgent()
		agent.delAgent()

	except rospy.ROSInterruptException:
		pass

