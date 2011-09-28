#!/usr/bin/perl

use CGI;
$q = new CGI;

if ($q->param('source'))
{
    print $q->header("text/plain; charset=EUC-JP");
    print "\n";
    open(SRC, $0);
    print <SRC>;
    exit 0;
}

################################################################
# ヘッダ
################################################################
$title = 'OSPF 経路計算サーバ';
$version = '2009/12/14 α版';
$mail = 'kashima@jp.fujitsu.com';


$mailto = $q->a({-href => "mailto:$mail"}, $q->i($mail));

sub description
{
    # print $q->style('p { width: 50%;  text-indent: 1em; }');
    print $q->h3('概要');
    print $q->p
	('OSPF でトラブルになりがちなこととして、'
	 . '「何故この経路はそんな方向を向いてしまうんだ」'
	 . 'という疑問に答えられないという点があります。'
	 . 'OSPF の経路計算、とくにエリア内の経路計算は、'
	 . 'RIP や BGP と違ってベクトル型ではないため'
	 . 'データの流れてくる方向と経路とは必ずしも一致しません。'
	 . '確認しようにも、ロジックは RFC の中にあってあまり図解もないので、'
	 . '簡単に確認することができません。');
    print $q->p
	('そこで、宛先となる経路までのパスを図示できれば…、という動機で'
	 . 'このプログラムを書き始めました。');
    print $q->p
	('残念ながら Ajax などのダイナミックな画面についてよく知らないので、'
	 . '昔ながらの HTML によるリンク埋め込みテキストで作成していますが、'
	 . 'リンクをたどることで LSA を進んだり戻ったりすることを'
	 . '可能にしています。');

    print $q->h3('対象となるルータ装置');
    print $q->p('以下の装置からの show ip ospf database detail について'
		. '解析の実績があります。');
    print $q->ul($q->li('GeoStream R900 シリーズ'),
		 $q->li('Si-R 3400 (推測)'),
		 $q->li('IPCOM S1000 系'),
		 $q->li('IPCOM S2000 系'),
		 $q->li('IPCOM EX 系'));
    print $q->p('また、表示系の似ているルータ装置によるデータでも'
		. 'サンプルがあればある程度の解析が可能です。'
		. '追加対応のご要望は、show ip ospf database の詳細'
		. '(LSA の内部の情報まで含むもの) を'
		. $mailto
		. 'までお送りください。隙間業務ですので反映は遅いですが'
		. 'きっと対応するのではなかろうかと思います。');

    print $q->h3('使い方');
    print $q->p('以下の要領で装置の OSPF Router-ID を確認してください。');
    print $q->ol($q->li('show ip ospf'));
    print $q->blockquote($q->pre("Statistics and variables:\n"
				 . "  Router ID: 1.1.1.0\n"
				 . "  SPF calculated 39 times"));
    print $q->p('こういった感じの表示が出てくれば、'
		. 'Router ID の部分が当該装置の OSPF Router-ID です。');
    print $q->p('また、以下の要領で装置の OSPF データベースを'
		. 'ファイルに取得してください。');
    print $q->ol($q->li('UNIX や Linux なら script コマンド、'
			. 'TeraTerm ならログ、そういった機能で'
			. 'ルータ装置からの出力をテキスト保存できるように'
			. 'してください'),
		 $q->li('script コマンドを使用している場合は、'
			. 'その中のシェルからターゲットルータに'
			. 'ログインしてください'),
		 $q->li('"show ip ospf database detail" を実行してください'),
		 $q->li('出力された内容が 1 行づつではなく'
			. 'LSA の種類毎にちがう様々な情報が入って'
			. 'いることを確認してください。'));
    print $q->p('ここで取得したファイルを本ページの「参照」ボタンで'
		. 'アップロードできるようにしてください。'
		. 'またそれと同時に、最初に取得した OSPF Router-ID を'
		. '次のコマに記入し、最後に「計算」ボタンを押してください。');
    print $q->blockquote('(なお、コメントにあるとおり、show ip ospf の出力を'
			 . 'アップロードするファイルに含めることも可能です。'
			 . 'その場合は Router-ID を手で入力する必要は'
			 . 'ありません。');
    print $q->p('そうすると次の画面には、経路計算の結果と、'
		. '当該ルータに近い方から順に LSA が表示されている'
		. 'と思います。');
    print $q->p('経路表から気になる経路を探したら、'
		. '「ひとつ戻る」クリックで、その宛先からルータまでの'
		. 'パスを辿ることができます。'
		. 'また、有効になれなかった経路と状態を比較したり、'
		. 'その経路やパス上の経路の元になる LSA を調べることも'
		. 'できます。');
    print $q->p('また、LSDB から気になる LSA をクリックして、'
		. 'その LSA が意味する経路や、そこまでのコストなどを'
		. '知ることもできます。'
		. 'Router-LSA のリンク情報をクリックすれば、そこからどの'
		. 'ルータやサブネットに繋がっているのか分かります。'
		. 'Network-LSA のリンク情報をクリックすれば、周囲にどの'
		. 'ルータがいるのか分かります。');

    print $q->h3('最後に');

    print $q->p('この Web ページは、プロ開統における正式な開発物では'
		. 'ありません。このページを利用するにあたって、'
		. 'ユーザ登録や契約等は不要ですが、'
		. 'このページの出力内容について保証はできません'
		. '(こう書くのは悲しいですが、正式な開発物ではないので'
		. '仕方ありません)。');
    print $q->p('この Web ページについてのご意見やご要望については'
		. $mailto
		. 'までご連絡ください');
}

@history=('2009/12/10: 経路計算まで完了',
	  '2009/12/14: 計算結果の日本語解説をちょっと増強',
	  '2009/12/14: <a href で末尾をきちんと示せるよう文末に <br> 増強',
	  '2009/12/14: 「ひとつ進む」と「ひとつ戻る」で経路と LSA がごっちゃにならないようにする (AS 境界ルータ経路に依存する AS 外部経路は対象外)',
	  '2009/12/16: External path preference を数値ではなく言葉にした',
	  '2009/12/16: Forwarder 計算ミス訂正',
	  );
@todo=('RouterID 入力フィールドに変な値が入らないよう javascript で入力制御する',
# 12/16       'External/NSSA の Forwarder アリのパターンの確認'
       '限定公開のため、このページの主旨などを記載する',
       '宛先を入力してもらって、javascript で適切な宛先に飛ばしてやれば、そこから「いっこ戻る」で traceroute の逆辿りが可能なんじゃね？',
       '利用アンケートが欲しい',
       'ご意見ご要望のページを作りたい',
       );
@thanksto=('李家さん: 限定公開にあたって、様々なアドバイスを頂きました');

sub show_and_exit
{
    my ($desc, @list) = @_;
    print $q->start_ul;
    for $txt (@list)
    {
	print $q->li($q->escapeHTML($txt));
    }
    print $q->end_ul;
    print $q->end_html;
    exit 0;
}

print $q->header('text/html; charset=EUC-JP');
print $q->start_html(-title => $title)."\n";
print $q->start_div({-id => 'head'})."\n";
print $q->comment('header')."\n";
print $q->h1($title)."\n";
print $q->i($version)."\n";
print $q->br, $mailto, $q->br, "\n";
print $q->a({-href => $q->url(-relative => 1)}, '初期化')."\n";

################################################################
# 構造体メンバ名
################################################################
$Name = 'Name';           # String # <a name と <a href 用の名称
$Text = 'テキスト';       # String # 入力ファイル文面
$Invalid = '不可理由';    # String # 不可である理由
$Mask = 'ネットマスク';   # String # ネットマスク
$Area = 'エリア';         # String # エリア ID
$AreaVal = 'エリア値';    # int    # エリア ID を数値化したもの (ソート用)
$LSType = 'LSType';       # String # LSA 種別
$LSId = 'LSId';           # String # Link State ID
$AdvRtr = '発行元LSA';    # String # LSA 広報元ルータの ルータ ID
$Age = '齢';              # int    # LS Age 0〜3599, ∞(3600)
$Opt = 'Option';          # String # オプション
$RtrOpt = 'ルータOpt';    # String # Router-LSA 特有オプション
$Pri = '優先度';          # int    # LSA や経路の優先度
$Metric = '記載コスト';   # int    # LSA や Link に記載されたコスト
$Cost = 'パスコスト';     # int    # パス全体のコスト
$Link = 'リンク';         # ARRAY  # Router/Network-LSA の Link
$Gateway = '次ホップ';    # HASH   # 次ホップ群 (アドレス => $Name)
$Route = '経路';          # Object # LSA が示す経路
$ASBR = 'AS境界ルータ';   # Object # LSA が示す AS 境界ルータ経路
$Back = 'ひとつ戻る';     # ARRAY  # 前段の LSA または RT
$More = 'ひとつ進む';     # ARRAY  # 次段の LSA または RT
$BackLink = '逆リンク';   # bool   # 戻りリンクになってることを示すフラグ
$Stub = '末端経路';       # Object # Router-LSA の Stub Link による経路
$MyAddr='自側アドレス';   # Str    # ルータ自身のアドレス
$MyIfp = '自側ifIndex';   # String # ルータの ifIndex
$Root = 'SPF起点';        # bool   # SPF 計算起点を示すフラグ
$Peer = 'SPF次ホップ';    # bool   # SPF 計算で次ホップを示すフラグ
$LinkBackOk =
    'LinkBackOk';         # bool   # 双方向リンク成立を示すフラグ
$MaybeTransit = 'トランジット'.
    'エリアサマリ';       # bool   # トランジットエリアサマリ
$ExtOpt = 'AS外部Type';   # String # External/NSSA-LSA 特有オプション
$Forward='転送アドレス';  # Str    # 転送先アドレス
$ExtPref= 'パス優先度';   # int    # External path preference (Section 16.4.1)
$Type1Cost =
    'Type1コスト';        # int    # Type2 外部経路の Type1 コスト
$HasForwarder =
    'Forwarder有';        # bool   # フォワーダがあることを示す
$OnTree = 'OnTree';       # bool   # LSDB 取り込み済を示すフラグ
$Addr = '宛先アドレス';   # String # 経路の宛先アドレス
$LSA = '元のLSA';         # Object # LSA
$Valid = '有効';          # bool   # 有効であることを示すフラグ

################################################################
# ユーティリティ変数
################################################################

# 自分自身を示すコスト
$SelfCost = 'ゼロ(だって自分自身だもの)';

# 経路の優先度表
%rtpri = ('Network' => 2,
	  'Router' => 3,
	  'Stub' => 4,
	  'SumNet' => 5,
	  'ASBR' => 7,
	  'External' => 8,
	  'NSSA' => 8);

# 経路の種別表
%rtype = ('Network' => 'ネットワークアドレス',
	  'Router' => 'ルータID',
	  'Stub' => 'ネットワークアドレス',
	  'SumNet' => 'ネットワークアドレス',
	  'External' => 'ネットワークアドレス',
	  'NSSA' => 'ネットワークアドレス',
	  'ASBR' => 'AS境界ルータ');

# rfc2328 16.4.1 External Path preference
%extpref = ('強い' => 1,
	    '普通' => 2);

# LSA の説明
%lsadesc = ('Router' => 'エリア内のルータ',
	    'Network' => 'エリア内ネットワーク',
	    'Stub' => 'エリア内の末端ネットワーク',
	    'SumNet' => 'エリア外ネットワーク',
	    'SumRtr' => 'エリア外の AS 境界ルータ',
	    'External' => 'AS外部経路',
	    'NSSA' => 'AS外部経路(NSSAエリア用)');

# mask ←→ masklen
@masklen = ('0.0.0.0',
	    '128.0.0.0',
	    '192.0.0.0',
	    '224.0.0.0',
	    '240.0.0.0',
	    '248.0.0.0',
	    '252.0.0.0',
	    '254.0.0.0',
	    '255.0.0.0',
	    '255.128.0.0',
	    '255.192.0.0',
	    '255.224.0.0',
	    '255.240.0.0',
	    '255.248.0.0',
	    '255.252.0.0',
	    '255.254.0.0',
	    '255.255.0.0',
	    '255.255.128.0',
	    '255.255.192.0',
	    '255.255.224.0',
	    '255.255.240.0',
	    '255.255.248.0',
	    '255.255.252.0',
	    '255.255.254.0',
	    '255.255.255.0',
	    '255.255.255.128',
	    '255.255.255.192',
	    '255.255.255.224',
	    '255.255.255.240',
	    '255.255.255.248',
	    '255.255.255.252',
	    '255.255.255.254',
	    '255.255.255.255');
for ($i = 0;  $i < $#masklen;  ++$i)
{
    $masklen{$masklen[$i]} = $i;
}

################################################################
# アップロードされた show ip ospf database detail を読み込む
################################################################
sub lsaname # LSA 識別子
{
    my ($area, $type, $id, $rtr) = @_;
    "Area:$area " . join(':', $type, $id, $rtr);
}
sub rtdest # 経路宛先
{
    my ($type, $dest, $areamask) = @_;
    my ($rtype) = ($rtype{$type});
    if ($rtype eq 'ネットワークアドレス')
    {
	return "$rtype:$dest:$areamask";
    }
    if ($rtype eq 'ルータID')
    {
	return "$rtype:$dest Area:$areamask";
    }
    return "$rtype:$dest";
}
sub rtname # 経路識別子
{
    my ($type, $dest, $areamask, $lsa) = @_;
    join(':', $type, $dest, $areamask, $lsa->{$Name});
}
sub addrval
{
    my ($addr) = @_;
    my (@addr, $val, $i);
    @addr = split(/\./, $addr);
    $val = 0;
    for ($i = $[;  $i <= $#addr;  ++$i)
    {
	$val = ($val * 0x100) + $addr[$i];
    }
    $val;
}
if ($q->param('db'))
{
    $self = $q->param('routerid');
    $text = $q->upload('db');
    $rfc1583compat = $q->param('RFC1583Compat');
    $debug = $q->param('debug');

    while (<$text>)
    {
	# ルータIDの確認
	unless ($self)
	{
	    if (/[Ss]tatistics and variables:/o)
	    {
		$nextwillberouterid = 1;
		next;
	    }
	    if ($nextwillberouterid)
	    {
		if (/Router ID: (\d+\.\d+\.\d+\.\d+)/o)
		{
		    $self = $1;
		}
		$nextwillberouterid = undef;
		next;
	    }
	}

	# show ip ospf database detail のエリア宣言部の読み込み
	if (/^LSA list in the LSDB for area (\d+\.\d+\.\d+\.\d+)/o)
	{
	    ($area) = ($1);
	    $area{$area} = 0;
	    $areaval = &addrval($area);
	    next;
	}
	if (/^LSA list in the LSDB/o)
	{
	    $area = 'Global';
	    $area{$area} = 0;
	    $areaval = 0x100000000;
	    next;
	}

	# LSA 一行目
	if (/^(Router|Network|SumNet|SumRtr|External|NSSA)\s+Id\s+(\d+\.\d+\.\d+\.\d+)\s+Router\s(\d+\.\d+\.\d+\.\d+)/o)
	{
	    ($lstype, $lsid, $adv) = ($1, $2, $3);
	    # $area は前行から継続利用
	    # $lsa は新規作成
	    $name = &lsaname($area, $lstype, $lsid, $adv);

	    $lsa = {};
	    $lsa->{$Text} = $_;
	    $lsa->{$Name} = $name;
	    $lsa->{$Gateway} = {};
	    $lsa->{$Back} = [];
	    $lsa->{$More} = [];

	    $lsa->{$Area} = $area;
	    $lsa->{$LSType} = $lstype;
	    $lsa->{$LSId} = $lsid;
	    $lsa->{$AdvRtr} = $adv;
	    $lsdb{$name} = $lsa;
	    next;
	}

	# LSA 2行目
	if (/^Age\s+(\d+)\s+Seq\s+[\dA-Fa-f]+\s+Sum\s+[\dA-Fa-f]+\s+Length\s+\d+\s+Option\s+<([^<>]*)>/o)
	{
	    ($age, $opt) = ($1, $2);
	    # $lsa, $area, $lsid は継続利用

	    $lsa->{$Text} .= $_;
	    $lsa->{$Age} = int($age);
	    $lsa->{$Opt} = $opt;

	    # Network-LSA の Id 重複は、Age で比較するため
	    # lsdb に特殊な登録をやっておく
	    if ($lstype eq 'Network')
	    {
		$name = &lsaname($area, 'Network', $lsid, undef);
		$old = $lsdb{$name};
		unless (defined $old && $old->{$Age} < $lsa->{$Age})
		{
		    $lsdb{$name} = $lsa;
		    $netdb{$name} = $lsa; # 特殊な登録をあとで消すため
		}
	    }
	    next;
	}

	# Router-LSA Option
	if (/^\s+\#links\s+\d+\s+Option\s+<([^<>]*)>/o)
	{
	    ($opt) = ($1);
	    # $lsa は継続利用
	    $lsa->{$Text} .= $_;
	    $lsa->{$RtrOpt} = $opt;
	    $lsa->{$Link} = ();

	    $lsa->{$Route} = &rtadd('Router', $lsid, undef, $lsa);
	    if (index($opt, 'E') >= $[)
	    {
		$lsa->{$ASBR} = &rtadd('ASBR', $lsid, undef, $lsa);
	    }
	    next;
	}
	# Router-LSA Link
	if (/^\s+(Point-to-Point|P-to-P|Transit|Stub|Virtual|Vlink)\s+Id\s+(\d+\.\d+\.\d+\.\d+)\s+\s+Data\s+(\d+\.\d+\.\d+\.\d+)\s+Metric\s+(\d+)/o)
	{
	    # $lsa は継続利用
	    # $link は新規作成
	    ($type, $linkid, $data, $metric) = ($1, $2, $3, $4);
	    $link = {};

	    $link->{$Text} = $_;
	    $link->{$Metric} = int($metric);
	    $link->{$Area} = $area;
	    $link->{$AreaVal} = $areaval;

	    if ($type eq 'Stub')
	    {
		$link->{$LSType} = 'Stub';
		$link->{$LSId} = $linkid;
		$link->{$Mask} = $data;
		$link->{$Stub} = &rtadd('Stub', $linkid, $data, $lsa);
		$link->{$MyAddr} = "self";
	    }
	    elsif ($type eq 'Transit')
	    {
		$link->{$LSType} = 'Network';
		$link->{$LSId} = $linkid;
		push(@linkdb, $link); # あとで $link->{$AdvRtr} を求める
		$link->{$MyAddr} = "Addr $data";
	    }
	    else
	    {
		$link->{$LSType} = 'Router';
		$link->{$LSId} = $linkid;
		$link->{$AdvRtr} = $linkid;
		if ($type eq 'Virtual'  ||  $type eq 'Vlink')
		{
		    $link->{$MyAddr} = "Virtual $data";
		}
		else
		{
		    $link->{$MyIfp} = "ifIndex $data";
		}
	    }

	    $link->{$LSA} = $lsa;
	    push(@{$lsa->{$Link}}, $link);
	    next;
	}
	
	# Network LSA netmask
	# Summary LSA netmask
	# External LSA netmask
	# NSSA LSA netmask
	if (/^\s+Network Mask (\d+\.\d+\.\d+\.\d+)/o)
	{
	    ($mask) = ($1);
	    $lsa->{$Text} .= $_;
	    if ($lstype eq 'SumRtr')
	    {
		$lsa->{$Route} = &rtadd('ASBR', $lsid, undef, $lsa);
		next;
	    }
	    $lsa->{$Mask} = $mask;
	    $lsa->{$Route} = &rtadd($lstype, $lsid, $mask, $lsa);
	    next;
	}

	# Network LSA link
	if (/^\s+Attached Router\s+(\d+\.\d+\.\d+\.\d+)/o)
	{
	    ($id) = ($1);
	    $link = {};

	    $link->{$Text} = $_;
	    $link->{$Metric} = 0;
	    $link->{$Area} = $area;
	    $link->{$AreaVal} = $areaval;

	    $link->{$LSType} = 'Router';
	    $link->{$LSId} = $id;
	    $link->{$AdvRtr} = $id;
	    $link->{$LSA} = $lsa;
	    $lsa->{$Link} = () unless $lsa->{$Link};
	    push(@{$lsa->{$Link}}, $link);
	    next;
	}

	# Summary LSA
	if (/^\s+TOS\s(\d+)\s+Metric\s+(\d+)/o)
	{
	    ($tos, $metric) = ($1, $2);

	    $lsa->{$Text} .= $_;
	    if (int($tos) == 0)
	    {
		$lsa->{$Metric} = int($metric);
		$origin = $lsdb{&lsaname($area, 'Router', $adv, $adv)};
		if ($origin)
		{
		    push(@{$origin->{$More}}, $lsa);
		    $lsa->{$Back}[$[] = $origin;
		}
	    }
	    next;
	}

	# External LSA
	# NSSA LSA
	if (/^\s+Option\s+<([^<>]*)>\s+TOS\s+(\d+)\s+Metric\s+(\d+)\s+Forwarder\s+(\d+\.\d+\.\d+\.\d+)\s+Tag\s+(\d+)/o)
	{
	    ($opt, $tos, $metric, $forwarder) = ($1, $2, $3, $4);
	    $lsa->{$Text} .= $_;
	    if (int($tos) == 0)
	    {
		$opt = "Type2";
		$lsa->{$ExtOpt} = $opt;
		$lsa->{$Route}->{$ExtOpt} = $opt;
		$lsa->{$Metric} = int($metric);
		$asbrdb{$adv} = () unless $asbrdb{$adv};
		push(@{$asbrdb{$adv}}, $lsa); # ASE有効確認用
		if ($forwarder ne '0.0.0.0')
		{
		    $lsa->{$Forward} = $forwarder;
		    $forwdb{$forwarder} = 1;
		}
	    }
	    next;
	}
    }
}

sub rtadd
{
    my ($type, $dest, $mask, $lsa) = @_;
    my ($rt, $i);
    $rt = {};
    if ($mask)
    {
	if (defined $masklen{$mask})
	{
	    $dest = &addrmask($dest, $mask);
	}
    }
    else
    {
	$mask = $lsa->{$Area};
    }
    $addr = &rtdest($type, $dest, $mask);
    $rt->{$Addr} = $addr;
    $rt->{$Name} = &rtname($type, $dest, $mask, $lsa);
    $rt->{$Pri} = $rtpri{$type};
    $rt->{$LSA} = $lsa;
    $rt->{$ExtPref} =
	(!$rfc1583compat
	 && $lsa->{$Area} ne '0.0.0.0'
	 && ($lsa->{$LSType} eq 'Router'
	     || $lsa->{$LSType} eq 'Network'))
	? '強い' : '普通';
    $rt->{$Back} = ();
    $rt->{$More} = ();
    $rtbl{$addr} = () unless $rtbl{$addr};
    push(@{$rtbl{$addr}}, $rt);
    $rt;
}
sub addrmask
{
    my ($addr, $mask) = @_;
    my (@addr, @mask, $i);
    @addr = split(/\./, $addr);
    @mask = split(/\./, $mask);
    for ($i = $[;  $i <= $#mask;  ++$i)
    {
	$addr[$i] = int($addr[$i]) & int($mask[$i])
    }
    for ($i = $#mask + 1;  $i <= $#addr;  ++$i)
    {
	$addr[$i] = 0;
    }
    join('.', @addr);
}
sub setvalid
{
    my ($list) = @_;

    # check primary route
    @pri = ();
    @transSum = ();
    for $rt (@{$list})
    {
	undef $rt->{$Valid};
	next unless defined $rt->{$Cost};
	next if defined $rt->{$Invalid};
	if ($rt->{$MaybeTransit})
	{
	    push(@transSum, $rt);
	    next;
	}
	if (@pri)
	{
	    if ($pri[$[]->{$Pri} < $rt->{$Pri})
	    {
		next;
	    }
	    if ($pri[$[]->{$Pri} > $rt->{$Pri})
	    {
		@pri = ($rt);
		next;
	    }
	    if ($rt->{$Pri} == $rtpri{'External'})
	    {
		if (!$pri[$[]->{$ExtOpt} &&  $rt->{$ExtOpt})
		{
		    next;
		}
		if ( $pri[$[]->{$ExtOpt} && !$rt->{$ExtOpt})
		{
		    @pri = ($rt);
		    next;
		}
		if ($rt->{$ExtOpt})
		{
		    if ($pri[$[]->{$Cost} < $rt->{$Cost})
		    {
			next;
		    }
		    if ($pri[$[]->{$Cost} > $rt->{$Cost})
		    {
			@pri = ($rt);
			next;
		    }
		}
		if ($extpref{$pri[$[]->{$Back}[$[]->{$ExtPref}} < $extpref{$rt->{$Back}[$[]->{$ExtPref}})
		{
		    next;
		}
		if ($extpref{$pri[$[]->{$Back}[$[]->{$ExtPref}} < $extpref{$rt->{$Back}[$[]->{$ExtPref}})
		{
		    @pri = ($rt);
		    next;
		}
	    }
	    elsif ($rt->{$Pri} == $rtpri{'ASBR'})
	    {
		if ($extpref{$pri[$[]->{$ExtPref}} < $extpref{$rt->{$ExtPref}})
		{
		    next;
		}
		if ($extpref{$pri[$[]->{$ExtPref}} > $extpref{$rt->{$ExtPref}})
		{
		    @pri = ($rt);
		    next;
		}
	    }
	    if ($pri[$[]->{$Cost} < $rt->{$Cost})
	    {
		next;
	    }
	    if ($pri[$[]->{$Cost} > $rt->{$Cost})
	    {
		@pri = ($rt);
		next;
	    }
	    if ($rt->{$ExtOpt})
	    {
		if ($pri[$[]->{$Type1Cost} < $rt->{$Type1Cost})
		{
		    next;
		}
		if ($pri[$[]->{$Type1Cost} > $rt->{$Type1Cost})
		{
		    @pri = ($rt);
		    next;
		}
	    }
	}
	push(@pri, $rt);
    }
    if (@pri)
    {
	for $rt (@transSum)
	{
	    if ($rt->{$Cost} > $pri[$[]->{$Cost})
	    {
		next;
	    }
	    if ($rt->{$Cost} < $pri[$[]->{$Cost})
	    {
		@pri = ();
	    }
	    push(@pri, $rt);
	}
    }
    for $rt (@pri)
    {
	$rt->{$Valid} = 1;
    }
}
sub getvalid
{
    my ($addr) = @_;
    &getvalidfromlist($rtbl{$addr});
}
sub getvalidfromlist
{
    my ($list) = @_;
    my ($rt);

    for $rt (@{$list})
    {
	return $rt if $rt->{$Valid};
    }
    undef;
}

################
# ぜんぶ読み終えたら
# Router-LSA から Transit Link を適正にする
# Network-LSA の lsdb への特殊な登録を外す
################
for $link (@linkdb)
{
    $net = $lsdb{&lsaname($link->{$Area}, 'Network',
			  $link->{$LSId}, undef)};
    if ($net)
    {
	$link->{$AdvRtr} = $net->{$AdvRtr};
    }
}
for $name (keys %netdb)
{
    undef $lsdb{$name};
}

################################################################
# 経路計算
################################################################
# エリア内
################
@cand = ();
%lsapri = ('Network' => 1,
	   'Router' => 2,
	   'Stub' => 3,
	   'SumRtr' => 4,
	   'SumNet' => 5,
	   'External' => 6,
	   'NSSA' => 6);
sub pushlink
{
    my ($link) = @_;
    my ($cost, $areaval) = ($link->{$Cost}, $link->{$AreaVal});
    my ($pri, $i);
    $pri = $lsapri{$link->{$LSType}};
    $link->{$Pri} = $pri;
    for ($i = $[;  $i <= $#cand;  ++$i)
    {
	next if $cand[$i]->{$Cost} < $cost;
	last if $cand[$i]->{$Cost} > $cost;
	next if $cand[$i]->{$Pri} < $pri;
	last if $cand[$i]->{$Pri} > $pri;
	next if $cand[$i]->{$AreaVal} < $areaval;
	last if $cand[$i]->{$AreaVal} > $areaval;
    }
    splice(@cand, $i, 0, $link);
}

while (($area, $val) = each %area)
{
    next if $area eq 'Global';
    $link = {};
    $link->{$Area} = $area;
    $link->{$AreaVal} = &addrval($area);
    $link->{$LSType} = 'Router';
    $link->{$LSId} = $self;
    $link->{$AdvRtr} = $self;
    $link->{$Cost} = $SelfCost;
    # ↑ 本当なら {$Cost} = 0 とすべき箇所だけど
    # FALSE 判定されてしまうのが嫌だから胡麻化す
    $link->{$Root} = 1;
    pushlink($link);
}
@root = @cand;

# @cand からひとつづつチェック
while (@cand)
{
    $link = shift(@cand);

    $lsa = $lsdb{&lsaname($link->{$Area}, $link->{$LSType},
			  $link->{$LSId}, $link->{$AdvRtr})};
    # link 先 LSA の存在と Age の確認
    next unless $lsa;
    if (!defined($lsa->{$Age})  ||  $lsa->{$Age} >= 3600)
    {
	$link->{$Invalid} = 'MaxAge';
	$lsa->{$Invalid} = 'MaxAge';
	next;
    }

    # Root じゃない LSA があれば、経路計算対象エリアとして登録する
    # あとでサマリ計算するかどうかの判断に使う。
    $parent = $link->{$LSA};
    $area = $link->{$Area};
    if ($parent)
    {
	$validarea{$area} = 1;
    }

    # コスト確認
    next if (defined($lsa->{$Cost}) && $lsa->{$Cost} < $link->{$Cost});

    $rt = $lsa->{$Route};
    $asbr = $lsa->{$ASBR};

    # LinkBack 確認と Peer addr 取得
    if ($parent)
    {
	$lstype = $parent->{$LSType};
	$lsid = $parent->{$LSId};
	$rtr = $parent->{$AdvRtr};
	for $back (@{$lsa->{$Link}})
	{
	    if ($back->{$LSType} eq $lstype
		&& $back->{$LSId} eq $lsid
		&& $back->{$AdvRtr} eq $rtr)
	    {
		$link->{$LinkBackOk} = 1;
		$back->{$BackLink} = 1;
		push(@{$parent->{$More}}, $lsa);
		push(@{$parent->{$Route}->{$More}}, $rt);
		push(@{$parent->{$Route}->{$More}}, $asbr) if $asbr;
		push(@{$lsa->{$Back}}, $parent);
		push(@{$rt->{$Back}}, $parent->{$Route});
		push(@{$asbr->{$Back}}, $parent->{$Route}) if $asbr;
		$peer = $back->{$MyAddr} || $link->{$MyIfp};
		last;
	    }
	}
	unless ($link->{$LinkBackOk})
	{
	    $link->{$Invalid} = 'NoBackLink';
	    next;
	}
    }

    # OK.
    if (defined($lsa->{$Cost}) && $lsa->{$Cost} > $link->{$Cost})
    {
	# reset gateway
	$lsa->{$Gateway} = {};
	$rt->{$Gateway} = {} if $rt;
	$asbr->{$Gateway} = {} if $asbr;
    }
    if ($lsa->{$LSType} eq 'Router'
	&& $area ne '0.0.0.0'
	&& index($lsa->{$RtrOpt}, 'V') >= $[)
    {
	$transit{$area} = 1;
    }
    $lsa->{$Cost} = $link->{$Cost};
    $rt->{$Cost} = $lsa->{$Cost} if $rt;
    $asbr->{$Cost} = $lsa->{$Cost} if $asbr;

    # $self もしくは $self 隣接 Network には {$Root} を作る
    # 以遠には {$Gateway} を作る
    if ($link->{$Root})
    {
	if ($lsa->{$LSType} eq 'Network')
	{
	    $gw = 'Connected';
	    $lsa->{$Gateway}->{$gw} = $parent->{$Name};
	    $rt->{$Gateway} = $lsa->{$Gateway} if $rt;
	}
	for $next (@{$lsa->{$Link}})
	{
	    if ($next->{$LSType} eq 'Network')
	    {
		$next->{$Root} = 1;
	    }
	    else
	    {
		$next->{$Peer} = 1;
	    }
	}
    }
    else
    {
	if ($link->{$Peer})
	{
	    $lsa->{$Gateway}->{$peer} = $lsa->{$Name};
	}
	while (($gw, $val) = each %{$parent->{$Gateway}})
	{
	    next if $gw eq 'Connected';
	    $lsa->{$Gateway}->{$gw} = $val;
	}
	$rt->{$Gateway} = $lsa->{$Gateway} if $rt;
	$asbr->{$Gateway} = $lsa->{$Gateway} if $asbr;
    }

    # Link 登録
    for $next (@{$lsa->{$Link}})
    {
	$next->{$Cost} = $lsa->{$Cost} + $next->{$Metric};
	if ($next->{$LSType} eq 'Stub')
	{
	    $rt = $next->{$Stub};
	    $rt->{$Cost} = $next->{$Cost} if $rt;
	    next;
	}
	&pushlink($next);
    }

    push(@tree, $lsa);
}

################
# サマリ
################
$bb = $validarea{'0.0.0.0'};
for $rtr (@tree)
{
    next unless $rtr->{$LSType} eq 'Router';
    for $sum (@{$rtr->{$More}})
    {
	next unless ($sum->{$LSType} eq 'SumNet'
		     || $sum->{$LSType} eq 'SumRtr');
	$rt = $sum->{$Route};
	if ($rtr->{$Cost} <= 0)
	{
	    $sum->{$Invalid} = '自分がアナウンスしてる奴なので無視';
	    $rt->{$Invalid} = '自分がアナウンスしてる奴なので無視';
	    next;
	}
	if (!defined($sum->{$Age}) || $sum->{$Age} >= 3600)
	{
	    $sum->{$Invalid} = 'MaxAge';
	    $rt->{$Invalid} = 'MaxAge';
	    next;
	}
	if (!defined($sum->{$Metric}) || $sum->{$Metric} >= 0xffffff)
	{
	    $sum->{$Invalid} = 'コスト ∞';
	    $rt->{$Invalid} = 'コスト ∞';
	    next;
	}
	if ($bb  &&  $rtr->{$Area} ne '0.0.0.0')
	{
	    if ($transit{$rtr->{$Area}})
	    {
		$cost = $rtr->{$Cost} + $sum->{$Metric};
		$sum->{$Cost} = $cost;
		$rt->{$Cost} = $cost;
		$gw = $rtr->{$Gateway};
		$sum->{$Gateway} = $gw;
		$rt->{$Gateway} = $gw;
		$rt->{$MaybeTransit} = 1;
		push(@tree, $sum);
	    }
	    else
	    {
		$sum->{$Invalid} ='バックボーンエリアではないので無視';
		$rt->{$Invalid} = 'バックボーンエリアではないので無視';
	    }
	}
	else
	{
	    $cost = $rtr->{$Cost} + $sum->{$Metric};
	    $sum->{$Cost} = $cost;
	    $rt->{$Cost} = $cost;
	    $gw = $rtr->{$Gateway};
	    $sum->{$Gateway} = $gw;
	    $rt->{$Gateway} = $gw;
	    $rt->{$Back}[$[] = $rtr;
	    push(@tree, $sum);
	}
    }
}

################
# さてこのへんで一度、エリア内経路とサマリ経路の優先度を整理しておこう
################
while (($addr, $list) = each %rtbl)
{
    &setvalid($list);
}

################
# 最後に ASE と NSSA
################
# 事前に Forwarder に対する NET 経路をひっぱって一覧にしておく
# この時点ではまだ External や NSSA に {'Valid '} は付いてないので
# エリア内またはエリア間パスのみを使って確認できる
@forwarder = keys %forwdb;
%forwdb = ();
for $forwarder (@forwarder)
{
    for ($i = $#masklen;  $i >= 0;  --$i)
    {
	$rt = &getvalid(&rtdest('Network', &addrmask($forwarder, $masklen[$i]), $masklen[$i]));
	next unless $rt;
	$forwdb{$forwarder} = $rt;
    }
}

# ASBR を基に外部経路を確認し、可能なら {$Valid} を立てる
# もし Forwarder もあれば、つい今しがた構築した %forwdb を使う
while (($adv, $aselist) = each %asbrdb)
{
    $asbr = &getvalid(&rtdest('ASBR', $adv, undef));
    next unless $asbr;
    if ($asbr->{$Invalid})
    {
	for $ase (@{$aselist})
	{
	    push(@{$asbr->{$More}}, $ase);
	    $ase->{$Invalid} = $rt->{$Invalid};
	}
	next;
    }
    if ($asbr->{$Cost} eq $SelfCost)
    {
	for $ase (@{$aselist})
	{
	    push(@{$asbr->{$More}}, $ase);
	    $ase->{$Invalid} = '自分がアナウンスしてる奴なので無視';
	    $ase->{$Route}->{$Invalid} = '自分がアナウンスしてる奴なので無視';
	}
	next;
    }
    for $ase (@{$aselist})
    {
	push(@{$asbr->{$More}}, $ase);
	$rt = $ase->{$Route};
	if (!defined($ase->{$Age})  ||  $ase->{$Age} >= 3600)
	{
	    $ase->{$Invalid} = 'MaxAge';
	    $rt->{$Invalid} = 'MaxAge';
	    next;
	}
	if (!defined($ase->{$Metric})  ||  $ase->{$Metric} >= 0xffffff)
	{
	    $ase->{$Invalid} = 'コスト ∞';
	    $rt->{$Invalid} = 'コスト ∞';
	    next;
	}
	if ($ase->{$Forward})
	{
	    $forw = $forwdb{$ase->{$Forward}};
	    next unless $forw;
	    push(@{$forw->{$More}}, $ase);
	    $rt->{$Forward} = $ase->{$Forward};
	    $ase->{$Back}[$[] = $forw;
	    $rt->{$Back}[$[] = $forw;
	    if ($ase->{$ExtOpt})
	    {
		$cost1 = $ase->{$Metric};
		$ase->{$Cost} = $cost1;
		$rt->{$Cost} = $cost1;
		$gw = $forw->{$Gateway};
		$ase->{$Gateway} = $gw;
		$rt->{$Gateway} = $gw;
		$cost2 = $forw->{$Cost};
		$cost = $cost1 + $cost2;
		$ase->{$Type1Cost} = $cost;
		$rt->{$Type1Cost} = $cost;
	    }
	    else
	    {
		$cost1 = $ase->{$Metric};
		$cost2 = $forw->{$Cost};
		$cost = $cost1 + $cost2;
		$ase->{$Cost} = $cost;
		$rt->{$Cost} = $cost;
		$gw = $forw->{$Gateway};
		$ase->{$Gateway} = $gw;
		$rt->{$Gateway} = $gw;
	    }
	}
	else
	{
	    $ase->{$Back}[$[] = $asbr;
	    $rt->{$Back}[$[] = $asbr;
	    if ($ase->{$ExtOpt})
	    {
		$cost1 = $ase->{$Metric};
		$ase->{$Cost} = $cost1;
		$rt->{$Cost} = $cost1;
		$cost2 = $asbr->{$Cost};
		$cost = $cost1 + $cost2;
		$ase->{$Type1Cost} = $cost;
		$rt->{$Type1Cost} = $cost;
		$gw = $asbr->{$Gateway};
		$ase->{$Gateway} = $gw;
		$rt->{$Gateway} = $gw;
	    }
	    else
	    {
		$cost1 = $ase->{$Metric};
		$cost2 = $asbr->{$Cost};
		$cost = $cost1 + $cost2;
		$ase->{$Cost} = $cost;
		$rt->{$Cost} = $cost;
		$gw = $asbr->{$Gateway};
		$ase->{$Gateway} = $gw;
		$rt->{$Gateway} = $gw;
	    }
	}
	push(@tree, $ase);
	$asedb{$rt->{$Addr}} = 1; # 追加があったアドレスを覚えとく
    }
}
# 追加があったアドレスの最優先経路を求め直す
while (($addr, $val) = each %asedb)
{
    &setvalid($rtbl{$addr});
}

# %rtbl を宛先順にソートする
%rttype = ('ネットワークアドレス' => 1, 'AS境界ルータ' => 2, 'ルータID' => 3);
while (($dest, $list) = each %rtbl)
{
    @dest = split(/[:\.]/, $dest);
    $dest[$[] = $rttype{$dest[$[]};
    $rtval{$dest} = ();
    push(@{$rtval{$dest}}, @dest);
}
sub sortaddr
{
    my ($i, $aa, $bb, $len, $lencmp);
    $aa = $rtval{$a};
    $bb = $rtval{$b};
    $lencmp = $#{$aa} - $#{$bb};
    $len = $#{$aa};
    $len = $#{$bb} if $#{$bb} < $len;
    for ($i = $[;  $i <= $len;  ++$i)
    {
	return ${$aa}[$i] <=> ${$bb}[$i] if ${$aa}[$i] != ${$bb}[$i];
    }
    $lencmp;
}
@rtaddrs = sort sortaddr keys %rtbl;

# 最後に、到達不可能だった奴等をリストに取り込む
for ($i = $[;  $i <= $#tree;  ++$i)
{
    $tree[$i]->{$OnTree} = 1;
}
while (($name, $lsa) = each %lsdb)
{
    next unless $lsa;
    if ($lsa->{$OnTree})
    {
	undef $lsa->{$OnTree};
	next;
    }
    push(@tree, $lsa);
    next if $lsa->{$Invalid};
    &setunreach($lsa);
    &setunreach($lsa->{$Route});
    &setunreach($lsa->{$ASBR});
    for $link (@{$lsa->{$Link}})
    {
	&setunreach($link->{$Stub});
    }
}
sub setunreach
{
    my ($item) = @_;
    $item->{$Invalid} = 'Unreachable' if $item;
}

################################################################
# 入力内容や読み込んだ内容などをベースに
# データ入力フォームを表示する
################################################################
print $q->start_multipart_form."\n";
print $q->ul($q->li($q->filefield('db'), 'show ip ospf database detail によって取得したファイル'),
	     $q->param('db') ? $q->ul($q->li($q->param('db'))) : undef,
	     $q->li($q->textfield('routerid', $self),
		    '経路計算したいルータの Router ID (show ip ospf database detail に含まれていれば不要) '),
	     $self ? $q->ul($q->li("Router ID = $self")) : undef,
	     $q->li($q->checkbox(-name => 'RFC1583Compat',
				 -checked => $q->param('RFC1583Compat'),
				 -value => 'on')),
	     $q->li($q->checkbox(-name => 'debug',
				 -value => 'on')));
print $q->submit('calc', '計算')
    . $q->reset
    . $q->submit('description', 'このプログラムの説明と使いかた')
    . $q->submit('source', 'このプログラムのソースコード')
    . $q->submit('history', '開発履歴')
    . $q->submit('todo', 'ToDo')
    . $q->submit('thanksto', 'Thanks To')
    . "\n";

if ($q->param('description'))
{
    &description;
    print $q->end_div;
    print $q->end_html;
    exit 0;
}

if ($q->param('history'))
{
    &show_and_exit('更新履歴', @history);
    exit 0;
}
if ($q->param('todo'))
{
    &show_and_exit('ToDo', @todo);
    exit 0;
}
if ($q->param('thanksto'))
{
    &show_and_exit('Thanks to', @thanksto);
    exit 0;
}

if (!$q->param('db'))
{
    print $q->end_form . "\n";
    print $q->end_div;
    print $q->end_html;
    exit;
}

print $q->br . 'Jump to ';
print $q->a({-href => '#%rtbl'}, "経路表");
print $q->br . 'Jump to ';
print $q->a({-href => '#%lsdb'}, "LSDB") . "\n";


################################################################
# show ip ospf route
################################################################
print $q->hr;
print $q->a({-name => '%rtbl'}, "経路表") . $q->br . "\n";
%ignore = ($Name => 1,
	   $Pri => 1,
	   $Addr => 1) unless $debug;
$ignore{$ExtOpt} = 1 if !$debug && $rfc1583compat;
for $addr (@rtaddrs)
{
    $list = $rtbl{$addr};
    $txt1 = &getvalid($addr) ? "*" : " ";
    $txt1 .= " $addr";
    print $q->a({-name => $addr}, $txt1)."\n";
    for $rt (@{$list})
    {
	$txt1 = $rt->{$Valid} ? "* " : "  ";
	$txt1 .= $lsadesc{$rt->{$LSA}->{$LSType}} . ' ';
	$txt1 .= $q->a({-name => $rt->{$Name}}, $rt->{$Addr})."\n";

	$txt2 = '';
	while (($tag, $val) = each %{$rt})
	{
	    next unless $val;
	    next if $ignore{$tag};
	    if ($tag eq $More  ||  $tag eq $Back)
	    {
		# ARRAYs (#href #val)
		for $more (@{$val})
		{
		    $txt3 = $more->{$Name};
		    $txt4 = $more->{$Addr} || $txt3;
		    $txt3 = $q->a({-href => "#$txt3"}, $txt4);
		    $txt2 .= "\t[$tag = $txt3]\n";
		}
		next;
	    }
	    if ($tag eq $Gateway)
	    {
		# HASH keys (href #val)
		while (($txt3, $val3) = each %{$val})
		{
		    $txt3 = $q->a({-href => "#$val3"}, $txt3);
		    $txt2 .= "\t[$tag = $txt3]\n";
		}
		next;
	    }
	    if ($tag eq $LSA)
	    {
		# Links
		$txt3 = $val->{$Name};
		$txt3 = $q->a({-href => "#$txt3"}, $txt3);
		$txt2 .=  "\t[$tag = $txt3]\n";
		next;
	    }
	    $txt2 .= "\t[$tag = $val]\n";
	}
	$txt1 .= $q->i($txt2);
	$txt1 = $q->pre($txt1);
	$txt1 = $q->blockquote({-style => 'border: 3px double;'}, $txt1);
	print "$txt1\n";
    }
}

################################################################
# show ip ospf database
################################################################
print $q->hr;
print $q->a({-name => '%lsdb'}, "LSDB") . $q->br . "\n";
%ignore = ($Name => 1,
	   $Text => 1,
	   $LSId => 1,
	   $Mask => 1,
	   $Area => 1,
	   $AreaVal => 1,
	   $LSType => 1,
	   $LSId => 1,
	   $AdvRtr => 1,
	   $Age => 1,
	   $Opt => 1,
	   $RtrOpt => 1,
	   $Pri => 1,
	   $Metric => 1,
	   $Link => 1,
	   $MyAddr => 1,
	   $MyIfp => 1,
	   $Root => 1,
	   $Peer => 1,
	   $ExtOpt => 1,
	   $OnTree => 1) unless $debug;
for $lsa (@tree)
{
    $txt1 = "Area " . $lsa->{$Area};
    $txt1 .= ",  Cost " . $lsa->{$Cost} if defined $lsa->{$Cost};
    print "$txt1\n";

    $txt1 = $q->escapeHTML($lsa->{$Text});
    $txt1 = $q->a({-name => $lsa->{$Name}}, $txt1) . "\n";

    $txt2 = '';
    while (($tag, $val) = each %{$lsa})
    {
	next unless $val;
	next if $ignore{$tag};
	if ($tag eq $More  ||  $tag eq $Back)
	{
	    # ARRAYs
	    for $more (@{$val})
	    {
		$txt3 = $more->{$Name};
		$txt4 = $more->{$Addr} || $txt3;
		$txt3 = $q->a({-href => "#$txt3"}, $txt4);
		$txt2 .= "\t[$tag = $txt3]\n";
	    }
	    next;
	}
	if ($tag eq $Gateway)
	{
	    # HASH keys (href #val)
	    while (($txt3, $val3) = each %{$val})
	    {
		$txt3 = $q->a({-href => "#$val3"}, $txt3);
		$txt2 .= "\t[$tag = $txt3]\n";
	    }
	    next;
	}
	if ($tag eq $Route  ||  $tag eq $ASBR)
	{
	    $txt3 = $val->{$Name};
	    $txt4 = $val->{$Addr} || $txt3;
	    $txt3 = $q->a({-href => "#$txt3"}, $txt4);
	    $txt2 .= "\t[$tag = $txt3]\n";
	    next;
	}
	$txt3 = "\t[$tag = $val]\n";
	$txt2 .= $txt3;
    }
    $txt1 .= $q->i($txt2);

    for $link (@{$lsa->{$Link}})
    {
	$txt2 = $link->{$Text};
	if ($txt2 =~ /^\s*(\S.+)\s*$/o)
	{
	    $txt3 = $1;
	    $ref = &lsaname($lsa->{$Area}, $link->{$LSType},
			    $link->{$LSId}, $link->{$AdvRtr});
	    $txt3 = $q->a({-href => "#$ref"}, $txt3);
	    $txt2 =~ s/^(\s*)\S.*(\s*)$/$1$txt3$2/g;
	}
	$txt1 .= "\n$txt2";

	$txt2 = "";
	while (($tag, $val) = each %{$link})
	{
	    next unless $val;
	    next if $ignore{$tag};
	    if ($tag eq $Gateway)
	    {
		# HASH keys (href #val)
		while (($txt3, $val3) = each %{$val})
		{
		    $txt3 = $q->a({-href => "#$val3"}, $txt3);
		    $txt2 .= "\t[$tag = $txt3]\n";
		}
		next;
	    }
	    if ($tag eq $LSA || $tag eq $Stub)
	    {
		$txt3 = $val->{$Name};
		$txt4 = $val->{$Addr} || $txt3;
		$txt3 = $q->a({-href => "#$txt3"}, $txt4);
		$txt2 .= "\t\t[$tag = $txt3]\n";
		next;
	    }
	    $txt2 .= "\t\t[$tag = $val]\n";
	}
	$txt1 .= $q->i($txt2);
    }
    $txt1 = $q->pre($txt1);
    $txt1 = $q->blockquote({-style => 'border: 3px double;'}, $txt1)."\n";
    $txt1 .= $q->br;
    print "$txt1\n";
}

################################################################
# 文末
################################################################
print '(以下余白)' . $q->br x 100;
print $q->end_div;
print $q->end_html;
