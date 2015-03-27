# -*- coding: utf-8 -*-

import json
from datetime import datetime

from db_helper import DbAgent

class Executor(object):
    '''
    尝试在这里设计第二版的executor
    '''
    # 总感觉这里的属性设计的怪怪的。
    # 首先，requestJson,responseCode的命名方式是否贴切？
    # 对于外部的访问者来说，是没有必要知道它们的类型的。
    # 
    def __init__(self, _request):
        self.__actions      = []
        self.__requestJson  = _request
        self.__responseDict = {
            "orderId":0,
            "responseDes":"",
            "ext1":"",
            "responseCode":"01",
            "show":"",
            "print":"",
            "amt": 0,
            "ext2": ""
        }
        self.orderInfo     = {}
        self.productInfo   = {}
        # 这里为了在外部只能访问，而不能被修改。
        # 所以在这里定义一个这样的访问器还是很有必要的，
        # 避免这个属性在别的地方被无意修改。
        self.__db          = DbAgent()
        # 这里应该可以很容易的配制日志。
        # 比如很容易的打开日志，很容易的关闭日志。
        self.registerActions()

    @property
    def requestDict(self):
        '''
        返回请求参数的字典形式,
        验证应该交给action，这里不应该进行验证
        而且它和responseJson对外都没有setter
        '''
        return json.loads(self.__requestJson)

    @property
    def responseDict(self):
        return self.__responseDict
    
    @property
    def responseJson(self):
        '''
        返回响应参数的json形式
        '''
        return json.dumps(self.__responseDict)

    @property
    def db(self):
        return self.__db

    def register(self, _action):
        '''
        将一个动作注册到执行者
        '''
        self.__actions.append(_action)

    def registerActions(self):
        '''
        在此处按照顺序注册需要执行的一系列动作
        '''
        self.register(VerifyTradeTime(self))
        self.register(VerifyParseRequest(self))
        self.register(VerifyOrderId(self))
        self.register(OperateFetchOrderInfo(self))

    def execute(self):
        '''
        依次执行已经注册了的动作
        '''
        for action in self.__actions:
            ok = action.execute()
            if not ok:
                return False
        return True

class Action(object):
    '''
    一个可以执行的动作类
    '''
    def __init__(self, _executor):
        self.__executor = _executor

    @property
    def executor(self):
        return self.__executor
        
    def execute(self):
        '''
        执行此动作
        这里就算是框架的思想，作为一个callback
        '''
        if self.callback():
            self.successResponse()
            return True
        else:
            self.failResponse()
            return False

    def callback(self):
        pass

    def successResponse(self):
        '''
        此动作成功后需要执行的操作
        '''
        pass
    
    def failResponse(self):
        '''
        此动作失败后需要执行的操作
        '''
        pass

class Verification(Action):
    '''
    此动作执行一个验证
    '''
    pass

class Operation(Action):
    '''
    此动作执行一个操作
    '''
    pass

class VerifyTradeTime(Verification):
    '''
    Pos机打款时间检查
    '''
    def callback(self):
        '''
        POS机仅在9点到18点开放
        '''
        hour = datetime.now().hour
        if 9 <= hour < 18:
            return True
        else:
            return False

    def failResponse(self):
        self.executor.responseDict["responseDes"] = u"Pos打款仅在9点到18点开放"

class VerifyParseRequest(Verification):
    '''
    请求json可解析验证
    '''
    def callback(self):
        try:
            self.executor.requestDict
        except Exception, e:
            return False
        return True

    def failResponse(self):
        self.executor.responseDict["responseDes"] = u"参数异常不能解析json"
            

class VerifyOrderId(Verification):
    '''
    验证订单id正确
    '''
    def callback(self):
        try:
            int(self.executor.requestDict["orderId"])
        except Exception, e:
            print "这里确实出错了！！！"
            return False
        return True

    def failResponse(self):
        self.executor.responseDict["responseDes"] = u"不是数字，非法id"

class OperateFetchOrderInfo(Operation):
    '''
    获取订单信息
    '''
    def callback(self):
        try:
            orderId = self.executor.requestDict["orderId"]
            self.executor.orderInfo = self.executor.db.get_pay_info_by_id(orderId)
        except Exception, e:
            return False
        return True

    def failResponse(self):
        self.executor.responseDict["responseDes"] = u"订单信息获取失败"

        
class VerifyOrderStatusPayed(Verification):
    '''
    订单状态已经支付
    '''
    def callback(self):
        '''
        已支付status
        '''
        status_payed = [990, 980, 900, 800]

        status = self.executor.orderInfo.get("status", -1)
        if status in status_payed:
            return False
        return True

    def failResponse(self):
        self.executor.responseDict["responseDes"] = u"订单已经被支付"

    
class VerifyOrderStatusFailed(Verification):
    '''
    订单状态无效
    '''
    def callback(self):
        '''
        已失败status
        '''
        status_failed = [700, 600, 0]

        status = self.executor.orderInfo.get("status", -1)
        if status in status_failed:
            return False
        return True

    def failResponse(self):
        self.executor.responseDict["responseDes"] = u"订单无效"

class VerifyDealMoney(Verification):
    '''
    订单金额验证
    '''
    def callback(self):
        if self.executor.orderInfo["deal_money"] == 0:
            return False
        return True

    def failResponse(self):
        self.executor.responseDes["responseDes"] = u"订单金额不能为0"
