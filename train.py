from __future__ import print_function
from __future__ import division

import argparse
import random
import torch
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
from torch.autograd import Variable
import numpy as np
from torch.nn import CTCLoss
import os
import utils
import dataset

import models.crnn as crnn

import matplotlib.pyplot as plt
import numpy as np
import torchvision

# functions to show an image


def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--trainroot', required=True, help='path to dataset')
parser.add_argument('--valroot', required=True, help='path to dataset')
parser.add_argument('--workers', type=int, help='number of data loading workers', default=2)
parser.add_argument('--batchSize', type=int, default=64, help='input batch size')
parser.add_argument('--imgH', type=int, default=32, help='the height of the input image to network')
parser.add_argument('--imgW', type=int, default=100, help='the width of the input image to network')
parser.add_argument('--nh', type=int, default=256, help='size of the lstm hidden state')
parser.add_argument('--nepoch', type=int, default=25, help='number of epochs to train for')
# TODO(meijieru): epoch -> iter
parser.add_argument('--cuda', action='store_true', help='enables cuda')
parser.add_argument('--ngpu', type=int, default=1, help='number of GPUs to use')
parser.add_argument('--pretrained', default='', help="path to pretrained model (to continue training)")
parser.add_argument('--alphabet', type=str, default="楊宋ゑ褄挽連庭ヶ伴畳此香鐵齬逞奇賊包峻ゴ隼慘瓮蜂于傳板誘祭し蠅卦迂椒硯燻ｋ耕筒伯唇椅嘔聨乙州袖峰弉ゝ灼慧数鮮匡崗丹衍塩盗е顆還問譬感θ力瑞蓬澗填國鯛膚普Αδ酵醇Ｃ惑磴敗杯憲魅叉柚示瑠粥ｇ氷瑚學維運備楳旨輯窟壽玲貶撚雇臑蓑以項痺犀ペ菖в状敢掴福煌訣隙捉表吟踪淫結蓄富守脱視針擬惰奪涅入撞徹蠱漕笑ﾙ絃笥能蔦び作浮痴弾銭弐痒デ邉快味梵圏殺癌鞍階稲鬱歿路獅型テ瞳網聰曖鰺餡複収下笠岳柔策漿唸鯖ﾍゃ涛塞借総奢崇捻癖ｴ磐膠頬剣持粛眤仲橋Ｅ酸米往見談倭偽大冴頷斉暴楼托苺至昇慄潺律隈屋с怨宿慈醍寿李麹肩購瞥桔蛤竄独顕汝渓晶聖柏嘗刑そ択嵜ｹ譲醒矛眄樂陪鎮支裟眠聲鯑叱劫磨ρ虫戴博櫓な触塑穏臭苔錠程が套枢鯆描夜充沈疾荏詠觀麺蔽榊К擢震埠ヵ滑量祠羹稿А崩立正局雋水觚升茎罠栖決歩暇貨駝莞欽ず疇躊層ぷ冒詈忽メ菌田時搬熟故冬囃植相す腸頃扮堪少誓啄咬間錣衢廣痰り肺澄治簿池炒楔溢盍α障呉復昂隋穂派興窃可肉莪絢邱陛壺椶殖彫音尹史品蘋鬼瞑ｶ乏疹醐壮溝將魴徳暮剰糊胃Ｗ膵窄髏休來エ獣茅琥矜湾芸孔市勉耽拉籠飼忘燃媛皇酋琴屍緑爪沫ぎ讀當ｱ暁蒙Г傑邪斜鳥腐蛆道阜種閃媒野桧へッ壇巴ヤ攘諮挫喉ｲｕ軽液態柿深胎璧前百秀剱残茨樹瓜諭爐更麁饌岩蘆洋犯埃泉褒庚毯注炸檻偵讃撒え郢経募賠漬銃愀ち因退属侯轡丈睨諸函槻咥婆ヨ励祀胤萓縫環趙渦婿妨酎隊必の遡謐凧鷲訓唯ｓй司ァ息灯室陸切烙諾薪成倍鉾材ﾎ顎燕提従機倣戸蚊請礼猾ｧ閣適足干咀怜制祥撥喝座硝嚥透湿げ乎県藻泄寧枝鷹筐猶蛾巨拍証実婦所雑贅戮セ灰子櫂反長彡や拶醤一栓嬰斐父匠栞蟲章翡浄覇祷譚繍嫐通か絶ａ盛廚儲嘲祟綿創隠萋淵花蹈渚に叙蛛嶼碕汐易姦兼ど重劼貫線満畿帯泥Н劾娶亮愁淑嬢文冑膸怪侠平質賂題鏡鋼急薦菓慰鈎漫冶優焦點政窓卯棟筍竹ョ修按詳濯述殲蹐榎貪敏究粟を坂共賭否霊津店洩賢雫想逢奮酊蔑哨酢釣煽遂帰傷枯庸互飛ｂ候恣食験断わ髭取裕騙っ綺沿阪伸厚醗綾磋潤罫宍駿擦諏鮹利槽理懇抗衒歌換ーザ有殻是記斂貼菜喜棲厨団徨邁輸ば括蹄琉惚桑列Ｚ堂ニ酪狽覚袂損辺抜茲晁雁晰戻Ω覗娩簑己狩逝昔援巧蜘燐誤愛慌瓩尖組磁末葦泌未尻訃ダ荷統ｵ堵待雖宜鮭咸繭漁俺纂媚色算礇鱈棄癩卓吹慇公櫛繩喫副羨和萃祇Ε殆賛弊奧解械д轟廼鞄禮ｬ悲省豆峙榜貝財ｨ奄七目ﾈ紅滞手不剤渾只貽挺廻朔擇痛楯思迎ぅ兜僖士紛馴職檢君ぇ避眇盥亦奴疲玩註廉麟酔双整獲賈ι孵捧琵瘤猪酌贋囚甫ギ疑扁緒布北莉斟澹欺墨厘魏弔拮壌露ィξ罹呈海巳錫林佇鷙尋苫ポ狼い彿姑彷Ｌ桜蒐菫暢外蘊穗盤苛撃縮甘ヒュ郭粗串念つ乾悍胚浪占眺尚薄試逅塗当嫡夷配蜜献称髪耳余滅亡襪Υ番腱光曚匐槌淋倶傀膨録閾率浩鱗習單キ辰曲ﾃ散例締誠趨吸図朗信履出譽彩縞謳造舵生誹囮畏丼匿脇給災浙鯊置引鉱侍豬羞諺拳檎縁科湧咽竣蕃寇妾馨經鮨送藝訪荒条欷督秋遅襖べﾑ篤腿ぐ誌遮襯憧拝ア蓮愼身т扈屈ﾛ采原韓ф翔仕ж嫻パ句姓唄詩ﾘ泙ワ段乞蒼鬆呂魎モ晴嗚籐誇л兩喰懐銘幾沼堰薬戌ハ努礁吏甦ь契斥屏安券奏禽起彼三證欧謀融鴉漆鼓盃場疋悦悸舐蘭膤髑嘩摂像悶弛蟻澱蠍絨儂蠑專ゅ許牲口麒ｌ宴醸惇刺喚癲堯湛牛穴閑培腔ゐ頑臓涎ﾆ左粒鯲商箴塀助績允爲て璽葵輻た比輙魚豕秘驚再号袴篁径靴ホ曼淀伏ぜ涼呆已侶閏軌禎纏過加顔敲韋蘇革卿腹袁εа桶鞭抄桂惨着沢筑映臨澁汚豈浅ｳ跡咾氏輩巫病浦龍麌漢牟尿既嶌標近俳飴脂勤臣膝梅突太卜肋凹滓顰柑爽撫照賤ガ恰零皓頂ο斧千鹽棍陵雲縄什刀鶏厄颯鑑伐蕁ビ育杞艇桃季餞的弦ц顧鎖暈滲僭京空覯υ欅俯彰ゲ蹴緻途賀供由ｸ芯舩敵振崎穀ﾇ愕郡棋姐發侮蔵騨慮薗毀ヲ貘装鮎幀牒峡ﾅウ致減蒸餃刹頼恩南宝宣徘旦荻会扶延旅掛編凪説絆懲挨蒲曝秒呑典舘凍俎握詰ヾ紫鯀噺賜執導懺棘珪尤惡盪納獏涜權晋肝冤倒響那撮藥佳別在巖返窮似坤情婚ふ均抵本瀝恒就ほ戰賎渡袋核沌腕争楢肢去言登教軋逮拓棚操鳩蕾藩永碗担浴ェ廊鄒烹鮴撤醫賃鐐随扉隘諫梱潜矯厭緩T屑虹湘地佑胱上藏鷏夫越昨痘於逐鯣妓如リ古異ｈ鬚鍮寵孤磔免濡畝阻詫回尾摺撲勿續紘研燥彦殴茜勧箋愚区聾爆略瞰梶撻東ﾗ翼慶埜罪觜捕諜院紐鮑飲卵倉瞬羚汁潘約頓瞼養癒無使茫騒瓢煉彬具爾Δ澤止ナ志渕簾魄腓珊斯怠尺貴銅元侑扇淳頌課囘奉ン从洲惧剖差茶則絹沁遵拒冗も粧枕擁饗遷寅鳶荼裳ヴ滸砂ま買物憎模民ょ勝鎧炊狙絲薮掟痕羅泳智帝事紙ﾀ樣拘嫌麓僉敷求頒亭疵廳稜γ炉韻招沐矮餅岸世眛波青ά要浜裸毒披務八療刷ﾂ藹毎闇歪濁掲洙コｊ菩噌佐甚鮃刃Σ艘抽繋壕忍咲鯒譟斤鼎法般設房芽舶吠漑徐々箇ぴД承塊颪叡躯靖ｘ暗群召駈凛オ拡樽盆肌牧ｚ愡だ鷯頚憊膣椿梯売也悔谷鈴憩鵬背討袈超橙煥点膳礫繊豐挿遙憶唾困訝妬舛濾児最Ｆ尼曜若劇雷拙腰憤走机詐网鶴六劣楠停螢鮗棹汎乳斬艶塚臆妖磯汲縦軟毅人祐爬盻拌鍬乃鉛薇祉祈喩盧凱訊客昆С鴇其牽紳等遠累動吐摘ｩ攣俵廟ぢ油Ру焚玉β孟塾禍頻ｻ莱拷づ亥効弧噪邦迷封ヘ偶膜餾族Ｊ投蠧違賞襲好検ﾕ楾唐馘午脚酬屬餤員秦歓萢歴峯官初莽旋絡盾謎類祝井爺舎翕松齢ｆ協湖箕権乍隻某ｫ失ム偉賦叢云蚤脊タν舌潟巾惣苗幅耗股紺τ酩償憂揉柱凋草釧弱佞聞榛г與威砥ゥ徴ド嘱五考睫嵩老内敦然斡滋蝿旗冨邂但禰叫字糧薔捺壱首庇曰壬禅挙閉篠岐貞彗餐瓶任饒Ｖひ儡聴覿巷裏郷書狭秩交窺旺彙辿疫枚ぞ軒挟疼薙良辱瞭景定灸増樺屁脳害羽寶圃躰轄撼狂η終天埼虔今偲繹堀礎菅敕仰険師啓殉幇華遥眈覧ы溶床防Ｎ凶駄唖鴻Ｂ霆抑眞粉飄攅釈ｯ麩怖潰私歎垣旬茸Λ右畠拭厳蟷資殷紗役租極〆雪輪製贄溺Ｍ扱雨届φ遊泡圧積捏膺丁序農悉到哀蹙携奔駕肇単喬埓價寛甥距貧醜皮西Ｕ該謗Ｈ渥僅脩陥甕謄園嗟躇凄霖М票識逸杵工影規領府遒惜貳遜佃狗フ昼瀬銀鷺圓慨湯麗揃版垰或揶寡ォ源器覦瑛血寂燭紹汰廛涵凝丕ｮ服齊雛兇裁茵債命萬廖男指偕梓呟雹剪措准撹侵蕪我底悼嵯浸遽落訟峨便巣朦街蕉ゆ墳む藜話続沃貿蹂依炭鉤仙厩衆膏錦う僧式柊濠叔堅ﾖ杭臼驕壷è億詭誕腑揆巻裾恫邊脹期馳蛮鄭祓皐尽伽墜拾凡喘織告櫃ん琶捌昭弁楮飩謡母輌摩奈條費效久蟹看レ曾芳曹頁瓠關咎与鵐主珍施ミ惹逗躍駒炎グ葺焼穫騰嗜麦蕕評軸衝ﾌ眩Ｓ萄獄坑恨é筏箔亙傘際村栃将込都Ｑ勘付短琲乗笹勾訐芋砧幡帥蓋直糞ら鍋ぃ洪恐ｎ處報堆税霞鍵泣者蛎迫嚇弓る魂企遇詞週著貢賽熾朧且寓変ｄ併蝶菱ゞ悪神各剃唆洞牌穿折狐詣嬌對貔ﾞ娯側狛樫蜃位犬庶じ代節滝鍛б迅愴伊諦鮒賓雅除黄労度腎虚輝写柴蹇廷寺践把先迦健家郵冊鼠即蝕κ晦肛躙チ豪я靄翻祖妙潔伝繕橘剥蝦削隕拐蔓鴎貯技闊ｺ密糾諒衡国謙кｪ嘘寨化翁О褻捜璃亢錯添梗腫弘崖御聯糸泊肯迭居几城觧改蜥欄皸蛙蔀拗暖怯腟Ｔ椰ｰｭ噂庄征索逆幣慙嵐儀獰煮寮芭親虞杜涯四読曇完楓勲孕丙勢警美ч陶Ｇ墾童探咤λ皺令拠桐俟Ｒ訳齟俸轢審陰イ蠕恍娼斎年謹護圭欠捨歳真蠣鞘叛渇亜饂ぶ鋪割絞竜特住楽舟ネ範答倖爵騎倹皆寸ツ十脛耐坊萌枠港麻介靱箏後渋碍幸党紊汗糠裔葬稀淺星ﾐ紬秤箪匂ｙ痢意ボ兄Ｘ堝歯瘍れ堕覺ｍ辣僻湊淹専禄監伍練死辻謂趣虎バ朕く慣會杖鳴没染蚕謝裂靡徊ス戒弄贔閻ノ虐鯡為ｷ渉孫霾衷島鄧瓦砦ベ燦晩悟被紆冷薀欝根聘郎郊学又痔片春從虜儒芥載簡煎吉后睾葉窯鋏向榴吊掌円巽睛猜穣系建萩業咄酉ジ葡耀Ã栽強而儖稔み膀忙輔錨罷嘉贖翅救錆彌嘆壁訛俄鎌捷蔡珈垂亞皿Ｏ嚢埒ｏ坦舒惠敬析き釜認ぁ細π錬霜Ψ壊姪猛釘濤ご嬉界価聽牢逓硫筈燈窒雌築声娠實容斗早剛用朽毛戦и弟で筆活玄畜紡鹸移鮪日同画才観桁け碩羮惟魑覆嶋帳豺旧幕幹縣阿餓惺濫體競議瑤殿雀押級低鰹拂ブ坐と僚脈螺関ﾊ克賄察抹予聳芻鵑狸瀋蒔汽鮠需鵜は鑽速奨Ｄ憾堤格抱梟錚半魁郁逡傭碑肖弌鵝躾札ぉ昧Ｐ茉錐ヌ耶船藤俣濃放ヂ逃帆臥濱案ケ攻英席嗅熱憬多蒋罎斑航門弥含訶甲夏號碁憚墓讐蛋妻觴角冥梁姉較曽卸清魔瑕鉄対ぼ町甜鋸崔高胴乖悠絵宮匹錘П藁雰陽繰陲Â弖ｼ戚稚鋭芦ピ灘羯禹栄頸Φ嫉ト難嫁況岬蜴ク顛兎館葛瞞蕎駐諡饉踏襟河魍シ笛義及蹟働頭這中ﾄ艦ヽ次滴竿熙境遺稽梢柵粋誰喪域鍼槃消蜷俊寒ｐ淡丘件樵悩魯孝願倦朴武あ知ﾋ風椀笋丞兆褐嶺白賁庫苑猟鰻僑瀧僂鈍猫判蜀攫蝋胸揄牡禊淒个泰緋産小央帽全娘淘性預芹譜嗤梨愿宰沖Π窪藐須ゾ訥欒咆ﾝ訂調做仏紂攪暫果隅廃哲駆ｔ忠降砕宥激ｿ衣桟伎閲木疎混燗繁儘麿ぬ横憑跳黙万亘哉功吾胆留鯨砺σ餌周兵他保勃踵益藍丱譴Ａ罵屮楡庵歉徒衞廠幼р塵揺存飽躁峪侫檸緯基鴨ﾉ墟貰慎糖架合槍明開茄姻珠里叩プ搭豸輿夕囁愉善枷款象恭妃寝肴静傍播馮採妥洒枡方蛍望屯哮演符骸販煙王誉ｗ分端寄宵排校精ﾔ呵衛係緊褥硬飢荘概銚邸姜術部奥暦董遍禁鮖め尊語舗隆盂宗仮叶藪飾犠坪隷爛萎両託危唱負九堺賣批ユ卒社面臺鱒盟盡氾促射瀕憐慕稼悗心Вä辛桓嗣雄誼揚恋栗肥ｾ来鼻芝接檜打流妄瘡展焙菊灌台お掘測煤髻畦達渊却蠢鏗譯賑勇限冠ｖ昴蝓仇團羊ｉ幽漱吃遼ズ嚼準И値跋了н妹些址Ｙ森ソ蛸Ｉ漏蔭卍閥應卑閔形こﾓ株馬貌ｒ申坡始襦受帖慢劉ぱз順印沺赦ロ月鞠酒狡額怒痩さ籍鰐豚翌倫鑼塁症偏希鰯杏屓喋鯤碧亨応管蛇髄禧蝉火宕逼様訴ﾜ縛楕済駁丸幻謬委榲ﾁ傾宛澆葱埋遣肪砲巡茹ｃぺ鮟ﾏ匆伺第丿料姿昏涙亀沸掻追鉉妊擾苦沙à猥純彊赤温選遭微疆豊儚盈鯵骨逍薩佛診焉呪櫻ざ聡洗ω迄柄柳責脅椣友拿ﾟ宇隣継マ庁患ζ鸞軍熊黎塹据補川何束晒缶鮓錮講稻Т呼僕烈陳垢脆新澪揮破気査自漂菠舞畔紋箒睡ラね翠ぽ牝飯牙赳樋疽素得懸眼Ｋ杉棒ゼ篇裡鉢鯉檀江漠貸宅勅処朋蠡体名塔粘辞進噴μ戯ﾒ陣附氣転册乘現邑非ｅﾚ莫霧兒丑土收煩ル珀綻構女刊恵烏忌Л刻循授駑鋳猿嵌計豹勁綜潮嘴常払替陀痙サ泪挑金控盲巌箸薫穢篭咳樟衰臍齋参凌綴洛淇筋仔カ屠腺踊昌康峠憺殊眦闘羶п箱綵幌詮畑鐘憫広宏矢ã隔槇楚鷭饅班石摯蓼噛ャ搾мヅ匙胡夢医凸塙旭ろ張撰衿黒睦肘鹿署漸棺椎蠹宙刈享酷喧朱集眉辟朝個欲蕩杰紀推о傲ゎ胞膿ｽ確琢囲綱鮫晃茂岡駅離爭哺発曙固並暑恥罰贈捗論赴俗褪電檬催山鳳営轍乱禿仁姫靭二尉之車溜掃球せ榮よ行 ")
parser.add_argument('--expr_dir', default='expr', help='Where to store samples and models')
parser.add_argument('--displayInterval', type=int, default=500, help='Interval to be displayed')
parser.add_argument('--n_test_disp', type=int, default=10, help='Number of samples to display when test')
parser.add_argument('--valInterval', type=int, default=500, help='Interval to be displayed')
parser.add_argument('--saveInterval', type=int, default=500, help='Interval to be displayed')
parser.add_argument('--lr', type=float, default=0.0001, help='learning rate for Critic, not used by adadealta')
parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. default=0.5')
parser.add_argument('--adam', action='store_true', help='Whether to use adam (default is rmsprop)')
parser.add_argument('--adadelta', action='store_true', help='Whether to use adadelta (default is rmsprop)')
parser.add_argument('--keep_ratio', action='store_true', help='whether to keep ratio for image resize')
parser.add_argument('--manualSeed', type=int, default=1234, help='reproduce experiemnt')
parser.add_argument('--random_sample', action='store_true', help='whether to sample the dataset with random sampler')
opt = parser.parse_args()
print(opt)

cudaDevice = torch.device("cuda:0")

if not os.path.exists(opt.expr_dir):
    os.makedirs(opt.expr_dir)

random.seed(opt.manualSeed)
np.random.seed(opt.manualSeed)
torch.manual_seed(opt.manualSeed)

cudnn.benchmark = True

if torch.cuda.is_available() and not opt.cuda:
    print("WARNING: You have a CUDA device, so you should probably run with --cuda")

train_dataset = dataset.lmdbDataset(root=opt.trainroot)
assert train_dataset
# if not opt.random_sample:
#     sampler = dataset.randomSequentialSampler(train_dataset, opt.batchSize)
# else:
#     sampler = None
train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=opt.batchSize,
    shuffle=True,
    # sampler=sampler,
    num_workers=int(opt.workers),
    collate_fn=dataset.alignCollate(imgH=opt.imgH, imgW=opt.imgW, keep_ratio=opt.keep_ratio))
test_dataset = dataset.lmdbDataset(
    root=opt.valroot, transform=dataset.resizeNormalize((100, 32)))

nclass = len(opt.alphabet) + 1
nc = 1

converter = utils.strLabelConverter(opt.alphabet)
criterion = CTCLoss()


# custom weights initialization called on crnn
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


crnn = crnn.CRNN(opt.imgH, nc, nclass, opt.nh)
# crnn.apply(weights_init)
# if opt.pretrained != '':
#     print('loading pretrained model from %s' % opt.pretrained)
#     crnn.load_state_dict(torch.load(opt.pretrained))
print(crnn)

image = torch.FloatTensor(opt.batchSize, 3, opt.imgH, opt.imgH)
text = torch.IntTensor(opt.batchSize * 5)
length = torch.IntTensor(opt.batchSize)

if opt.cuda:
    crnn.cuda()
    crnn = torch.nn.DataParallel(crnn, device_ids=range(opt.ngpu))
    image = image.cuda()
    criterion = criterion.cuda()

image = Variable(image)
text = Variable(text)
length = Variable(length)

# loss averager
loss_avg = utils.averager()

# setup optimizer
if opt.adam:
    optimizer = optim.Adam(crnn.parameters(), lr=opt.lr)
elif opt.adadelta:
    optimizer = optim.Adadelta(crnn.parameters())
else:
    optimizer = optim.RMSprop(crnn.parameters(), lr=opt.lr)


def val(net, dataset, criterion, max_iter=100):
    print('Start val')

    for p in crnn.parameters():
        p.requires_grad = False

    net.eval()
    data_loader = torch.utils.data.DataLoader(
        dataset, shuffle=True, batch_size=opt.batchSize, num_workers=int(opt.workers))
    val_iter = iter(data_loader)

    i = 0
    n_correct = 0
    loss_avg = utils.averager()

    max_iter = min(max_iter, len(data_loader))
    for i in range(max_iter):
        data = val_iter.next()
        i += 1
        cpu_images, cpu_texts = data
        batch_size = cpu_images.size(0)
        utils.loadData(image, cpu_images)
        t, l = converter.encode(cpu_texts)
        utils.loadData(text, t)
        utils.loadData(length, l)

        preds = crnn(image)
        preds_size = Variable(torch.IntTensor([preds.size(0)] * batch_size))
        cost = criterion(preds, text, preds_size, length) / batch_size
        loss_avg.add(cost)

        _, preds = preds.max(2)
        # preds = preds.squeeze(2)
        preds = preds.transpose(1, 0).contiguous().view(-1)
        sim_preds = converter.decode(preds.data, preds_size.data, raw=False)
        for pred, target in zip(sim_preds, cpu_texts):
            if pred == target.lower():
                n_correct += 1

    raw_preds = converter.decode(preds.data, preds_size.data, raw=True)[:opt.n_test_disp]
    for raw_pred, pred, gt in zip(raw_preds, sim_preds, cpu_texts):
        print('%-20s => %-20s, gt: %-20s' % (raw_pred, pred, gt))

    accuracy = n_correct / float(max_iter * opt.batchSize)
    print('Test loss: %f, accuray: %f' % (loss_avg.val(), accuracy))


def trainBatch(net, criterion, optimizer):
    data = train_iter.next()
    cpu_images, cpu_texts = data
    # imshow(torchvision.utils.make_grid(cpu_images))
    # print(cpu_texts)
    batch_size = cpu_images.size(0)
    utils.loadData(image, cpu_images)
    t, l = converter.encode(cpu_texts)
    utils.loadData(text, t)
    utils.loadData(length, l)

    preds = crnn(image)
    preds_size = Variable(torch.IntTensor([preds.size(0)] * batch_size))
    cost = criterion(preds, text, preds_size, length) / batch_size
    crnn.zero_grad()
    cost.backward()
    optimizer.step()
    return cost


for epoch in range(opt.nepoch):
    train_iter = iter(train_loader)
    i = 0
    while i < len(train_loader):
        for p in crnn.parameters():
            p.requires_grad = True
        crnn.train()

        cost = trainBatch(crnn, criterion, optimizer)
        loss_avg.add(cost)
        i += 1

        print('[%d/%d][%d/%d] Loss: %f' %
              (epoch, opt.nepoch, i, len(train_loader), loss_avg.val()))
        loss_avg.reset()

        # if i % opt.displayInterval == 0:
        #     print('[%d/%d][%d/%d] Loss: %f' %
        #           (epoch, opt.nepoch, i, len(train_loader), loss_avg.val()))
        #     loss_avg.reset()

        if i % opt.valInterval == 0:
            val(crnn, test_dataset, criterion)

        if (i == len(train_loader) - 1) and (epoch == opt.nepoch - 1):
            torch.save(
                crnn.state_dict(), '{0}/netCRNN_{1}_{2}.pth'.format(opt.expr_dir, epoch, i))
