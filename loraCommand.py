##メモ##
#送信は16進数で読み込みはアスキー
#binascii.hexlify(data[, sep[, bytes_per_sep=1]]):バイナリデータの16進数表現，データの各バイトは対応する2桁の16進数になる
#'文字列'.encode('文字コード名'):文字列をバイトに変換
#b'バイト列'.decode('文字コード名'):バイトを文字列に変換

##フォーマットと例##
#command = first + len(cmd + param) + cmd + param + last
#4040ff4154 + <len({22+文字数}/2)> + AAAA0001ffffffffffff + <文字数> + <“[done*180000]*10”> +  AA
#4040ff4154 + 1b + AAAA0001ffffffffffff + 10 + 5b646f6e652a3138303030305d2a3130 + AA
###プログラム###
import binascii
import datetime
import struct

##取得##
#時間取得
dt_now = datetime.datetime.now()
time = dt_now.strftime ('%H%M%S')
print("time:",time)

##入力##
param1 = input('送信先アドレス(param1):').zfill(4)
c0 = input('command:')

#コマンドと引数#
# bitDouble: double(64ビット長)を、8bitずつ(0x00 ~ 0xFF)に区切って8ビットを生成した型
# 64bitを8bitずつ8桁にして生成する
if c0 == "pos" or c0 =="goto":# c1 = 緯度: bitDouble, c2 = 経度: bitDouble
    c1 = input('latitude:')#64bitを文字列としてc1に格納
    c2 = input('longtitude:')
    param6in = c0 + "*" + c1 + "*" + c2 + "*" + time
    
#rec:受信したことを伝える
elif c0 == "rec" or c0 == "rssi" or c0 == "come" or c0 == "rqps" or c0 == "done":
    param6in = c0 + "*" + time
    
elif c0 == "rqrs":
    c1 = input('何秒間で:')
    c2 = input('何回送る:')#c1秒間でc2回送信
    param6in = c0 + "*" + c2 + "*" + c1 + "*" + time
    
elif c0 == "err":
    c1 = input('エラー名:')
    param6in = c0 + "*" + c1 + "*" + time
    
elif c0 == "remi":
    param6in = c0
    
elif c0 == "srun":#探索データ送信(走行状態, 復帰の可否が分かり次第送信)
    c1 = input('状態(反転/0,横転/1,スタック/2,復帰不可/3):int')
    c2 = input('latitude:') #緯度
    c3 = input('longtitude:') #経度
    param6in = c0 + "*" + str(c1) + "*" + c2 + "*" + c3
    
    elif c0 == "rout":#移動経路送信
    c1 = input('データNo.(-1で終了): int')
    c2 = input('latitude:') #緯度
    c3 = input('longtitude:') #経度
    param6in = c0 + "*" + str(c1) + "*" + c2 + "*" + c3
    
elif c0 == "saft":#安全性評価データ送信
    c1 = input('安全性評価データ: int(0 ~ INT_MAX)')
    c2 = input('latitude:') #緯度
    c3 = input('longtitude:') #経度
    param6in = c0 + "*" + str(c1) + "*" + c2 + "*" + c3
    
elif c0 == "por":#複数ローバの座標等の情報送信
    c1 = input('データ数(以下データ数分だけ繰り返す): int')
    c2 = input('latitude:') #緯度
    c3 = input('longtitude:') #経度
    param6in = c0 + "*" + str(c1) + "*" + c2 + "*" + c3
    
else:
 for i in range(3):
  print("check your input")
  i = i + 1
  param6in = c0
  




##フォーマット##
first = "@@FFAT" #@@FFAT
cmd = "AAAA" #AAAA
#param1 = 入力 #0001
param2to4 = "ffffffffffff" #コマンド内容
#param6in = #done*180000
param6 ="[" + param6in + "]*" + str(len(param6in)) #[done*180000]*11
param5 = len(param6)-1 #10([]内の*の数を抜いた長さ)
param = str(param1) + param2to4 + str(param5) + param6 #0001ffffffffffff10[done*180000]
last = "AA"
command = first +  str(len(cmd + param)) + cmd + param + last
Command = str(binascii.hexlify(command.encode()))
Command = Command[2:len(Command)-1]
##出力
print (Command)


##確認用(16進数のコマンドをアスキー文字に変換)
Default = str(binascii.unhexlify(Command))
Default = Default[2:len(Default)-1]
print("送信内容:" + Default)
