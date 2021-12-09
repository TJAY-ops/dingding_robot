# -*- coding: utf-8-*-
from flask import Flask
from flask import jsonify,request
app = Flask(__name__)

def initKey(post_userid, post_sign, post_timestamp, post_mes):
    # 配置token
    # 得到当前时间戳
    timestamp = str(round(time.time() * 1000))
    # 计算签名
    app_secret = '*****'
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(post_timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    # 验证是否来自钉钉的合法请求
    if (abs(int(post_timestamp) - int(timestamp)) < 3600000 and post_sign == sign):
        webhook="https://oapi.dingtalk.com/robot/send?access_token=123456789"#宝1
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        # 发送消息
        #message_json = json.dumps(selectMes(post_userid, post_mes))
        # 返回发送状态
        return sendText()
        #info = requests.post(url=webhook, data=message_json, headers=header)
        print(info.text)
    else:
        print("Warning:Not DingDing's post")
        
def sendText(post_userid, send_mes):
    # 发送文本形式
    message = {
        "msgtype": "text",
        "text": {
            "content": send_mes
        },
        "at": {
            "atDingtalkIds": [post_userid],
            "isAtAll": False
        }
    }
    return message
@app.route("/",methods=['GET','POST'])
def home():
    print "--------------1",request.json
    org_msg=request.json
    #post_sign = org_msg.get('sign').strip()
    #post_timestamp = org_msg.get('timestamp').strip()

    if org_msg is None:
        return {}
    post_userid = org_msg.get('senderId').strip()
    sender_nick = org_msg.get('senderNick').strip()###发送消息的昵称，到时候做权限管理
    group_name=org_msg.get("conversationTitle")####获取群组的名字
    if group_name==u"螺旋蜗":
        return {}
    content = org_msg.get('text').get('content')
    print "--------------------",content
    if content.strip()=="":
        send_msg=u"不要调戏我，后面请输入执行指令（不清楚可以打help)"
    else:
        send_msg=u"你说的是: {0}".format(content)
    msg=sendText(post_userid,send_msg)
    return msg

    
    
@app.route("/ppt",methods=['GET','POST'])
def hello_world():
    # print "--------1 ",dir(request.form)
    print "--------2 ",request.json
    print "-----------3 ",dir(request.values)
    vv=request.values.to_dict()
    sql="replace into test_fake_newuser_abtest("
    vls=")values("
    for k,v in vv.iteritems():
        sql+=k+","
        vls+="%s,"
    sql=sql[:-1]+vls[:-1]+")"
    print "----------",sql
    return sql

if __name__ == "__main__":
    app.run(debug=True,port=8090)
