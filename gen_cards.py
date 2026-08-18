#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 生成小红书卡片 cards.html —— 网页内容原样流式分页，目标 18 页

import math
import re

FLAG = ('<span style="background:var(--flag-blue)"></span>'
        '<span style="background:var(--flag-white)"></span>'
        '<span style="background:var(--flag-red)"></span>'
        '<span style="background:var(--flag-yellow)"></span>'
        '<span style="background:var(--flag-green)"></span>')

# ---- 网页内容块，原样搬运 ----

KEYS = ('<ul class="card__keys"><li><span>海拔决定秩序</span><strong>一 高原的秩序</strong></li> <li><span>山河决定地图</span><strong>二 山河的地图</strong></li> <li><span>车是腿，慢是快</span><strong>三 路上的驾驶学</strong></li> <li><span>看墙色认教派</span><strong>四 信仰的世界</strong></li> <li><span>手艺是还在运转的产业</span><strong>五 手艺的文明</strong></li> <li><span>材料决定房子</span><strong>六 建筑的方言</strong></li></ul>')

PAGE1 = [
  ('kicker', '李大妈的自驾路书'),
  ('h1', '<strong>川西自驾行前笔记</strong>'),
  ('intro', '川西自驾是一门功课：海拔怎么排、山河怎么切、车怎么开、信仰怎么认、手艺在哪儿、房子为什么长这样。'),
  ('meta', '我习惯在行前把零碎信息检索、整理成笔记，当出行线索。笔记更新于2026年8月18日。封路、天气、信号等信息随季节变化，出发前以官方信息为准。'),
  ('h2', '开篇\u3000六章速览'),
  ('keys', KEYS),
]

BODY_STREAM = [
  ('h3', '与人相处'),
  ('p', '<strong>牧民。</strong> 牛羊是牧民的主要家当。遇到牧群，放慢车速、不鸣笛，等它们过。拍牧民和牲畜，先打招呼再举相机。牧场的帐篷和围栏，不随便进。'),
  ('p', '<strong>匠人。</strong> 进工坊先问能不能看，问手艺、问工序，匠人愿意聊就聊。工具和材料不上手碰。买现货，半成品和机压仿品不碰。'),
  ('p', '<strong>僧侣。</strong> 称呼用「师父」或「上师」。进大殿脱帽、轻声、顺时针走，不拍照、不指佛像。法会时安静看，不打断、不围观起哄。'),
  ('p', '<strong>司机和本地人。</strong> 见面一句「扎西德勒」，气氛就开了。问路、问价，态度客气，多数人都愿意答。高原上的人大多直接，不绕弯，打交道也直接。'),
  ('p', '<strong>买东西。</strong> 讲好价就认，不反复缠价。看上了再还价，压完不买最伤和气。'),
  ('p', '<strong>拍照。</strong> 拍人先问，拍寺院内部和法会先看有没有禁令。相机镜头对着人的时候，先问一句，多数人会同意的。'),
  ('h2', '高原的秩序'),
  ('lead', '海拔决定秩序。'),
  ('p', '进川西先认海拔。<strong>3000米是一道门槛</strong>，多数人的高反从这里开始。行程按海拔排，不按景点排：一天的路程控制在两三小时山路，下午留白看天，天气不对就提前收车。景点不会消失，路况和天气才是当天的变量。'),
  ('p', '窗口期。<strong>5到6月、9到10月中是全年最稳的时段</strong>。雨季6到8月以夜雨为主，白天多数能走。冬季也能走，但救援半径长，一台车陷在无人垭口，代价远超省下的时间。'),
  ('p', '防高反。从低到高慢慢爬，头两天不在3500米以上过夜。氧气不足的典型信号是头痛、睡不着、没胃口，多数人两三天能适应。乙酰唑胺遵医嘱提前吃，布洛芬缓解头痛，红景天提前一周吃，只作辅助。指夹式血氧仪测血氧，<strong>掉到90%以下就停，不硬撑</strong>。夜里头痛加重、白天精神很差、走路发飘，是危险信号，撤到低海拔。'),
  ('p', '补给认准县城。<strong>进县城加满油</strong>，一离开县城就默认补给消失，往深处走，一律当天往返。'),
  ('p', '离线地图出发前下好，<strong>自救物资可以不用，但不能没有</strong>。冬季走，车上常备防滑链。'),
  ('h2', '山河的地图'),
  ('lead', '山河决定地图。山脉怎么切，路就怎么修。'),
  ('p', '川西怎么来的。约4000万到5000万年前，印度板块撞上欧亚板块，把一片浅海抬成陆地，就是青藏高原，川西在高原的东南缘。碰撞到现在没停，高原还在缓慢升高。'),
  ('p', '山脉全是南北走向。横断山把川西切成一列列山岭，从东往西：邛崃山，四姑娘山在主脊上；大雪山，贡嘎山海拔7508.9米，蜀山之王；沙鲁里山；雀儿山。山与山之间夹着河谷，路顺着河谷修，镇子落在河谷里。<strong>川西的聚落跟着山河走，不跟着行政区划走。</strong>'),
  ('p', '河流往三处去。东部是大渡河，小金、金川、丹巴都在它的水系里；雅砻江从甘孜县城边流过；金沙江是德格的西界，德格县城在金沙江东岸。三条江各走各的，最后都汇进长江。'),
  ('p', '海子是古冰川留下的湖。冰期冰川刨出的洼地积水成湖，理塘到稻城之间的海子山，古冰川退去后留下1145个高原湖泊。单个看，康定的木格措、九龙的伍须海、巴塘的措普湖各有各的颜色，德格雀儿山下的新路海紧挨着雪峰。'),
  ('p', '川西地震多，因为它在鲜水河断裂带上。这条断裂带从中部纵贯，历史上强震不断。对旅行者，最实在的是<strong>路况随时可能因塌方管制</strong>；很多陡崖和河谷的走向，就是断裂带运动的痕迹。'),
  ('p', '植被随海拔分层，从山谷到垭口一路换。2500米以下是针阔混交林；2500到3500米是云杉冷杉的针叶林，高山杜鹃夹在林里；3500到4500米是高山灌丛和高山草甸，冬虫夏草、雪茶都长在这一层；4500米以上是流石滩，雪莲贴着碎石长。<strong>同一条路翻几座山，一天走完四个植被带，别处南北几千公里才有的植被变化，在这里按海拔一层层排</strong>。'),
  ('p', '吃的也跟海拔走。青稞是高原的当家作物，炒熟磨成糌粑，拌上酥油茶捏成团，是藏人的日常主食；酥油茶用砖茶和酥油熬，热量高、解渴御寒，当地有<strong>「宁可三日无肉，不可一日无茶」</strong>的说法。牦牛在海拔3500米以上放养，肉干、火锅、炖汤都常见；血肠是待客的上等菜，牛血或羊血和肉丁灌进小肠煮熟。松茸这类菌子长在森林里，集中在金沙江、雅砻江、大渡河上中游的高山峡谷，夏秋雨后出得多，炖鸡、涮锅都常吃。这些不用刻意找，路边饭馆的菜单上就有。'),
  ('h2', '路上的驾驶学'),
  ('lead', '车是腿，慢是快。一半技术，一半克制。'),
  ('p', '川西路上要让的，是大货车和牧民的牛羊。弯道不超车。<strong>让路是这条路的默认礼节</strong>。'),
  ('p', '高原开车有两个隐性风险。长下坡一直踩刹车会热衰减，要用低挡位和发动机制动；超车动力衰减，要留出比平原长得多的余量。冰雪路面上，四驱也一样打滑，<strong>慢才是安全</strong>。'),
  ('p', '手机信号在县城和景区都有，支线基本没有。<strong>离开主路之前，给家人或朋友发一个位置</strong>，让他们知道人在哪。进了支线，信号就断了，把没信号当默认状态。应急手段：中国电信有手机直连卫星业务，华为、小米等部分手机开通后，不换卡不换号就能在无信号区通话、发定位；雅安318自驾大本营有全国首个城市卫星服务站，可以租天通卫星设备，按天十元左右。'),
  ('h3', '加油'),
  ('p', '加油站集中在县城和几个大镇，见油就加。认准中石油、中石化，避开私人黑站。理塘到稻城之间约200公里没有加油站，G317甘孜到德格一带靠马尼干戈这类节点补给。<strong>油箱过半就找下一个县城</strong>。'),
  ('h3', '充电'),
  ('p', '川西这两年变化快。2025年6月甘孜州18个公路养护站和14个快充站投运，理塘到稻城段充电桩最大间距125公里；318沿线超300个充电桩，快充占七成以上。密度从东往西递减：成都到康定每30到50公里一个快充；康定、新都桥、雅江、理塘每80到150公里；理塘往稻城亚丁、新都桥往塔公八美每150到200公里。冷嘎措、格聂、若尔盖穿越段还是盲区。实际体验要打折：约一成五的桩故障或被燃油车占位，节假日热门站排队可能超一小时。高原续航缩水约三四成。<strong>电量低于三成就找桩</strong>，进景区前在县城充到八成以上。查桩用特来电、国网e充电、星星充电的App，或高德的新能源模式。'),
  ('h3', '封路信息'),
  ('p', '两类封路最常见：汛期6到8月塌方落石，抢修期间半幅放行或管制；冬季11月到次年3、4月冬管，比如九绵高速夜间20点到次日8点禁行，夹金山段整个冬天双向禁行，理小路冬天全段禁行。截至2026年8月17日，阿坝州正实行货车临时管制（过境4轴及以上货车白天7点到21点禁行），同时处在汛期，山洪预警可能随时发布。<strong>G317马尔康到观音桥段，自2025年11月红旗特大桥垮塌后一直中断</strong>，绕行走壤塘、阿坝、红原方向，约多3小时；官方便道工程预计2026年9月底至10月初通车。官方渠道：阿坝州政府官网阿坝路况专栏、四川发布和成都发布公众号、高速救援12122、报警96122。<strong>官方路况和高德，出发当天交叉核对</strong>。'),
  ('h2', '信仰的世界'),
  ('lead', '看墙色，认教派。'),
  ('p', '川西在藏文化版图里的位置。藏区习惯分成三大块：拉萨一带的卫藏，青海甘肃的安多，还有以甘孜、昌都为核心的康巴。康巴人性格外放，「康巴汉子」的名声就是这么来的。和卫藏、安多不同，川西<strong>没有哪个教派一家独大</strong>。甘孜州登记的藏传佛教寺院有515座，宁玛、格鲁、萨迦、噶举、苯教五大教派齐全，哪个都占不到一半。一次看全这些派别，别处凑不齐。'),
  ('p', '认教派，看寺庙外墙的颜色。宁玛派叫<strong>红教</strong>，是最古老的派别，多随牧区分布。萨迦派叫<strong>花教</strong>，寺墙刷红、白、黑三色条纹，据说是文殊、观音、金刚手三位菩萨的象征。噶举派叫<strong>白教</strong>，叫法来自早期僧人穿白衣的传承，四川藏区的祖寺是德格的八邦寺。格鲁派叫<strong>黄教</strong>，传入最晚，理塘的长青春科尔寺是康区最早的格鲁派寺院。还有苯教，比藏传佛教更古老的本地信仰，没有对应的颜色称呼，它在川西的地位比在西藏老家还高，<strong>阿坝县的郎依寺，是国内外现存规模最大的苯教寺院</strong>，阿坝金川的雍忠拉顶寺一带被称为「第二象雄」——也就是苯教文化的第二个中心。'),
  ('p', '最特别的是德格。历代德格土司推行「不分教派、一律扶持」的政策，硬是把五大教派全留在自家地盘上，这在藏区很少见，<strong>德格也因此成了藏文化的三大中心之一</strong>。'),
  ('p', '路边的符号，各有含义。经幡也叫风马旗，五种颜色对应蓝天、白云、红火、江河、大地，挂在山顶风口，<strong>藏人相信风吹动一次等于诵经一次</strong>。玛尼堆是刻了六字真言的石块堆，路人经过会念着真言添一块石头，不搬走当纪念品。白塔源于古印度的覆钵式佛塔，路过捡块石头放上去，或献条哈达许愿。德格佐钦寺的白塔是尼泊尔风格，方形塔顶四面画着佛眼，<strong>和加德满都的博达哈大佛塔同一形制</strong>，博达哈是全世界最大的覆钵塔。转经筒里装着经文，转一圈等于念诵一遍，藏人转经廊、转佛塔、转寺院都是这个逻辑。六字真言「唵嘛呢叭咪吽」是观世音菩萨的总持咒，被看作雪域佛法最根本的念诵。'),
  ('p', '和信仰打交道，有几条规矩：<strong>绕行一律顺时针，只有苯教是逆时针</strong>。磕长头是身敬、语敬、意敬三者合一，额头叩地的瞬间，心里同时念咒、观想，这是他们能磕几千公里的原因。煨桑是烧香柏枝，敬献给神佛的香火，也是祈愿的仪式。献哈达要看对象：白色最普遍，黄色献给活佛和高僧，五彩哈达被视为菩萨的衣裳，只在隆重场合用。<strong>哈达只递到对方手里，不能挂脖子上，只有长辈给晚辈才往脖子上搭</strong>。天葬是藏人把遗体布施给神鹰，被认为是最高的舍身布施，<strong>全程严禁围观、拍照，当地有明文规定，连打听都不要</strong>。另有几条硬规矩：<strong>不摸别人的头，佛像、唐卡、经书不指</strong>，非要指就五指并拢、手心朝上，不进人家供奉的佛堂，不取献给塔上的供品，过门槛不踩。'),
  ('p', '川西的佛学院，把藏地的学问办在草原和山沟里。寺院的分科叫「五明」：工巧明是工艺，医方明是医学，声明是语言文字，因明是逻辑论辩，内明是佛学；再加上修辞、辞藻、韵律、戏剧、历算五科，合称「十明」。色达的喇荣、白玉的亚青、德格的佐钦，都是宁玛派的大佛学院，学通五明的僧人，藏语称「班智达」。'),
  ('p', '三大佛学院里，亚青寺最出名的是觉姆岛。它在白玉县昌台草原，1985年由阿秋仁波切创建，是宁玛派的修行地。昌曲河绕寺流过，把女众修行区围成一座河心岛，就是「觉姆岛」，岛上密布上万间绛红色小木屋，住的是觉姆，也就是藏地的女性出家人。屋子是她们自己伐木、夯土、一钉一板搭起来的，每间不足十平方米，屋顶压着塑料布和泥土。<strong>成年男性不上觉姆岛</strong>，岛外的男众不过桥。每年入冬，觉姆们钻进一间仅容一人的小屋，百日闭关，黄昏后才走出。山坡上立着一尊巨大的莲花生大师金像。'),
  ('h2', '手艺的文明'),
  ('lead', '还在挣钱的传承，才是活传承。'),
  ('p', '麦宿在德格县金沙江东岸的河谷里，六千多居民有两千多位工匠，分布在三十多个工坊，做十六种手工艺。黑陶、铜铸、唐卡、木雕、藏香、藏纸、藏戏面具、金银加工、牛羊毛编织，被称为「中国藏族传统手工艺之乡」。<strong>它不是摆在展柜里的「非遗秀」</strong>。寺庙要佛像法器，本地人过日子要锅碗和经堂装饰，订单一直不断。麦宿进出不易，外头的东西不好运进来，要用的、要供的都得自己做，手艺就一代代传了下来。最出名的铜铸佛像，老匠人夏雷尼玛的鎏金铜是内地近乎失传的古法，他做的佛像因为工艺古朴精良，常被人冒充古董倒卖，甚至流到了国外。他女儿拍的《麦宿泥塑》纪录片，拿过国际手工艺视频大赛的一等奖。钦乐工坊还在用砂模、失蜡法铸利玛铜。后来县里建了扶贫车间，挂出「麦宿手造」的品牌，2024年还到成都开了集市。从一块铜皮到一尊佛像，工坊里能看到整套流程。手工工坊有现货，机压翻模的是仿品。'),
  ('p', '白玉河坡号称「格萨尔王的兵器库」，1300多年前就开始铸兵器，现在是国家级非遗「藏族金属锻造技艺」的代表，白玉藏刀最有名。13个行政村、230多家非遗工坊，<strong>是全国最大的藏族金属锻造群落</strong>，年订单超过1200万元。2025年8月，河坡手工艺文旅体融合园区开园，建了藏族金工博物馆。'),
  ('p', '壤塘在阿坝州，藏语意思是「财神居住的地方」，核心是觉囊文化。2010年建起第一个觉囊唐卡传习所，<strong>免费教贫困家庭的青少年，一学六到八年</strong>。现在有20多个传习所、3项国家级非遗，壤巴拉非遗传习创业园8万多平方米，聚集唐卡、藏医药、藏陶、藏毯等16类手艺，2024年产值两千多万元。县里还在北京、上海、成都、深圳设了传习基地，60名学员接过故宫藏品唐卡复制的项目。觉囊唐卡工坊进了全国「非遗工坊典型案例」。唐卡的颜色从矿石里磨出来：蓝用青金石，红用朱砂，绿用孔雀石，金是真金箔。矿物不含有机成分，见光不褪色，<strong>一张唐卡放几百年，颜色还是那样</strong>。'),
  ('p', '德格印经院本身是一门还在运转的印刷产业。1729年建，藏了32万余块雕版，其中古旧印版22.8万块，<strong>是全世界手工木刻印版藏量最多的地方</strong>。经版内容不止经文：宗教、历史、医学、天文历算、文学、艺术都有，「藏文化大百科全书」这个外号就是这么来的。'),
  ('p', '印刷是流水线工序：裁纸、泡纸、兑墨、研朱砂、印刷、晾晒、分页、核对、装订，十几道。印经书三人一组，一高一矮相对坐，高者固定印纸刷墨，矮者递纸、用卷布滚筒滚印，配合熟练的一天印2400张4800页。材料也讲究：<strong>藏纸用瑞香狼毒草的根，含毒，虫不蛀、鼠不咬</strong>；雕版用海拔3000米以上的红桦木，微火熏烤、水煮、烘干，刻好的版要过12次审校，在酥油里泡一天才算完成。'),
  ('p', '<strong>印经院至今没通电</strong>，是怕火险伤经版，游客就着天光看印刷间。古旧经版现在限量印刷，近十年复刻了2.2万余块新版供印，古版封存，印版修复每年补刻230余块。2006年它进了国家级非遗，2009年被联合国教科文组织列入人类非物质文化遗产代表作名录。'),
  ('h2', '建筑的方言'),
  ('lead', '材料决定房子。'),
  ('p', '川西的民居，藏寨是主流。石、木、土，山上出什么料就盖什么房，材料定了骨架，骨架定了长相。'),
  ('p', '嘉绒藏寨与古碉，在丹巴一带最出名。石木结构，片石砌墙，房子依山势叠在山坡上，顶层外缘围一圈黄、黑、白三色带。甲居藏寨评上「中国最美的六大乡村古镇」之首，中路藏寨海拔2100米。丹巴古碉鼎盛时号称「千碉之国」，梭坡乡的古碉群，<strong>是全世界古碉最密集的地方</strong>。碉楼按功能分要隘碉、烽火碉、寨碉、家碉四类，还分雌雄。'),
  ('p', '藏寨的结构，从下到上一条线。以甲居藏寨为例，石木结构，三到四层，各层逐层内收，顶上留出晒粮平台。底层圈养牲畜兼做仓库，畜圈的门和人进出的门分开；二层是锅庄火塘、厨房和客堂，一家人围着火塘吃饭说话，是日常生活的中心；三层住人；顶层是经堂，全楼装饰最华美、画满壁画，长者交出管家权后在这里吃斋念经，办婚丧嫁娶时做法事的喇嘛也暂住这层。屋顶四角各凸起一个白石塔，代表山、树、水、地四方神灵，上插经幡；楼沿中间有煨桑炉，有大事时点柏枝祭神。<strong>从牲畜到人再到神，楼层越往上，越靠近精神世界。</strong>层与层之间用独木梯上下。'),
  ('p', '古碉的来历比寨子长。雏形约3500年前就出现，和丹巴中路罕额依的新石器遗址一脉相承。汉代，这一带的冉駹夷为抵御北方游牧羌人的进攻，在石室基础上建起碉楼，《后汉书》记载他们「累石为室，高者至十余丈，为邛笼」，邛笼就是碉楼。明清碉楼最多时约3000座。乾隆两次用兵大小金川，前后打了十几年，金川「地险碉坚」，清军动火炮才拿下。防御做得很细：碉门开在二层楼高的位置，战时收独木梯、关碉门；射击孔做成喇叭形，墙外收窄、墙内放宽，挡得住箭，又不挡视线；墙底厚1.5到2米，顶部收薄到0.5到0.6米。还有一条老规矩：谁家生了男孩就修高碉，每长一岁加修一层，<strong>长到18岁碉楼正好18层，成人礼上把炼成的钢刀交给他</strong>。'),
  ('p', '道孚崩科，是另一类藏式民居，骨架全用木头。「崩」是木头架起来，「科」是房子。圆木对劈、卯榫咬合，<strong>整栋房不用一颗铁钉</strong>。1973年炉霍大地震，片石墙房成片倒塌，木构的崩科扛住了，这一带重建时普遍改用这套做法，道孚、炉霍现存的民居就以崩科为主。崩科大小以「空」计数，四根柱子之间算一空，约二十平方米。室内精雕细镂、描金绘彩，外号「民间故宫」。'),
  ('p', '民居在藏寨之外还有几路。乡城白藏房，2020年评上「中国白藏房文化之乡」，现存6000多栋，土木结构，土墙夯筑，能用上百年，墙体收成梯形，大小看柱子多少。传统上四到六层，底层养牲畜，二层住人，上面晒粮。每年有个「白色灌礼」的民俗，用山上一种白土拌水从墙头浇下来，把墙浇白，既加固又祈福。木雅藏房在康定木雅地区，片石砌筑。羌族的桃坪羌寨在阿坝理县，房子叫「庄房」，全石砌成，<strong>工匠不绘图、不计算，凭经验垒</strong>，石墙一层层向内收分，屋顶平台家家相连，外号「东方神秘古堡」。寨里的羌碉9层、高约30米，经受了1933年叠溪、2008年汶川几次大地震。'),
  ('p', '寺院建筑，有一套固定骨架：大经堂（指钦）是核心，佛学院（礼仓）、佛殿（拉康）、印经院在侧，整体依山而建，不追求中轴线对称。大经堂空间高阔、柱网密集，阿坝格尔登寺的大经堂有120根柱子。<strong>金顶是等级的标志</strong>，重檐歇山、铜瓦鎏金，顶上立镏金宝瓶、法轮金鹿，是藏汉结合的做法，色达东嘎寺主殿金顶用真金箔，几公里外都看得见。辩经场挨着佛学院，僧人在空地上拍掌问答；转经廊绕着佛堂或佛塔排满转经轮，格尔登寺49米高的佛塔外围有几百个小转经轮。各教派都能看：理塘长青春科尔寺1580年建，占地33万平方米，是康区规模最大的格鲁寺；马尔康大藏寺是嘉绒碉房式；木雅地区还有汉藏结合的碉楼经堂。苯教寺院另成一路，金川雍忠拉顶寺是代表。'),
]

APPENDIX = [
  ('h2', '出发清单、藏语词'),
  ('h3', '出发检查清单'),
  ('list', '<li>证件：身份证、驾驶证、行驶证，随身带好</li> <li>药品：乙酰唑胺（遵医嘱）、布洛芬、感冒药、肠胃药、红景天（出发前就开始吃，只作辅助）</li> <li>衣物：抓绒、羽绒、冲锋衣，帽子、墨镜、防晒霜，保温杯</li> <li>装备：指夹式血氧仪、离线地图</li> <li>车：拖车绳、防滑链、充气泵、补胎工具</li>'),
  ('h3', '藏语常用词'),
  ('cwords', '<li><b>扎西德勒</b>吉祥如意，最通用的问候</li> <li><b>突及其</b>谢谢</li> <li><b>卡里沛</b>您慢走（送别时说）</li> <li><b>卡里秀</b>您留步（自己留步时说）</li> <li><b>广达</b>对不起</li> <li><b>嘎地</b>辛苦了</li>'),
  ('h3', '延伸阅读'),
  ('cwords', '<li><b>香巴拉深处</b>纪录片，2018，豆瓣8.7。四川藏区人文，理塘、金川、稻城亚丁都在片里，讲普通人过日子</li> <li><b>第三极</b>纪录片，青藏高原全貌，和《香巴拉深处》同一个总制片人</li> <li><b>尘埃落定</b>阿来，2000年茅盾文学奖。写阿坝马尔康的嘉绒土司，路上看的碉楼寨房就是小说里的世界</li> <li><b>艽野尘梦</b>陈渠珍。清末川藏亲历记，羌塘逃生115人活7人</li>'),
]


CSS = """
  :root{
    --ink:#1e2530;
    --paper:#ece5d4;
    --dim:#a89f8a;
    --vermilion:#c1493f;
    --vermilion-deep:#a83a30;
    --gold:#d9b23c;
    --flag-blue:#2f6fd0;
    --flag-white:#ffffff;
    --flag-red:#d9553f;
    --flag-yellow:#d9b23c;
    --flag-green:#3d9e7f;
    --serif:"Noto Serif SC","Source Han Serif SC","Songti SC","STSong",serif;
    --sans:"PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  html,body{margin:0;padding:0;}
  html{background:#3a4152;}
  body{background:#3a4152;padding:0;font-family:var(--serif);}

  .card{
    width:1080px;height:1440px;
    background:var(--paper);color:var(--ink);
    padding:0;
    display:flex;flex-direction:column;position:relative;
    margin:0 auto;
    box-shadow:0 10px 30px rgba(0,0,0,.35);
  }
  .card + .card{margin-top:64px;}

  .flag{display:flex;height:14px;width:100%;flex-shrink:0;}
  .flag span{flex:1;}

  .card__inner{
    flex:1;display:flex;flex-direction:column;
    padding:48px 64px 52px;
  }

  .card__kicker{
    font-family:var(--sans);color:var(--gold);
    font-size:21px;letter-spacing:.34em;text-align:center;margin-bottom:20px;
  }
  .card h1{
    font-size:56px;font-weight:700;text-align:center;
    letter-spacing:.07em;line-height:1.4;
  }
  .card__intro{
    font-size:26px;line-height:1.9;color:var(--dim);
    text-align:center;margin:26px 0 8px;
  }
  .card__meta{
    font-family:var(--serif);font-size:22px;line-height:1.7;
    text-align:center;color:var(--dim);margin-bottom:6px;
  }

  .card h2{
    font-size:36px;font-weight:700;color:var(--vermilion-deep);
    text-align:center;letter-spacing:.12em;line-height:1.5;
    margin:30px 0 20px;
  }
  .card h3{
    font-family:var(--sans);font-size:26px;font-weight:600;
    letter-spacing:.24em;color:var(--vermilion-deep);
    margin:34px 0 14px;
  }
  .card__lead{
    color:var(--vermilion);font-size:30px;line-height:1.9;
    border-left:4px solid var(--vermilion);padding-left:20px;
    margin-bottom:28px;
  }
  .card p{font-size:29px;line-height:1.92;color:var(--ink);text-align:justify;margin-bottom:1em;}
  .card p:last-child{margin-bottom:0;}

  .card strong{
    background:var(--vermilion);color:#fff;font-weight:700;
    padding:0 .14em;border-radius:4px;
    box-decoration-break:clone;-webkit-box-decoration-break:clone;
  }

  .card__keys{list-style:none;margin:28px 0 34px;}
  .card__keys li{
    display:flex;justify-content:space-between;align-items:baseline;
    font-size:32px;border-bottom:1px dashed rgba(30,37,48,.28);
    padding:16px 2px;
  }
  .card__keys li:last-child{border-bottom:none;}
  .card__keys li strong{
    letter-spacing:.06em;white-space:nowrap;
  }

  .card ul.card__list{list-style:none;margin:6px 0 0;font-size:29px;line-height:1.92;}
  .card__list li{padding:.28em 0;padding-left:1.1em;position:relative;}
  .card__list li:before{content:"·";position:absolute;left:0;color:var(--vermilion);}
  .card ul.card__cwords{list-style:none;margin:6px 0 0;font-size:29px;line-height:1.92;}
  .card__cwords li{padding:.24em 0;}
  .card__cwords b{
    display:inline-block;min-width:4.6em;color:var(--vermilion);font-weight:600;
    font-family:var(--sans);letter-spacing:.04em;
  }

  .card p,.card li{text-wrap:pretty;}
  .card h1,.card h2,.card h3{text-wrap:balance;}
  .card .nowrap{white-space:nowrap;}

  .card__foot{
    margin-top:auto;display:flex;justify-content:space-between;align-items:center;
    font-family:var(--sans);color:var(--dim);
    font-size:20px;letter-spacing:.14em;padding-top:36px;flex-shrink:0;
  }
  .card__foot .foot-flag{display:flex;height:5px;width:96px;}
  .card__foot .foot-flag span{flex:1;}
"""

JS = """
<script>
  (function(){
    var q = new URLSearchParams(location.search).get('card');
    if (q){
      var idx = parseInt(q,10) - 1;
      var cards = document.querySelectorAll('.card');
      cards.forEach(function(c,i){ c.style.display = (i === idx) ? 'flex' : 'none'; });
      var c = cards[idx];
      if (c){ c.style.margin = '0 auto'; }
      window.scrollTo(0,0);
    }
  })();
</script>
"""


CPL = 32   # 正文一行约能放的字数（内容区 952px / 29px）
LHP = 56   # 正文一行高度（29px × 1.92）


def _lines(t):
    return max(1, math.ceil(len(t) / CPL))


def block_height(kind, html):
    """按 CSS 实际尺寸估算块高度（px），用于防止内容超高、页脚被挤出卡片。"""
    t = re.sub(r'<[^>]+>', '', html)
    if kind == 'kicker':
        return 49  # 21px×1.4 + 下 margin 20
    if kind == 'h1':
        return 78  # 56px×1.4，单行
    if kind == 'intro':
        return math.ceil(len(t) / 36) * 49 + 34  # 26px×1.9，内容区能放约 36 字/行
    if kind == 'meta':
        return math.ceil(len(t) / 43) * 37 + 6  # 22px×1.7，约 43 字/行
    if kind == 'h2':
        return 104  # 36px×1.5 + 上下 margin 50
    if kind == 'h3':
        return 85   # 26px×1.4 + 上下 margin 48
    if kind == 'lead':
        return math.ceil(len(t) / 31) * 57 + 28  # 30px×1.9，内容区去掉左边竖线留白
    if kind == 'keys':
        return 524  # 6 项 × 77 + 上下 margin 62
    if kind in ('list', 'cwords'):
        pad = 16 if kind == 'list' else 14
        items = re.findall(r'<li>(.*?)</li>', html, re.S)
        h = 6  # ul 上 margin
        for it in items:
            h += _lines(re.sub(r'<[^>]+>', '', it)) * LHP + pad
        return h
    return _lines(t) * LHP + 29  # 普通段落 + 下 margin 1em


def partition(stream, H):
    pages = []
    cur = []
    cur_h = 0
    n = len(stream)
    i = 0
    while i < n:
        kind, html = stream[i]
        bh = block_height(kind, html)
        if kind == 'h2':
            if cur:
                pages.append(cur)
                cur = []
                cur_h = 0
            cur.append((kind, html))
            cur_h = bh
        elif kind == 'h3':
            # 小标题必须跟它的正文同页：按「h3 + 下一块」估量
            nxt = stream[i + 1] if i + 1 < n else None
            need = bh + (block_height(nxt[0], nxt[1]) if nxt else 0)
            if cur and cur_h + need > H:
                pages.append(cur)
                cur = []
                cur_h = 0
            cur.append((kind, html))
            cur_h += bh
        else:
            if cur and cur_h + bh > H:
                pages.append(cur)
                cur = []
                cur_h = 0
            cur.append((kind, html))
            cur_h += bh
        i += 1
    if cur:
        pages.append(cur)
    return pages


def kind_html(kind, html):
    if kind == 'kicker':
        return '<div class="card__kicker">%s</div>' % html
    if kind == 'h1':
        return '<h1>%s</h1>' % html
    if kind == 'intro':
        return '<p class="card__intro">%s</p>' % html
    if kind == 'meta':
        return '<p class="card__meta">%s</p>' % html
    if kind == 'h2':
        return '<h2>%s</h2>' % html
    if kind == 'h3':
        return '<h3>%s</h3>' % html
    if kind == 'lead':
        return '<p class="card__lead">%s</p>' % html
    if kind == 'keys':
        return html
    if kind == 'list':
        return '<ul class="card__list">%s</ul>' % html
    if kind == 'cwords':
        return '<ul class="card__cwords">%s</ul>' % html
    return '<p>%s</p>' % html


def render_card(i, blocks):
    inner = ['<div class="flag" aria-hidden="true">' + FLAG + '</div>']
    inner.append('<div class="card__inner">')
    for kind, html in blocks:
        inner.append(kind_html(kind, html))
    inner.append('<div class="card__foot">')
    # 首页已有 kicker 品牌字，页脚不再重复；其余页左下角写品牌
    inner.append('<span>' + ('李大妈的自驾路书' if i > 1 else '') + '</span>')
    inner.append('<span class="foot-flag" aria-hidden="true">' + FLAG + '</span>')
    inner.append('<span>' + ('%02d' % i) + '</span>')
    inner.append('</div>')
    inner.append('</div>')
    return '<div class="card" id="card%d">%s</div>' % (i, ''.join(inner))


def main():
    # 总页数 = 页1 + 正文分页 + 附录2页，目标是 18
    # 内容区可用高度约 1262px，页脚占约 64px，正文安全上限取 1200 左右
    counts = {}
    for H in range(980, 1401, 5):
        n = 1 + len(partition(BODY_STREAM, H)) + 2
        counts.setdefault(n, H)
    target = counts.get(18)
    if target is None:
        keys = sorted(counts.keys())
        near = min(keys, key=lambda k: abs(k - 18))
        target = counts[near]
        print('note: no H gives 18; using %d pages (H=%d)' % (near, target))

    body_pages = partition(BODY_STREAM, target)
    # 合并孤页：单块且高度很小（≤300px）的页并入前一页，如第13页并入第12页
    merged = []
    for pg in body_pages:
        h_pg = sum(block_height(k, hh) for k, hh in pg)
        if merged and len(pg) == 1 and h_pg <= 300 and merged[-1][1] + h_pg <= target + 60:
            merged[-1][0].extend(pg)
            merged[-1][1] += h_pg
        else:
            merged.append([pg, h_pg])
    body_pages = [pg for pg, _ in merged]

    pages = [PAGE1] + body_pages + [APPENDIX[:5], APPENDIX[5:]]
    cards = [render_card(i, blocks) for i, blocks in enumerate(pages, 1)]

    for idx, blocks in enumerate(pages, 1):
        h = sum(block_height(k, hh) for k, hh in blocks)
        flag = '  <-- 超限!' if h > target else ''
        print('card-%02d: 估算 %3dpx / H=%d%s' % (idx, h, target, flag))

    html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>川西自驾行前笔记 · 小红书卡片</title>\n<style>\n' + CSS +
            '</style>\n</head>\n<body>\n\n' +
            '\n\n'.join(cards) +
            '\n\n' + JS + '\n</body>\n</html>\n')
    with open('cards.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('H=%d total pages=%d' % (target, len(pages)))


if __name__ == '__main__':
    main()
