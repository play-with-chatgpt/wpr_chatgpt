#!/usr/bin/env python3
# coding=utf-8

import rospy
from std_msgs.msg import String
from urllib import response
import openai
   
# 接收问题字符串回调函数
def cbQuestion(msg):
    rospy.loginfo("--------------------")
    rospy.loginfo(msg.data)

    global conversation
    global msg_log
    if(conversation == True):
        msg_log.append({"role": "user", "content": msg.data})
    else:
        msg_log = [{"role": "user", "content": msg.data}]

    # print(msg_log)

    global model_engine
    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=msg_log,

    )

    response = completion["choices"][0]["message"]["content"]
    rospy.logwarn(response)

    if(conversation == True):
        msg_log.append({"role": "assistant", "content": response})

# 主函数
if __name__ == "__main__":
    rospy.init_node("chatgpt_node")

    #读取 API Key 参数
    api_key =  rospy.get_param('~openai/api_key')
    model_engine =  rospy.get_param('~openai/model' , "gpt-3.5-turbo")
    personality =  rospy.get_param('~openai/personality' , "")
    conversation =  rospy.get_param('~openai/conversation' , "False")

    openai.api_key = api_key

    rospy.logwarn("ChatGPT: 当前使用模型 %s",model_engine)

    # 订阅外部输入的问话
    question_sub = rospy.Subscriber("/wpr_ask", String, cbQuestion, queue_size=1)

    # 发布ChatGPT返回的结果
    response_pub = rospy.Publisher("/chatspt_answer", String, queue_size=1)

    msg_log = []

    if(len(personality) > 0):
        msg_log.append({"role": "system", "content": "你是一名"+personality})
        rospy.logwarn("ChatGPT: 我是一名"+personality+",我已经准备好了！向我提问吧 ^_^")
    else:
        rospy.logwarn("ChatGPT: 我已经准备好了！向我提问吧 ^_^")

    rospy.spin()