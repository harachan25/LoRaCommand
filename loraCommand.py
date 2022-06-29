#lenはcmdとparamの長さの合計バイト
#送信は16進数で読み込みはアスキー

import binascii
import datetime


#4040ff4154 + <len({22+文字数}/2)> + AAAA0001ffffffffffff + <文字数> + <“[done*180000]*10”>          +  AA
#4040ff4154   1b                    AAAA0001ffffffffffff   10        5b646f6e652a3138303030305d2a3130 AA


#command = first + len1 +  midium + len2 + cmd0 + last
first =  '4040ff4154'
#len1 ←len後からAA前までの文字数（{20 + len(cmd1)}/2）を16進数にした文字列
middle = 'AAAA0001ffffffffffff'
#len2 ← len(cmd1)/2を16進数にした文字列
#cmd1 = '' アスキー文字のコマンドを16進数にした文字列，今回のコマンドは[done*180000]*10
last = 'AA'


#時間取得
dt_now = datetime.datetime.now()
time = dt_now.strftime ('%H%M%S')
print(time)
#cmd1
c1 = input()


if　c1 == "pos":
    #c2 =
    c2len = int(len(c2))
    c3 = "[" + c1 + "*" + time + "]*" + c2len
elif c1 == "rec": #受信したことを伝える
    c2 = c1 + "*" + time
    c2len = int(len(c2))
    c3 = "[" + c2 + "]*" + c2len
elif c1 == "rssi":
    c2 = c1 + "*" + time
    c2len = int(len(c2))
    c3 = "[" + c2 + "]*" + c2len
elif c1 == "goto":
    #c2 =
    c2len = int(len(c2))
    c3 = "[" + c1 + "*" + time + "]*" + c2len
elif c1 == "come":
    c2 = c1 + "*" + time
    c2len = int(len(c2))
    c3 = "[" + c2 + "]*" + c2len
elif c1 == "rqps":
    #c2 =
    c2len = int(len(c2))
    c3 = "[" + c1 + "*" + time + "]*" + c2len
elif c1 == "rqrs":
    #c2 =
    c2len = int(len(c2))
    c3 = "[" + c1 + "*" + time + "]*" + c2len
elif c1 == "done":
    c2 = c1 + "*" + time
    c2len = int(len(c2))
    c3 = "[" + c2 + "]*" + c2len
elif c1 == "err":
   #c2 = 
    c2len = int(len(c2))
    c3 = "[" + c1 + "*" + time + "]*" + c2len
    #引数なし
elif c1 == "remi":
    c2 = c1
    c2len = int(len(c2))
    c3 = "[" + c1 + "*" + c2len
else:
  c3= "none"
  

cmd0 = str(binascii.hexlify(c3.encode()))
cmd1 = cmd0[2:len(cmd0)-1]

#len2
num2 = int(len(cmd1) /2)
len2 = hex(num2)[2:] # num2に格納された数字を16進数の文字列にして代入

#len1
num1 = int((len(middle) + len(len2) + len(cmd1))/2)
len1 = hex(num1)[2:] # num1に格納された数字を16進数の文字列にして代入


command = first + len1 +  middle + len2 + cmd1 + last
print(command)
