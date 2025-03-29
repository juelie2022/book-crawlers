import requests
import time
import sys
import random

from source.Proxies_Pool import Proxies_Pool
import source.Header
from source.basic_class_function import Get_Book

class Requester:
    def __init__(self, book_name="Default Book", whether_epub=False,
                 use_proxies=False, proxies_pool_num=5, thread_num=1):
        """
        初始化 Requester 对象。
        
        参数:
          - book_name: 书籍名称，用于初始化 Get_Book
          - whether_epub: 是否生成 epub（传递给 Get_Book）
          - use_proxies: 是否启用代理
          - proxies_pool_num: 代理池大小
          - thread_num: 线程数
        """
        # 依赖 Get_Book 实例化，管理代理、user_agent 等
        self.book = Get_Book(book_name, whether_epub, use_proxies, proxies_pool_num, thread_num)
        # 初始化 header，设置初始 User-Agent
        initial_header = {"User-Agent": self.book.user_agent.rgua()}
        self.header = Header(header=initial_header)
    
    def update_user_agent(self):
        """更新 User-Agent 头"""
        new_ua = self.book.user_agent.rgua()
        self.header.perm_replace_header("User-Agent", new_ua)
    
    def send_request(self, url, method="GET", data=None):
        """
        通用请求方法，根据是否使用代理来选择请求方式。
        
        参数:
          - url: 请求的目标地址
          - method: 请求方式 ("GET" 或 "POST")
          - data: POST 请求时发送的数据
        
        返回:
          - requests.Response 对象
        """
        # 更新请求头中的 User-Agent
        self.update_user_agent()
        # 根据是否启用代理选择对应的请求方法
        if self.book.whether_Proxies:
            response = self.book.proxies_request(url, method == "POST", data)
        else:
            response = self.book.request(url, method == "POST", data)
        return response

# 示例使用：
if __name__ == "__main__":
    # 初始化一个 Requester 实例，这里不使用代理（use_proxies=False）
    requester = Requester(book_name="Example Book", whether_epub=False,
                          use_proxies=False, proxies_pool_num=5, thread_num=1)
    test_url = "https://www.example.com"
    try:
        # 发送 GET 请求
        resp = requester.send_request(test_url, method="GET")
        print("状态码：", resp.status_code)
        # 打印部分响应内容
        print("响应内容：", resp.text[:300])
    except Exception as e:
        print("请求出错：", e)
