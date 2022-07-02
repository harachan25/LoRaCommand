#lenはcmdとparamの長さの合計バイト
#送信は16進数で読み込みはアスキー

import binascii
import datetime
import struct


#4040ff4154 + <len({22+文字数}/2)> + AAAA0001ffffffffffff + <文字数> + <“[done*180000]*10”>          +  AA
#4040ff4154   1b                    AAAA0001ffffffffffff   10        5b646f6e652a3138303030305d2a3130 AA


#command = first + len1 +  midium + len2 + cmd0 + last
first =  '4040ff4154'
#len1 ←len後からAA前までの文字数（{20 + len(cmd1)}/2）を16進数にした文字列
middle = 'AAAA0001ffffffffffff'
#len2 ← len(cmd1)/2を16進数にした文字列
#cmd1 = '' アスキー文字のコマンドを16進数にした文字列，例：[done*180000]*10
last = 'AA'


#時間取得
dt_now = datetime.datetime.now()
time = dt_now.strftime ('%H%M%S')
print(time)
#cmd1
c0 = input()


# bitDouble: double(64ビット長)を、8bitずつ(0x00 ~ 0xFF)に区切って8ビットを生成した型
# 64bitを8bitずつ8桁にして生成する
if c0 == "pos":
# c1 = 緯度: bitDouble, c2 = 経度: bitDouble
    c1 = input() #64bitを文字列としてc1に格納
    c2 = input()
    i = 0
    j = 0
    C1 = 0 #-3.141519
    C1_1 = struct.pack('>d', C1) #b'\xc0\t!\xd4\xb6\xa6\x19\xdb'
    C1_2 = struct.unpack('>Q', C1_1)[0] #13837628527553681883
    C1_3 = bin(C1_2) #'0b1100000000001001001000011101010010110110101001100001100111011011'
    C1_3[2:len(C1_3)] #'1100000000001001001000011101010010110110101001100001100111011011'
    C2 = 0
    C2_1 = struct.pack('>d', C2)
    C2_2 = struct.unpack('>Q', C2_1)[0]
    C2_3 = bin(C2_2)
    C2_3[2:len(C2_3)]
    for i in range(8): #8回繰り返す
        c1_i = int(c1[8*i:8*i+8]) #文字列c1から8文字(8桁)ずつ取り出す
        c2_i = int(c2[8*i:8*i+8])
        print(hex((c1_i)))
        print(hex((c2_i)))
        C1 = str(C1) + str(str(c1_i)[2:len(hex(c1_i))-1]) #取り出した8文字を16進数に変換して足す
        C2 = str(C2) + str(str(c2_i)[2:len(hex(c2_i))-1])
        print(C1)
        i = i + 1
    c9 = c0 + "*" + C1 + "*" + C2 + "*" + time
elif c0 == "rec": #受信したことを伝える
    c9 = c0 + "*" + time
    
elif c0 == "rssi":
    c9 = c0 + "*" + time
    
elif c0 == "goto":
#c1 = 緯度: bitDouble, c2 = 経度: bitDouble
    c1 = input()
    c2 = input()
    c9 = c0 + "*" + c1 + "*" + c2 + "*" + time
    
elif c0 == "come":##
    c9 = c0 + "*" + time
    
elif c0 == "rqps":##
    c9 = c0 + "*" + time
    
elif c0 == "rqrs":
    c1 = input() #c2秒間でc1回送信
    c2 = input()
    c9 = c0 + "*" + c1 + "*" + c2 + "*" + time
    
elif c0 == "done":##
    c9 = c0 + "*" + time
    
elif c0 == "err":
    c1 = input()
    c9 = c0 + "*" + c1 + "*" + time
    
elif c0 == "remi":
    c9 = c0
elif c0 == "sacc":
    c1 = input() #データ数(以下データ数分だけ繰り返す): int
    c2 = input() #緯度
    c3 = input() #経度
    c4 = input() #加速度L2ノルム: bitDouble
    c9 = c0 + "*" + str(c1) + "*" + c2 + "*" + c3 + "*" + c4
elif c0 == "srun":
    c1 = input() #状態(反転/0,横転/1,復帰不可/2): int
    c2 = input() #緯度
    c3 = input() #経度
    c9 = c0 + "*" + str(c1) + "*" + c2 + "*" + c3
    
else:
  c9= "none"
  
  
c9len = str(len(c9))
c = "[" + c9 + "]*" + c9len
cmd0 = str(binascii.hexlify(c.encode()))
cmd1 = cmd0[2:len(cmd0)-1]

#len2
num2 = int(len(cmd1) /2)
len2 = hex(num2)[2:] # num2に格納された数字を16進数の文字列にして代入

#len1
num1 = int((len(middle) + len(len2) + len(cmd1))/2)
len1 = hex(num1)[2:] # num1に格納された数字を16進数の文字列にして代入


command = first + len1 +  middle + len2 + cmd1 + last
print(command)
