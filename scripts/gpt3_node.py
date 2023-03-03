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

    global api_key
    openai.api_key = api_key
    prompt = msg.data

    global model_engine
    completion = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    if 'choices' in completion:
            if len(completion['choices'])>0:
                response= completion['choices'][0]['text']
                global response_pub
                answer_msg = String()
                answer_msg.data = response
                response_pub.publish(answer_msg)
            else:
                response = None
    else:
            response = None
    rospy.logwarn(response)

# 主函数
if __name__ == "__main__":
    rospy.init_node("gpt3_node")

    #读取 API Key 参数
    api_key =  rospy.get_param('~openai/api_key')
    model_engine =  rospy.get_param('~openai/model' , "davinci-instruct-beta-v3")

    rospy.logwarn("GPT-3: 当前使用模型 %s",model_engine)

    # 订阅外部输入的问话
    question_sub = rospy.Subscriber("/wpr_ask", String, cbQuestion, queue_size=1)

    # 发布ChatGPT返回的结果
    response_pub = rospy.Publisher("/chatspt_answer", String, queue_size=1)

    rospy.logwarn("GPT-3: 我已经准备好了！向我提问吧 ^_^")
    rospy.spin()