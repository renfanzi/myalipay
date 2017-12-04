#!/usr/bin/env python
# -*- coding:utf-8 -*-


from alipay1.myalipay import AliPay
import os, json, requests

# 支付宝配置参数
ALIPAY_APPID = "2017112100081631"
ALIPAY_URL = "https://openapi.alipay.com/gateway.do"
# "123456", "000001"
order_id = "000002"  # order_id

"""
    支付类
"""

def pay():

    # 创建用于进行支付宝支付的工具对象
    alipay = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_path="/opt/code/my_code/myPythonAlipay/alipay1/web/web_private_key.pem",
        alipay_public_key_path="/opt/code/my_code/myPythonAlipay/alipay1/web/web_public_key.pem",
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False  配合沙箱模式使用
    )

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(0.01),  # 将Decimal类型转换为字符串交给支付宝, 支付宝金额
        subject="商贸商城1",
        return_url="https://www.baidu.com",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    url = ALIPAY_URL + "?" + order_string
    req = requests.get("%s" % url)
    # print(req.content)
    print(req.text)

    return json.dumps({"code": 0, "message": "请求支付成功", "url": url})



def check_pay(order_id):
    # 创建用于进行支付宝支付的工具对象
    alipay = AliPay(
        appid="2017112100081631",
        app_notify_url=None,  # 默认回调url
        app_private_key_path="/opt/code/my_code/myPythonAlipay/alipay1/web/web_private_key.pem",
        alipay_public_key_path="/opt/code/my_code/myPythonAlipay/alipay1/web/web_public_key.pem",
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA2,官方推荐，配置公钥的时候能看到
        debug=False  # 默认False  配合沙箱模式使用
    )

    # while True:
        # 调用alipay工具查询支付结果
    response = alipay.api_alipay_trade_query(out_trade_no=order_id)  # response是一个字典
    # print(response)
    # 判断支付结果
    code = response.get("code")  # 支付宝接口调用成功或者错误的标志
    trade_status = response.get("trade_status")  # 用户支付的情况

    if code == "10000" and trade_status == "TRADE_SUCCESS":
        # 表示用户支付成功
        # 返回前端json，通知支付成功
        return json.dumps({"code": 0, "message": "支付成功"}, ensure_ascii=False)

    elif code == "40004" or (code == "10000" and trade_status == "WAIT_BUYER_PAY"):
        # 表示支付宝接口调用暂时失败，（支付宝的支付订单还未生成） 后者 等待用户支付
        # 继续查询
        # print(code)
        # print(trade_status)
        # continue
        return json.dumps({"code": 2, "message": "未生成或等待用户支付"})
    else:
        # 支付失败
        # 返回支付失败的通知
        return json.dumps({"code": 1, "message": "支付失败"})

if __name__ == '__main__':


    # a = pay()
    ret = check_pay('123456')
    print(ret)
