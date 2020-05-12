from bs4 import BeautifulSoup
import urllib.request, requests, time

# 헤더에 유저 에이전트 값 넣어야 요청이 제대로 옴
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}         

# 텔레그램 봇 요청
def sendTelegramMsg(APIKey, chatID, text):
  r = requests.get("https://api.telegram.org/bot"
                   + APIKey + "/sendMessage?chat_id="
                   + chatID + "&text="
                   + text + "&parse_mode=Markdown")
  return r

# ------------ 사용 전 직접 설정해 주어야 하는 부분 ------------

# 텔레그램 설정
TelAPI = "" # 텔레그램 봇키
TelChan = "" # 주소
updTime = 120 #second

# 갤러리 설정 
gall = ['baseball_new8',]
prevNum = []

# -------------------------------------------------------------


# 시간 표시 형식
tType = "%Y-%m-%d %H-%M-%S"
print ("--------DCBELL 설정 값--------")
print ("Telegram 채널ID: " + TelChan)
print ("Update Time: " + str(updTime))

roop = 0
while (1):

    #마이너, 정식갤러리 판별
    link = 'https://gall.dcinside.com/board/lists/?id=' + gall[roop]
    r = requests.get(link, headers = hdr).text
    #마이너 갤러리일 경우
    if 'location.replace' in r: link = link.replace('board/','mgallery/board/')

    req = urllib.request.Request(link, headers = hdr)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.find_all("tr", { "class" : "ub-content us-post"})

    for post in posts:
        tmp = post.find("td", { "class" : "gall_tit ub-word"})

        if "<b>" not in str(tmp):
            prevNum[roop] = post.find("td", { "class" : "gall_num"}).text # 게시글 번호
            break

    roop = roop + 1
    if (not gall[roop]) :
        break

while(1):
    try:
        for g in gall:

            req = urllib.request.Request(link, headers = hdr)
            html = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(html, "html.parser")
            posts = soup.find_all("tr", { "class" : "ub-content us-post"})
            posts.reverse()

            for post in posts:

                # 게시글 제목
                tmp = post.find("td", { "class" : "gall_tit ub-word"})

                if "<b>" not in str(tmp):
                    title = tmp.a.text
                    postnum = post.find("td", { "class" : "gall_num"}).text # 게시글 번호   
                    tmp = post.find("td", { "class" : "gall_writer ub-writer"}) # 게시글 작성자 (유동은 IP)
                    name = tmp.find("em").text
                    ip = tmp.find("span", { "class" : "ip"})

                    if ip is not None: ip = ip.text
                    else: ip = None

                    if (int(postnum) > int(prevNum)):
                        print("-------")
                        print(g + ": " + postnum)
                        if (ip) :
                            print(name + ip + " : " + title)
                            sendTelegramMsg(TelAPI, TelChan,
                                            name + ip + " : \n" + title + "\n" +
                                            "[글 링크](https://gall.dcinside.com/" + g + "/" + postnum + ")")
                        else :
                            print(name + " : " + title)
                            sendTelegramMsg(TelAPI, TelChan,
                                            name + " : \n" + title + "\n" +
                                            "[글 링크](https://gall.dcinside.com/" + g + "/" + postnum + ")")
                        prevNum = postnum
                        break
            time.sleep(1)

    except Exception as ex:
        print("[Error]", ex)

    time.sleep(updTime)

