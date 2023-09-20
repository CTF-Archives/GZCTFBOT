import asyncio
import requests
import urllib3
import argparse
import json, time, sys
from datetime import datetime, timezone, timedelta

urllib3.disable_warnings()

URL = ""
GROUP_NOTICE_ID = 0
GROUP_EVENTS_ID = 0
MATCH_ID = 0
CQ_PORT = 0

# Total Announcement Lens
noticeLen = 0
# Match Announcement Lens
normalListLen = 0
# New Challenge Lens
newchallengeListLen = 0
# New Hint Lens
newhintLen = 0
# First Blood Lens
firstbloodLen = 0
# Second Blood Lens
secondbloodLen = 0
# Third Blood Lens
thirdbloodLen = 0

noticeList = []

def processTime(t):
    input_time = datetime.fromisoformat(t)
    input_time_utc = input_time.replace(tzinfo=timezone.utc)
    beijing_timezone = timezone(timedelta(hours=8))
    beijing_time = input_time_utc.astimezone(beijing_timezone)
    return beijing_time.strftime("%Y-%m-%d %H:%M:%S")

def getNotice(URL, MATCH_ID):
    request = requests.session()
    dic = {
        'platform-notice': URL + '/api/game/{0}/notices'.format(MATCH_ID),
        'platform-events': URL + '/api/game/{0}/events?hideContainer=false&count=2&skip=0'.format(MATCH_ID)
    }
    try:
        res = request.get(dic['platform-notice'], verify=False)
        allList = json.loads(res.text)
        return allList
    except:
        sys.exit("\033[31m[%s] [ERROR]: 0ops! Something wrong... :(\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))))
    
# Match Announcement Information
def getNormalInfo(URL, MATCH_ID):
    global noticeLen
    tmpList = getNotice(URL, MATCH_ID)
    tmpListLen = len(tmpList)
    if (noticeLen < tmpListLen):
        interval = tmpListLen - noticeLen
        normal_list = []
        for i in range(0, interval):
            if (tmpList[i]['type'] == 'Normal'):
                notices = {
                    "id": tmpList[i]['id'],
                    "time": tmpList[i]['time'],
                    "content": tmpList[i]['content']
                }
                normal_list.append(notices)
        sorted(normal_list, key=lambda notices: notices['id'])
    return normal_list

# New Challenge Information
def getNewChallengeInfo(URL, MATCH_ID):
    global noticeLen
    tmpList = getNotice(URL, MATCH_ID)
    tmpListLen = len(tmpList)
    if (noticeLen < tmpListLen):
        interval = tmpListLen - noticeLen
        newchallenge_list = []
        for i in range(0, interval):
            if (tmpList[i]['type'] == 'NewChallenge'):
                notices = {
                    "id": tmpList[i]['id'],
                    "time": tmpList[i]['time'],
                    "content": tmpList[i]['content']
                }
                newchallenge_list.append(notices)
        sorted(newchallenge_list, key=lambda notices: notices['id'])
    return newchallenge_list

# New Hint Information
def getNewHintInfo(URL, MATCH_ID):
    global noticeLen
    tmpList = getNotice(URL, MATCH_ID)
    tmpListLen = len(tmpList)
    if (noticeLen < tmpListLen):
        interval = tmpListLen - noticeLen
        newhint_list = []
        for i in range(0, interval):
            if (tmpList[i]['type'] == 'NewHint'):
                notices = {
                    "id": tmpList[i]['id'],
                    "time": tmpList[i]['time'],
                    "content": tmpList[i]['content']
                }
                newhint_list.append(notices)
        sorted(newhint_list, key=lambda notices: notices['id'])
    return newhint_list

# First Blood Information
def getFirstBloodInfo(URL, MATCH_ID):
    global noticeLen
    tmpList = getNotice(URL, MATCH_ID)
    tmpListLen = len(tmpList)
    if (noticeLen < tmpListLen):
        interval = tmpListLen - noticeLen
        firstblood_list = []
        for i in range(0, interval):
            if (tmpList[i]['type'] == 'FirstBlood'):
                notices = {
                    "id": tmpList[i]['id'],
                    "time": tmpList[i]['time'],
                    "content": tmpList[i]['content']
                }
                firstblood_list.append(notices)
        sorted(firstblood_list, key=lambda notices: notices['id'])
    return firstblood_list

# Second Blood Information
def getSecondBloodInfo(URL, MATCH_ID):
    global noticeLen
    tmpList = getNotice(URL, MATCH_ID)
    tmpListLen = len(tmpList)
    if (noticeLen < tmpListLen):
        interval = tmpListLen - noticeLen
        secondblood_list = []
        for i in range(0, interval):
            if (tmpList[i]['type'] == 'SecondBlood'):
                notices = {
                    "id": tmpList[i]['id'],
                    "time": tmpList[i]['time'],
                    "content": tmpList[i]['content']
                }
                secondblood_list.append(notices)
        sorted(secondblood_list, key=lambda notices: notices['id'])
    return secondblood_list

# Third Blood Information
def getThirdBloodInfo(URL, MATCH_ID):
    global noticeLen
    tmpList = getNotice(URL, MATCH_ID)
    tmpListLen = len(tmpList)
    if (noticeLen < tmpListLen):
        interval = tmpListLen - noticeLen
        thirdblood_list = []
        for i in range(0, interval):
            if (tmpList[i]['type'] == 'ThirdBlood'):
                notices = {
                    "id": tmpList[i]['id'],
                    "time": tmpList[i]['time'],
                    "content": tmpList[i]['content']
                }
                thirdblood_list.append(notices)
        sorted(thirdblood_list, key=lambda notices: notices['id'])
    return thirdblood_list

# Sending Message
def sendMessage(msg, CQ_PORT, GROUP_NOTICE_ID):
    try:
        request = requests.Session()
        r = request.get("http://127.0.0.1:%s/send_group_msg?group_id=%s&message=%s" 
                        % (
                            str(CQ_PORT),
                            str(GROUP_NOTICE_ID), 
                            str(msg))
                        )
        print('\033[32m[%s] [SEND] Sending message to %s\033[0m' % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), GROUP_NOTICE_ID))
    except requests.exceptions.ConnectionError as e:
        sys.exit("\033[31m[%s] [ERROR] Error sending message to %s, Connection error possible port or address error\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), GROUP_NOTICE_ID))

async def sendMessageNotice(URL, MATCH_ID, CQ_PORT, GROUP_NOTICE_ID):
    global normalListLen, newchallengeListLen, newhintLen, firstbloodLen, secondbloodLen, thirdbloodLen
    try:
        while True:
            message = ""
            # Normal List
            tmpNormalList = getNormalInfo(URL, MATCH_ID)
            tmpNormalListLen = len(getNormalInfo(URL, MATCH_ID))
            # New Challenge
            tmpNewChallengeInfo = getNewChallengeInfo(URL, MATCH_ID)
            tmpNewChallengeInfoLen = len(getNewChallengeInfo(URL, MATCH_ID))
            # New Hint
            tmpNewHintInfo = getNewHintInfo(URL, MATCH_ID)
            tmpNewHintInfoLen = len(getNewHintInfo(URL, MATCH_ID))
            # First Blood
            tmpFirstBloodInfo = getFirstBloodInfo(URL, MATCH_ID)
            tmpFirstBloodInfoLen = len(getFirstBloodInfo(URL, MATCH_ID))
            # Second Blood
            tmpSecondBloodInfo = getSecondBloodInfo(URL, MATCH_ID)
            tmpSecondBloodInfoLen = len(getSecondBloodInfo(URL, MATCH_ID))
            # Third Blood
            tmpThirdBloodInfo = getThirdBloodInfo(URL, MATCH_ID)
            tmpThirdBloodInfoLen = len(getThirdBloodInfo(URL, MATCH_ID))

            print('\033[33m[%s] [INFO]: Waiting data...\033[0m' % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))))
            if (normalListLen < tmpNormalListLen):
                message = "【比赛公告】\n内容：%s\n时间：%s" % (tmpNormalList[0]['content'], processTime(tmpNormalList[0]['time']))
                print("\033[32m[%s] [ANNOUNCEMENTS] Data on receipt of Announcements %s\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), tmpNormalList[0]['content']))
                sendMessage(msg=message, CQ_PORT=CQ_PORT, GROUP_NOTICE_ID=GROUP_NOTICE_ID)
                normalListLen = tmpNormalListLen
            else:
                normalListLen = tmpNormalListLen
            if (newchallengeListLen < tmpNewChallengeInfoLen):
                message = "【新增题目】\n%s\n时间：%s" % (tmpNewChallengeInfo[0]['content'], processTime(tmpNewChallengeInfo[0]['time']))
                print("\033[32m[%s] [NEW CHALLENGE] Data on receipt of New Challenge %s\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), tmpNewChallengeInfo[0]['content']))
                sendMessage(msg=message, CQ_PORT=CQ_PORT, GROUP_NOTICE_ID=GROUP_NOTICE_ID)
                newchallengeListLen = tmpNewChallengeInfoLen
            else:
                newchallengeListLen = tmpNewChallengeInfoLen
            if (newhintLen < tmpNewHintInfoLen):
                message = "【题目提示】\n%s\n时间：%s" % (tmpNewHintInfo[0]['content'], processTime(tmpNewHintInfo[0]['time']))
                print("\033[32m[%s] [NEW HINT] Data on receipt of New Hint %s\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), tmpNewHintInfo[0]['content']))
                sendMessage(msg=message, CQ_PORT=CQ_PORT, GROUP_NOTICE_ID=GROUP_NOTICE_ID)
                newhintLen = tmpNewHintInfoLen
            else:
                newhintLen = tmpNewHintInfoLen
            if (firstbloodLen < tmpFirstBloodInfoLen):
                message = "【一血播报】\n%s\n时间：%s" % (tmpFirstBloodInfo[0]['content'], processTime(tmpFirstBloodInfo[0]['time']))
                print("\033[32m[%s] [FIRST BLOOD] Data on receipt of First Blood %s\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), tmpFirstBloodInfo[0]['content']))
                sendMessage(msg=message, CQ_PORT=CQ_PORT, GROUP_NOTICE_ID=GROUP_NOTICE_ID)
                firstbloodLen = tmpFirstBloodInfoLen
            else:
                firstbloodLen = tmpFirstBloodInfoLen
            if (secondbloodLen < tmpSecondBloodInfoLen):
                message = "【二血播报】\n%s\n时间：%s" % (tmpSecondBloodInfo[0]['content'], processTime(tmpSecondBloodInfo[0]['time']))
                print("\033[32m[%s] [SECOND BLOOD] Data on receipt of First Blood %s\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), tmpSecondBloodInfo[0]['content']))
                sendMessage(msg=message, CQ_PORT=CQ_PORT, GROUP_NOTICE_ID=GROUP_NOTICE_ID)
                secondbloodLen = tmpSecondBloodInfoLen
            else:
                secondbloodLen = tmpSecondBloodInfoLen
            if (thirdbloodLen < tmpThirdBloodInfoLen):
                message = "【三血播报】\n%s\n时间：%s" % (tmpThirdBloodInfo[0]['content'], processTime(tmpThirdBloodInfo[0]['time']))
                print("\033[32m[%s] [THIRD BLOOD] Data on receipt of First Blood %s\033[0m" % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), tmpThirdBloodInfo[0]['content']))
                sendMessage(msg=message, CQ_PORT=CQ_PORT, GROUP_NOTICE_ID=GROUP_NOTICE_ID)
                thirdbloodLen = tmpThirdBloodInfoLen
            else:
                thirdbloodLen = tmpThirdBloodInfoLen
            await asyncio.sleep(3)

    except KeyboardInterrupt as e:
        print('\033[31m[%s] [ERROR]: Trying to exit !!!\033[0m' % (str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))))

async def runner():
    tasks = [
        asyncio.create_task(sendMessageNotice(
            URL=URL,
            GROUP_NOTICE_ID=GROUP_NOTICE_ID,
            MATCH_ID=MATCH_ID,
            CQ_PORT=CQ_PORT
        )),
    ]
    normalListLen = len(getNormalInfo(URL=URL, MATCH_ID=MATCH_ID))
    newchallengeListLen = len(getNewChallengeInfo(URL=URL, MATCH_ID=MATCH_ID))
    newhintLen = len(getNewHintInfo(URL=URL, MATCH_ID=MATCH_ID))
    firstbloodLen = len(getFirstBloodInfo(URL=URL, MATCH_ID=MATCH_ID))
    secondbloodLen = len(getSecondBloodInfo(URL=URL, MATCH_ID=MATCH_ID))
    thirdbloodLen = len(getThirdBloodInfo(URL=URL, MATCH_ID=MATCH_ID))

    await asyncio.gather(*tasks)

def main():
    global URL, GROUP_NOTICE_ID, MATCH_ID, CQ_PORT
    BANNER = """\033[01;34m\
    
  _____  ______    _____ ___________  ______       _   
 |  __ \|___  /_ _/  __ \_   _|  ___| | ___ \     | |  
 | |  \/   / /(_|_) /  \/ | | | |_    | |_/ / ___ | |_ 
 | | __   / /     | |     | | |  _|   | ___ \/ _ \| __|
 | |_\ \./ /____ _| \__/\ | | | |     | |_/ / (_) | |_    \033[0m\033[4;37m%s\033[0m
  \____/\_____(_|_)\____/ \_/ \_|     \____/ \___/ \__|   \033[0m\033[4;37m%s\033[0m\n
    """ % ("Author: IceCliffs", "Version: v0.0.2")
    print(BANNER)
    parser = argparse.ArgumentParser(description="GZ::CTF QQ Bot")
    parser.add_argument('--url', 
                        required=True,
                        help="platform url")
    parser.add_argument('--notice', 
                        required=True,
                        help="qq notice Group")
    parser.add_argument('--id', 
                        required=True,
                        help="race id")
    parser.add_argument('--port', 
                        required=True,
                        help="cq port")
    parser.add_argument('--events', 
                        help="qq detail group (optional)")
    parser.add_argument('--cookie', 
                        help="administrator cookie")
    args = parser.parse_args()
    
    if args.url and args.notice and args.id and args.port:
        URL = args.url
        GROUP_NOTICE_ID = args.notice
        MATCH_ID = args.id
        CQ_PORT = args.port
        asyncio.run(runner())

if __name__ == "__main__":
    main()