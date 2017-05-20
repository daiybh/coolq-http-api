
keyword_findPeople = '#车找人#'
keyword_findCar = '#人找车#'


class MessagePaser:

    def __init__(self, _msgSender):
        self.msgSender = _msgSender

    def isCar(self, data):
        msg = data.get('message')
        if len(msg) < 10:
            return False
        v = msg.find(keyword_findPeople)
        if v == -1:
            return False
        return True

    def isFindCar(self, data):
        msg = data.get('message')
        if len(msg) < 5:
            return
        v = msg.find(keyword_findCar)
        if v == -1:
            return False
        return True

    def isBan(self, msg, group_id):
        """
        usage:#禁言#时长(分)#@QQ
        """
        v = msg.find('#禁言#')
        if v < 0:
            return
        v1 = msg.find('#', v + 4)
        duration = 30
        if v1 >= 0:
            duration = msg[v + 4:v1]
        findQQstr = '[CQ:at,qq='
        v = msg.find(findQQstr)
        if v < 0:
            return

        v = v + len(findQQstr)
        v1 = msg.find(']', v)

        if v1 < 0:
            return
        QQ = msg[v:v1]
        #print("ban-->",group_id,QQ,duration)
        self.msgSender.set_group_ban(group_id, QQ, int(duration) * 60)
        return True

    def isAdminMsg(self, data):
        if data.get('user_id') != 7277017:
            return '', 204
        group_id = data.get('group_id')
        msg = data.get('message')
        if self.isBan(msg, group_id):
            return '', 204
        if msg.find("#帮助#") > -1:
            s = ''
            s = s + "\n" + self.isBan.__doc__
            self.msgSender.send_private_msg(data.get('user_id'), s)
        return '', 204

    def passMessage_Private(self, data):
        self.msgSender.send_private_msg(
            data.get('user_id'),  data.get('message'))
        return '', 204
