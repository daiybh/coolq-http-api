import requests



class MsgSender:

    replyUrl=''
    requestHeaders=''
    def __init__(self,_replyUrl,_requestHeaders):
        self.replyUrl = _replyUrl
        self.requestHeaders = _requestHeaders
    def send_msg(self,func, jsonMsg):
        requests.post(self.replyUrl + func, json=jsonMsg, headers=self.requestHeaders)
    def send_private_msg(self,userid,msg):
        self.send_msg('send_private_msg', jsonMsg={'user_id': userid, 'message': msg})
    def set_group_ban(self,group_id,userid,duration=30*60):
        #print("ban",group_id,userid,duration)
        self.send_msg('set_group_ban',jsonMsg={'user_id':userid,'group_id':group_id,'duration':duration})
