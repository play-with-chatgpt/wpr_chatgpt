#!/usr/bin/env python3
# coding=utf-8

import rospy
from std_msgs.msg import String
import sys

# 主函数
if __name__ == "__main__":
    rospy.init_node("str_pub")

    if(len(sys.argv) > 1):
        #rospy.loginfo(sys.argv[1])
        question_msg = String()
        question_msg.data = sys.argv[1]

        # 发布问题给ChatGPT返回的结果
        ask_pub = rospy.Publisher("/wpr_ask", String, queue_size=1)
        rospy.sleep(0.1)
        ask_pub.publish(question_msg)
    else:
        rospy.logwarn("请在指令的后面加入要发送的问句")
    
    rospy.sleep(0.1)