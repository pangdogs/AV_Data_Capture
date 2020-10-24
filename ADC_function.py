import requests
from lxml import etree

import config

SUPPORT_PROXY_TYPE = ("http", "socks5", "socks5h")

def get_data_state(data: dict) -> bool:  # 元数据获取失败检测
    if "title" not in data or "number" not in data:
        return False

    if data["title"] is None or data["title"] == "" or data["title"] == "null":
        return False

    if data["number"] is None or data["number"] == "" or data["number"] == "null":
        return False

    return True


def getXpathSingle(htmlcode,xpath):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result1 = str(html.xpath(xpath)).strip(" ['']")
    return result1


def get_proxy(proxy: str, proxytype: str = None) -> dict:
    ''' 获得代理参数，默认http代理
    '''
    if proxy:
        if proxytype in SUPPORT_PROXY_TYPE:
            proxies = {"http": proxytype + "://" + proxy, "https": proxytype + "://" + proxy}
        else:
            proxies = {"http": "http://" + proxy, "https": "https://" + proxy}
    else:
        proxies = {}

    return proxies


# 网页请求核心
def get_html(url, cookies: dict = None, ua: str = None, return_type: str = None):
    proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)

    if ua is None:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"} # noqa
    else:
        headers = {"User-Agent": ua}

    for i in range(retry_count):
        try:
            if not proxy == '':
                result = requests.get(str(url), headers=headers, timeout=timeout, proxies=proxies, cookies=cookies)
            else:
                result = requests.get(str(url), headers=headers, timeout=timeout, cookies=cookies)

            result.encoding = "utf-8"

            if return_type == "object":
                return result
            else:
                return result.text

        except requests.exceptions.ProxyError:
            print("[-]Connect retry {}/{}".format(i + 1, retry_count))
        except requests.exceptions.ConnectionError:
            print("[-]Connect retry {}/{}".format(i + 1, retry_count))
    print('[-]Connect Failed! Please check your Proxy or Network!')


def post_html(url: str, query: dict) -> requests.Response:
    proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)

    for i in range(retry_count):
        try:
            result = requests.post(url, data=query, proxies=proxies)
            return result
        except requests.exceptions.ProxyError:
            print("[-]Connect retry {}/{}".format(i+1, retry_count))
    print("[-]Connect Failed! Please check your Proxy or Network!")
    input("Press ENTER to exit!")
    exit()


def get_javlib_cookie() -> [dict, str]:
    import cloudscraper
    proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)

    raw_cookie = {}
    user_agent = ""

    # Get __cfduid/cf_clearance and user-agent
    for i in range(retry_count):
        try:
            raw_cookie, user_agent = cloudscraper.get_cookie_string(
                "http://www.b47w.com/cn",
                proxies=proxies
            )
            break
        except requests.exceptions.ProxyError:
            print("[-] ProxyError, retry {}/{}".format(i+1, retry_count))
        except cloudscraper.exceptions.CloudflareIUAMError:
            print("[-] IUAMError, retry {}/{}".format(i+1, retry_count))

    return raw_cookie, user_agent
		
def get_javdb_cookie() -> [dict, str]:
    import cloudscraper
    proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)

    raw_cookie = {}
    user_agent = ""

    # Get __cfduid/cf_clearance and user-agent
    for i in range(retry_count):
        try:
            raw_cookie, user_agent = cloudscraper.get_cookie_string(
                "http://www.javdb.com/",
                proxies=proxies
            )
            break
        except requests.exceptions.ProxyError:
            print("[-] ProxyError, retry {}/{}".format(i+1, retry_count))
        except cloudscraper.exceptions.CloudflareIUAMError:
            print("[-] IUAMError, retry {}/{}".format(i+1, retry_count))

    return raw_cookie, user_agent

def translateTag_to_sc(tag):
    tranlate_to_sc = config.Config().transalte_to_sc()
    if tranlate_to_sc:
        dict_gen = {'中文字幕': '中文字幕', '推薦作品': '推荐作品', '通姦': '通奸', '淋浴': '淋浴', '舌頭': '舌头',
                    '下流': '下流', '敏感': '敏感', '變態': '变态', '願望': '愿望', '慾求不滿': '慾求不满', '服侍': '服侍',
                    '外遇': '外遇', '訪問': '访问', '性伴侶': '性伴侣', '保守': '保守', '購物': '购物', '誘惑': '诱惑',
                    '出差': '出差', '煩惱': '烦恼', '主動': '主动', '再會': '再会', '戀物癖': '恋物癖', '問題': '问题',
                    '騙奸': '骗奸', '鬼混': '鬼混', '高手': '高手', '順從': '顺从', '密會': '密会', '做家務': '做家务',
                    '秘密': '秘密', '送貨上門': '送货上门', '壓力': '压力', '處女作': '处女作', '淫語': '淫语', '問卷': '问卷',
                    '住一宿': '住一宿', '眼淚': '眼泪', '跪求': '跪求', '求職': '求职', '婚禮': '婚礼', '第一視角': '第一视角',
                    '洗澡': '洗澡', '首次': '首次', '劇情': '剧情', '約會': '约会', '實拍': '实拍', '同性戀': '同性恋',
                    '幻想': '幻想', '淫蕩': '淫荡', '旅行': '旅行', '面試': '面试', '喝酒': '喝酒', '尖叫': '尖叫',
                    '新年': '新年', '借款': '借款', '不忠': '不忠', '檢查': '检查', '羞恥': '羞耻', '勾引': '勾引',
                    '新人': '新人', '推銷': '推销', 'ブルマ': '运动短裤',

                    'AV女優': 'AV女优', '情人': '情人', '丈夫': '丈夫', '辣妹': '辣妹', 'S級女優': 'S级女优', '白領': '白领',
                    '偶像': '偶像', '兒子': '儿子', '女僕': '女佣', '老師': '老师', '夫婦': '夫妇', '保健室': '保健室',
                    '朋友': '朋友', '工作人員': '工作人员', '明星': '明星', '同事': '同事', '面具男': '面具男', '上司': '上司',
                    '睡眠系': '睡眠系', '奶奶': '奶奶', '播音員': '播音员', '鄰居': '邻居', '親人': '亲人', '店員': '店员',
                    '魔女': '魔女', '視訊小姐': '视讯小姐', '大學生': '大学生', '寡婦': '寡妇', '小姐': '小姐', '秘書': '秘书',
                    '人妖': '人妖', '啦啦隊': '啦啦队', '美容師': '美容师', '岳母': '岳母', '警察': '警察', '熟女': '成熟的女人',
                    '素人': '素人', '人妻': '人妻', '痴女': '痴女', '角色扮演': '角色扮演', '蘿莉': '萝莉',
                    '模特': '模特', '教師': '教师', '學生': '学生', '少女': '少女', '新手': '新手', '男友': '男友',
                    '護士': '护士', '媽媽': '妈妈', '主婦': '主妇', '孕婦': '孕妇', '女教師': '女教师', '年輕人妻': '年轻人妻',
                    '職員': '职员', '看護': '看护', '外觀相似': '外观相似', '色狼': '色狼', '醫生': '医生', '新婚': '新婚',
                    '黑人': '黑人', '空中小姐': '空中小姐', '運動系': '运动系', '女王': '女王', '西裝': '西装', '旗袍': '旗袍',
                    '兔女郎': '兔女郎', '白人': '白人',

                    '制服': '制服', '內衣': '内衣', '休閒裝': '休閒装', '水手服': '水手服', '全裸': '全裸', '不穿內褲': '不穿内裤',
                    '和服': '和服', '不戴胸罩': '不戴胸罩', '連衣裙': '连衣裙', '打底褲': '打底裤', '緊身衣': '紧身衣', '客人': '客人',
                    '晚禮服': '晚礼服', '治癒系': '治癒系', '大衣': '大衣', '裸體襪子': '裸体袜子', '絲帶': '丝带', '睡衣': '睡衣',
                    '面具': '面具', '牛仔褲': '牛仔裤', '喪服': '丧服', '極小比基尼': '极小比基尼', '混血': '混血', '毛衣': '毛衣',
                    '頸鏈': '颈链', '短褲': '短裤', '美人': '美人', '連褲襪': '连裤袜', '裙子': '裙子', '浴衣和服': '浴衣和服',
                    '泳衣': '泳装', '網襪': '网袜', '眼罩': '眼罩', '圍裙': '围裙', '比基尼': '比基尼', '情趣內衣': '情趣内衣',
                    '迷你裙': '迷你裙', '套裝': '套装', '眼鏡': '眼镜', '丁字褲': '丁字裤', '陽具腰帶': '阳具腰带', '男装': '男装',
                    '襪': '袜',

                    '美肌': '美肌', '屁股': '屁股', '美穴': '美穴', '黑髮': '黑发', '嬌小': '娇小', '曬痕': '晒痕',
                    'F罩杯': 'F罩杯', 'E罩杯': 'E罩杯', 'D罩杯': 'D罩杯', '素顏': '素颜', '貓眼': '猫眼', '捲髮': '捲发',
                    '虎牙': '虎牙', 'C罩杯': 'C罩杯', 'I罩杯': 'I罩杯', '小麥色': '小麦色', '大陰蒂': '大阴蒂', '美乳': '美乳',
                    '巨乳': '巨乳', '豐滿': '丰满', '苗條': '苗条', '美臀': '美臀', '美腿': '美腿', '無毛': '无毛',
                    '美白': '美白', '微乳': '微乳', '性感': '性感', '高個子': '高', '爆乳': '爆乳', 'G罩杯': 'G罩杯',
                    '多毛': '多毛', '巨臀': '巨臀', '軟體': '软体', '巨大陽具': '巨大阳具', '長發': '长发', 'H罩杯': 'H罩杯',
                    '美脚': '美腿', '高个子': '高',

                    '舔陰': '舔阴', '電動陽具': '女优按摩棒', '淫亂': '淫乱', '射在外陰': '射在外阴', '猛烈': '猛烈', '後入內射': '后入内射',
                    '足交': '足交', '射在胸部': '射在胸部', '側位內射': '侧位内射', '射在腹部': '射在腹部', '騎乘內射': '骑乘内射', '射在頭髮': '射在头发',
                    '母乳': '母乳', '站立姿勢': '站立姿势', '肛射': '肛射', '陰道擴張': '阴道扩张', '內射觀察': '内射观察', '射在大腿': '射在大腿',
                    '精液流出': '精液流出', '射在屁股': '射在屁股', '內射潮吹': '内射潮吹', '首次肛交': '首次肛交', '射在衣服上': '射在衣服上', '首次內射': '首次内射',
                    '早洩': '早泄', '翻白眼': '翻白眼', '舔腳': '舔脚', '喝尿': '喝尿', '口交': '口交', '內射': '内射',
                    '自慰': '自慰', '後入': '后入', '騎乘位': '骑乘位', '顏射': '颜射', '口內射精': '口内射精', '手淫': '手淫',
                    '潮吹': '潮吹', '輪姦': '轮奸', '亂交': '乱交', '乳交': '乳交', '小便': '小便', '吸精': '吸精',
                    '深膚色': '深肤色', '指法': '手指插入', '騎在臉上': '颜面骑乘', '連續內射': '连续内射', '打樁機': '打桩机', '肛交': '肛交',
                    '吞精': '吞精', '鴨嘴': '鸭嘴', '打飛機': '打飞机', '剃毛': '剃毛', '站立位': '站立位', '高潮': '高潮',
                    '二穴同入': '二穴同时插入', '舔肛': '舔肛', '多人口交': '多人口交', '痙攣': '痉挛', '玩弄肛門': '玩弄肛门', '立即口交': '立即口交',
                    '舔蛋蛋': '舔蛋蛋', '口射': '口射', '陰屁': '阴屁', '失禁': '失禁', '大量潮吹': '大量潮吹', '69': '69',

                    '振動': '振动', '搭訕': '搭讪', '奴役': '奴隶', '打屁股': '打屁股', '潤滑油': '乳液',
                    '按摩': '按摩', '散步': '散步', '扯破連褲襪': '扯破连裤袜', '手銬': '手铐', '束縛': '捆绑', '調教': '调教',
                    '假陽具': '假阳具', '變態遊戲': '变态游戏', '注視': '注视', '蠟燭': '蜡烛', '電鑽': '电钻', '亂搞': '乱搞',
                    '摩擦': '摩擦', '項圈': '项圈', '繩子': '捆绑', '灌腸': '灌肠', '監禁': '监禁', '車震': '车震',
                    '鞭打': '鞭打', '懸掛': '悬挂', '喝口水': '喝口水', '精液塗抹': '精液涂抹', '舔耳朵': '舔耳朵', '女體盛': '女体盛',
                    '便利店': '便利店', '插兩根': '二穴同时插入', '開口器': '开口器', '暴露': '暴露', '陰道放入食物': '阴道放入食物', '大便': '大便',
                    '經期': '经期', '惡作劇': '恶作剧', '電動按摩器': '女优按摩棒', '凌辱': '凌辱', '玩具': '玩具', '露出': '露出',
                    '肛門': '肛门', '拘束': '拘束', '多P': '多P', '潤滑劑': '乳液', '攝影': '摄影', '野外': '野外',
                    '陰道觀察': '阴道观察', 'SM': 'SM', '灌入精液': '灌入精液', '受虐': '受虐', '綁縛': '捆绑', '偷拍': '偷拍',
                    '異物插入': '异物插入', '電話': '电话', '公寓': '公寓', '遠程操作': '远程操作', '偷窺': '偷窥', '踩踏': '踩踏',
                    '無套': '无套',

                    '企劃物': '企划物', '獨佔動畫': '独佔动画', '10代': '10代', '1080p': '', '人氣系列': '人气系列', '60fps': '',
                    '超VIP': '超VIP', '投稿': '投稿', 'VIP': 'VIP', '椅子': '椅子', '風格出眾': '风格出众', '首次作品': '首次作品',
                    '更衣室': '更衣室', '下午': '下午', 'KTV': 'KTV', '白天': '白天', '最佳合集': '最佳合集', 'VR': 'VR',
                    '動漫': '动漫',

                    '酒店': '酒店', '密室': '密室', '車': '车', '床': '床', '陽台': '阳台', '公園': '公园',
                    '家中': '家中', '公交車': '公交车', '公司': '公司', '門口': '门口', '附近': '附近', '學校': '学校',
                    '辦公室': '办公室', '樓梯': '楼梯', '住宅': '住宅', '公共廁所': '公共厕所', '旅館': '旅馆', '教室': '教室',
                    '廚房': '厨房', '桌子': '桌子', '大街': '大街', '農村': '农村', '和室': '和室', '地下室': '地下室',
                    '牢籠': '牢笼', '屋頂': '屋顶', '游泳池': '游泳池', '電梯': '电梯', '拍攝現場': '拍摄现场', '別墅': '别墅',
                    '房間': '房间', '愛情旅館': '爱情旅馆', '車內': '车内', '沙發': '沙发', '浴室': '浴室', '廁所': '厕所',
                    '溫泉': '温泉', '醫院': '医院', '榻榻米': '榻榻米',

                    '无码流出': '无码流出',
                    '折磨': '折磨', '嘔吐': '呕吐', '觸手': '触手', '蠻橫嬌羞': '蛮横娇羞', '處男': '处男', '正太控': '正太控',
                    '出軌': '出轨', '瘙癢': '瘙痒', '運動': '运动', '女同接吻': '女同接吻', '性感的x': '性感', '美容院': '美容院',
                    '處女': '处女', '爛醉如泥的': '烂醉如泥', '殘忍畫面': '残忍画面', '妄想': '妄想', '學校作品': '学校作品',
                    '粗暴': '粗暴', '姐妹': '姐妹', '雙性人': '双性人', '跳舞': '跳舞', '性奴': '性奴',
                    '倒追': '倒追', '性騷擾': '性骚扰', '其他': '其他', '戀腿癖': '恋腿癖', '偷窥': '偷窥', '花癡': '花痴',
                    '男同性恋': '男同性恋', '情侶': '情侣', '戀乳癖': '恋乳癖', '亂倫': '乱伦', '其他戀物癖': '其他恋物癖', '偶像藝人': '偶像艺人',
                    '野外・露出': '野外・露出', '獵豔': '猎艳', '女同性戀': '女同性恋', '企畫': '企画', '10枚組': '10枚组', '性感的': '性感',
                    '科幻': '科幻', '女優ベスト・総集編': '精选・综合', '温泉': '温泉', 'M男': 'M男', '原作コラボ': '原作协作',
                    '16時間以上作品': '16时间以上作品', 'デカチン・巨根': '巨大阴茎', 'ファン感謝・訪問': '粉絲感謝', '動画': '动画', 'ハーレム': '后宫',
                    '日焼け': '晒黑', '早漏': '早泄', 'キス・接吻': '接吻', '汗だく': '流汗', 'スマホ専用縦動画': '智能手机的垂直视频', 'Vシネマ': '电影放映',
                    'アニメ': '动漫', 'アクション': '动作',
                    'イメージビデオ（男性）': '男性', '孕ませ': '受孕', 'ボーイズラブ': '男同性恋',
                    'ビッチ': 'bitch', '特典あり（AVベースボール）': '特典', 'コミック雑誌': '漫画雑志', '時間停止': '时间停止',
                    'ナンパ': '猎艳', 'ハメ撮り': '第一人称摄影', '巨根': '巨大阴茎',

                    '黑幫成員': '黑帮成员', '童年朋友': '童年朋友', '公主': '公主', '亞洲女演員': '亚洲女演员', '伴侶': '伴侣', '講師': '讲师',
                    '婆婆': '婆婆', '格鬥家': '格斗家', '女檢察官': '女检察官', '明星臉': '明星脸', '女主人、女老板': '老板娘・女主人', '模特兒': '模特儿',
                    '美少女': '美少女', '車掌小姐': '车掌小姐',
                    '千金小姐': '千金小姐', '已婚婦女': '已婚妇女', '女醫生': '女医生', '各種職業': '各种职业',
                    '妓女': '妓女', '賽車女郎': '赛车女郎', '女大學生': '女大学生', '展場女孩': '展场女孩', '母親': '母亲',
                    '家教': '家教', '护士': '护士', '蕩婦': '荡妇', '黑人演員': '黑人演员', '女生': '女生', '女主播': '女主播',
                    '高中女生': '高中女生', '服務生': '服务生', '魔法少女': '魔法少女', '學生（其他）': '其他学生', '動畫人物': '动画人物', '遊戲的真人版': '游戏真人版',
                    '超級女英雄': '超级女英雄', '烂醉如泥的': '烂醉如泥',

                    '女戰士': '女战士', '及膝襪': '及膝袜', '娃娃': '娃娃', '女忍者': '女忍者',
                    '女裝人妖': '女装人妖', '猥褻穿著': '猥亵穿着', '貓耳女': '猫耳女', '女祭司': '女祭司',
                    '泡泡襪': '泡泡袜', '裸體圍裙': '裸体围裙', '迷你裙警察': '迷你裙警察',
                    '身體意識': '身体意识', 'OL': 'OL', '和服・喪服': '和服・丧服', '體育服': '体育服', '内衣': '内衣',
                    '學校泳裝': '学校泳装', '女傭': '女佣', '校服': '校服',
                    '泳裝': '泳装', '哥德蘿莉': '哥德萝莉', '和服・浴衣': '和服・浴衣',

                    '超乳': '超乳', '肌肉': '肌肉', '乳房': '乳房', '嬌小的': '娇小的', '高': '高',
                    '變性者': '变性人', '胖女人': '胖女人', '成熟的女人': '成熟的女人',
                    '蘿莉塔': '萝莉塔', '貧乳・微乳': '贫乳・微乳',

                    '顏面騎乘': '颜面骑乘', '食糞': '食粪', '手指插入': '手指插入',
                    '女上位': '女上位', '拳交': '拳交', '深喉': '深喉',
                    '排便': '排便', '飲尿': '饮尿',  '濫交': '滥交',
                    '放尿': '放尿', '打手槍': '打手枪',
                    '顏射x': '颜射', '中出': '中出', '肛内中出': '肛内中出',

                    '女優按摩棒': '女优按摩棒', '子宮頸': '子宫颈', '催眠': '催眠', '乳液': '乳液',
                    '插入異物': '插入异物', '紧缚': '紧缚', '強姦': '强奸', '藥物': '药物', '汽車性愛': '汽车性爱',
                    '糞便': '粪便',  '跳蛋': '跳蛋', '緊縛': '紧缚', '按摩棒': '按摩棒',
                    '性愛': '性爱',  '逆強姦': '逆强奸',

                    '合作作品': '合作作品', '恐怖': '恐怖', '教學': '教学', 'DMM專屬': 'DMM专属', 'R-15': 'R-15',
                    'R-18': 'R-18', '戲劇': '戏剧', '3D': '3D', '特效': '特效', '故事集': '故事集', '限時降價': '限时降价',
                    '複刻版': '复刻版', '戲劇x': '戏剧', '戀愛': '恋爱', '高畫質': '高画质', '主觀視角': '主观视角', '介紹影片': '介绍影片',
                    '4小時以上作品': '4小时以上作品', '薄馬賽克': '薄马赛克', '經典': '经典', '首次亮相': '首次亮相', '數位馬賽克': '数位马赛克',
                    '纪录片': '纪录片', '國外進口': '国外进口', '第一人稱攝影': '第一人称摄影', '業餘': '素人', '局部特寫': '局部特写', '獨立製作': '独立制作',
                    'DMM獨家': 'DMM独家', '單體作品': '单体作品', '合集': '合集', '高清': '高清', '字幕': '字幕', '天堂TV': '天堂TV',
                    'DVD多士爐': 'DVD多士炉', 'AV OPEN 2014 スーパーヘビー': 'AVOPEN2014超级重量级',
                    'AV OPEN 2014 ヘビー級': 'AVOPEN2014重量级',
                    'AV OPEN 2014 ミドル級': 'AVOPEN2014中量级',
                    'AV OPEN 2015 マニア/フェチ部門': 'AVOPEN2015爱好・恋物癖部门', 'AV OPEN 2015 熟女部門': 'AVOPEN2015熟女部门',
                    'AV OPEN 2015 企画部門': 'AVOPEN2015企画部门', 'AV OPEN 2015 乙女部門': 'AVOPEN2015少女部门',
                    'AV OPEN 2015 素人部門': 'AVOPEN2015素人部门', 'AV OPEN 2015 SM/ハード部門': 'AVOPEN2015SM・真实部门',
                    'AV OPEN 2015 女優部門': 'AVOPEN2015女优部门', 'AVOPEN2016人妻・熟女部門': 'AVOPEN2016人妻・熟女部门',
                    'AVOPEN2016企画部門': 'AVOPEN2016企画部门', 'AVOPEN2016ハード部門': 'AVOPEN2016真实部门',
                    'AVOPEN2016マニア・フェチ部門': 'AVOPEN2016爱好・恋物癖部门', 'AVOPEN2016乙女部門': 'AVOPEN2016少女部门',
                    'AVOPEN2016女優部門': 'AVOPEN2016女优部门', 'AVOPEN2016ドラマ・ドキュメンタリー部門': 'AVOPEN2016戏剧・纪录片部门',
                    'AVOPEN2016素人部門': 'AVOPEN2016素人部门', 'AVOPEN2016バラエティ部門': 'AVOPEN2016综艺部门',
                    'VR専用': 'VR専用', '堵嘴·喜劇': '喜剧', '性別轉型·女性化': '性别转型·女性化',
                    '為智能手機推薦垂直視頻': '为智能手机推荐垂直视频', '設置項目': '设置项目', '迷你係列': '迷你系列',
                    '體驗懺悔': '体验忏悔', '黑暗系統': '黑暗系统', 'AVOPEN2016业余部门': 'AVOPEN2016素人部门', '业余': '素人',
                    'AVOPEN2016爱好/恋物癖部门': 'AVOPEN2016爱好・恋物癖部门', 'AV OPEN 2016 疯狂/恋物癖部门':'AVOPEN2016爱好・恋物癖部门',
                    'AVOPEN2016疯狂/恋物癖部门':'AVOPEN2016爱好・恋物癖部门', 'AVOPEN2017实干部门':'AVOPEN2017真实部门',

                    'オナサポ': '手淫', 'アスリート': '运动员', '覆面・マスク': '面具', 'ハイクオリティVR': '高品质VR',
                    'アクメ・オーガズム': '极致・性高潮', '花嫁': '花嫁', 'デート': '约会', '軟体': '软体', '娘・養女': '养女', 'スパンキング': '打屁股',
                    'スワッピング・夫婦交換': '夫妇交换', '部下・同僚': '下属・同事', '胸チラ': '露胸', 'バック': '背后',
                    '男の潮吹き': '男人高潮', '女上司': '女上司', 'セクシー': '性感', '受付嬢': '接待员', 'ノーブラ': '不穿胸罩',
                    '白目・失神': '翻白眼・失神', 'M女': 'M女', '女王様': '女王', 'ノーパン': '不穿内裤', 'セレブ': '名流', '病院・クリニック': '医院诊所',
                    'お風呂': '洗浴', '叔母さん': '叔母', '罵倒': '辱骂', 'お爺ちゃん': '爷爷', '逆レイプ': '逆强奸',
                    'ディルド': '假阳具', 'ヨガ': '瑜伽', '飲み会・合コン': '酒会・联谊会', '部活・マネージャー': '社团・经理', 'お婆ちゃん': '外婆',
                    'ビジネススーツ': '制服外套', 'チアガール': '啦啦队', 'ママ友': '主妇之友', '妄想族': '妄想族', '蝋燭': '蜡烛', '鼻フック': '鼻钩',
                    '放置': '放置', 'サンプル動画': '范例影片', 'サイコ・スリラー': '心理・惊悚片', 'ラブコメ': '爱情喜剧', 'オタク': '御宅族',
                    'ロングヘアー': '长发',

                    ## JAVDB
                    '可播放': '可播放', '可下載': '可下载', '含字幕': '含字幕', '單體影片': '单体影片', '含預覽圖': '含预览图',
                    '含預覽視頻': '含预览视频', '淫亂，真實': '淫乱・真实', '男同性戀': '男同性恋',
                    '韓國': '韩国', '形象俱樂部': '形象俱乐部', '友誼': '友谊', '亞洲': '亚洲',
                    '暗黑系': '暗黑系', '天賦': '天赋', '被外國人幹': '被外国人干',
                    '魔鬼系': '魔鬼系', '奴隸': '奴隶', '白天出軌': '白天出轨', '流汗': '流汗',
                    '曬黑': '晒黑', '正常': '正常', '新娘，年輕妻子': '新娘・年轻妻子', '飛特族': '飞特族', '奇異的': '奇异的',  '藝人': '艺人',
                    '痴漢': '痴汉', '大小姐': '大小姐', '角色扮演者': '角色扮演者', '妹妹': '妹妹',
                    '禮儀小姐': '礼仪小姐', '老闆娘，女主人': '老板娘・女主人', '其他學生': '其他学生',
                    '運動短褲': '运动短裤', '和服，喪服': '和服・丧服', '女兒': '女儿', '年輕女孩': '年轻女孩',
                    '制服外套': '制服外套', '修女': '修女', 'COSPLAY服飾': 'Cosplay服饰',
                    '浴衣': '浴衣', '蘿莉角色扮演': '萝莉角色扮演',
                    '巨大陰莖': '巨大阴茎', '平胸': '平胸', '美腳': '美腿',
                    '巨大屁股': '巨大屁股', '瘦小身型': '瘦小身型',
                    '二穴同時挿入': '二穴同时插入',  '接吻': '接吻', '騎乗位': '骑乘位', '捆綁': '捆绑',
                    '精選，綜合': '精选・综合', '戶外': '户外', '導尿': '导尿', '脫衣': '脱衣',
                    '行動': '行动', '成人電影': '成人电影', '綜合短篇': '综合短篇', '滑稽模仿': '滑稽模仿',
                    '男性': '男性', '冒險': '冒险', '模擬': '模拟', '愛好，文化': '爱好・文化',
                    '懸疑': '悬疑', '美少女電影': '美少女电影', '感官作品': '感官作品', '觸摸打字': '触摸打字',
                    '紀錄片': '纪录片', '去背影片': '去背影片',
                    '戰鬥行動': '战斗行动', '16小時以上作品': '16小时以上作品',  '重印版': '重印版',
                    '歷史劇': '历史剧', '寫真偶像': '写真偶像',
                    '西洋片': '西洋片', '45分鍾以內': '45分钟以内', '45-90分鍾': '45-90分钟', '90-120分鍾': '90-120分钟',
                    '120分鍾以上': '120分钟以上',

                    # FANZA
                    '人妻・主婦': '已婚妇女', '女子校生': '高中女生', '幼なじみ': '童年朋友',
                    'キャンギャル': '展场女孩', '盗撮・のぞき': '偷窥', 'コミック': '漫画',
                    '寝取り・寝取られ・NTR': 'NTR', 'バスガイド': '巴士导游', 'スチュワーデス': '空中小姐', 'ドール': '娃娃',
                    'ヘルス・ソープ': '泡沫浴', '未亡人': '寡妇', 'マッサージ・リフレ': '按摩', '不倫': '出轨', 'お姫様': '大小姐',
                    '若妻・幼妻': '新娘・年轻妻子', 'モデル': '模特儿', '面接': '面试', 'メイド': '女佣', 'ホテル': '酒店',
                    '黒人男優': '黑人演员', '小柄': '娇小', '筋肉': '肌肉', '巨尻': '巨大屁股', 'アジア女優': '亚洲女演员',
                    'そっくりさん': '明星脸', '長身': '高', 'スレンダー': '苗条', '女装・男の娘': '女装人妖', '処女': '处女',
                    '童貞': '童贞', '妊婦': '孕妇', '白人女優': '白人', 'パイパン': '无毛',
                    '学生服': '学生服', 'ミニ系': '萝莉塔', 'ぽっちゃり': '胖女人',
                    'コスプレ': 'Cosplay', '競泳・スクール水着': '学校泳装',
                    '体操着・ブルマ': '运动短裤', 'Cosplay服饰': 'Cosplay服饰',
                    'チャイナドレス': '中国服饰', 'ニーソックス': '过膝袜',
                    '裸エプロン': '裸体围裙', 'バニーガール': '兔女郎', 'パンスト・タイツ': '连裤袜',
                    '巫女': '巫女', '水着': '泳装', 'ミニスカ': '超短裙', 'ミニスカポリス': '超短裙警察', 'めがね': '眼镜',
                    'ランジェリー': '内衣', 'ルーズソックス': '泡泡袜', 'レオタード': '紧身衣',
                    'アクション・格闘': '战斗行动', '脚フェチ': '恋腿癖', 'イメージビデオ': '写真视频',
                    '淫乱・ハード系': '淫乱・真实', '学園もの': '学校作品',
                    '局部アップ': '局部特写', '巨乳フェチ': '恋乳癖',
                    'クラシック': '经典', 'ゲイ': '男同性恋', 'レースクィーン': '女王',
                    '残虐表現': '残忍画面', '尻フェチ': '屁股', '女性向け': '女性向',
                    'スポーツ': '运动', 'その他フェチ': '其他恋物癖',
                    '単体作品': '单体作品', 'ダーク系': '暗黑系', 'ダンス': '跳舞', '着エロ': '猥亵穿着', 'デビュー作品': '首次亮相',
                    '特撮': '特效', 'ドキュメンタリー': '纪录片', 'ドラマ': '戏剧',
                    'パンチラ': '内衣', 'ファンタジー': '幻想', '復刻': '复刻',
                    'ベスト・総集編': '精选・综合', 'ホラー': '恐怖', 'ごっくん': '吞精',
                    '洋ピン・海外輸入': '国外进口', 'レズ': '女同性恋', '恋愛': '恋爱',
                    '足コキ': '足交', 'アナルセックス': '肛交', '異物挿入': '插入异物', 'オナニー': '手淫', 'おもちゃ': '玩具',
                    '浣腸': '灌肠', '鬼畜': '鬼畜', 'くすぐり': '痒痒',
                    '拷問': '拷问', '潮吹き': '潮吹', '縛り・緊縛': '紧缚', '脱糞': '排便', '手コキ': '打手枪',
                    '電マ': '女优按摩棒', 'パイズリ': '乳交', 'フィスト': '拳交', 'フェラ': '口交', 'ぶっかけ': '颜射', '放尿・お漏らし': '放尿',
                    'レズキス': '女同接吻', 'ローション・オイル': '乳液', 'インディーズ': '印度', '期間限定セール': '限时特卖',
                    'イラマチオ':'深喉', '美尻':'美臀', '指マン': '手指插入', '手マン': '手指插入', 'ローション': '乳液',

                    # mgstage
                    'ギャル': '辣妹', 'カップル': '情侣', 'エステ・マッサージ': '美容・按摩',
                    '3P・4P': '3P・4P', '中出し': '中出',
                    'キャバ嬢・風俗嬢': '公主', '童顔': '童颜',
                    '職業色々': '各种职业', '配信専用': '配信专用', 'アイドル・芸能人': '偶像・艺人', '偶像艺人': '偶像・艺人',
                    'アナル': '肛门', '姉・妹': '姐妹', 'Eカップ': 'E罩杯', 'イタズラ': '恶作剧',
                    '色白': '白皙', '淫語モノ': '淫语',
                    'インストラクター': '讲师', 'ウェイトレス': '女服务生', 'Hカップ': 'H罩杯', 'Fカップ': 'F罩杯', 'お母さん': '母亲',
                    '女将・女主人': '老板娘・女主人', 'お嬢様・令嬢': '大小姐', 'お姉さん': '姐姐', 'オモチャ': '玩具',
                    '女戦士': '女战士', '女捜査官': '女搜查官', 'カーセックス': '汽车性爱', '介護': '看护',
                    '格闘家': '格斗家', '家庭教師': '家庭教师', '看護婦・ナース': '护士',
                    'キス': '接吻', '着物・浴衣': '和服・浴衣', '近親相姦': '近亲通奸',
                    '金髪・ブロンド': '金发', '逆ナン': '倒追', '義母': '后母', 'ゲイ・ホモ': '同性恋',
                    '口内射精': '口内射精', '口内発射': '口内发射',
                    'コンパニオン': '伴侣', '羞恥・辱め': '羞辱', '主観': '主观视角',
                    'ショタ': '正太控', '女医': '女医生', '女子アナ': '女主播', '女子大生': '女大学生',
                    'Gカップ': 'G罩杯', 'スチュワーデス・CA': '空中小姐', '清楚': '清秀',
                    'Dカップ': 'D罩杯', '泥酔': '烂醉如泥', '盗撮': '偷拍', 'ドラッグ・媚薬': '媚药', 'ニューハーフ': '变性者',
                    'スケベな淫乱淑女': '淫乱的美女', 'バイブ': '按摩棒', 'ショートヘアー': '短发', 'メガネ':'眼镜', '寝取り・寝取られ': 'NTR',
                    '顔面騎乗':'颜面骑乘',

                    #fc2
                    'フェチ': '恋物癖', '自分撮り': '自拍', 'OL・お姉さん': 'OL姐姐', '３P・乱交': '3P・乱交', '海外': '海外',
                    'BL': 'BL', 'アダルト': '成人', 'コスプレ・制服':'Cosplay・制服', '個人撮影': '个人摄影', '初撮り': '初次拍摄',

                    #javlib
                    '和服、喪服': '和服・丧服', '心理、驚悚片': '心理・惊悚片', '愛好、文化': '爱好・文化', '新娘、年輕妻子': '新娘・年轻妻子',
                    '淫亂、真實': '淫乱・真实', '精選、綜合': '精选・综合', '老闆娘、女主人': '老板娘・女主人', '给女性观众': '女性向',
                    '和服、丧服': '和服・丧服', '心理、惊悚片': '心理・惊悚片', '爱好、文化': '爱好・文化', '新娘、年轻妻子': '新娘・年轻妻子',
                    '淫乱、真实': '淫乱・真实', '精选、综合': '精选・综合', '老板娘、女主人': '老板娘・女主人', '給女性觀眾': '女性向',
                    }
        try:
            return dict_gen[tag]
        except:
            return tag
    else:
        return tag
