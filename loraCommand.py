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
Time = str(binascii.hexlify(time.encode()))

#cmd1
c0 = input('command:')
#前半:
fo = c0 + "*"
Fo = str(binascii.hexlify(fo.encode()))

# bitDouble: double(64ビット長)を、8bitずつ(0x00 ~ 0xFF)に区切って8ビットを生成した型
# 64bitを8bitずつ8桁にして生成する
if c0 == "pos" or c0 =="goto":# c1 = 緯度: bitDouble, c2 = 経度: bitDouble
    c1 = input('latitude:')#64bitを文字列としてc1に格納
    c2 = input('longtitude:')
    
    i = 0
    C1 = ""
    C1_a = struct.pack('>d', float(c1)) #b'\xc0\t!\xd4\xb6\xa6\x19\xdb'
    C1_b = struct.unpack('>Q', C1_a)[0] #13837628527553681883
    C1_c = bin(C1_b) #'0b1100000000001001001000011101010010110110101001100001100111011011'
    C1_d = str(C1_c)[2:len(C1_c)] #'1100000000001001001000011101010010110110101001100001100111011011'
    C1_e = C1_d.zfill(64)
    C2 = ""
    C2_a = struct.pack('>d', float(c2)) #b'\xc0\t!\xd4\xb6\xa6\x19\xdb'
    C2_b = struct.unpack('>Q', C2_a)[0] #13837628527553681883
    C2_c = bin(C2_b) #'0b1100000000001001001000011101010010110110101001100001100111011011'
    C2_d = str(C2_c)[2:len(C2_c)] #'1100000000001001001000011101010010110110101001100001100111011011'
    C2_e = C2_d.zfill(64)
    for i in range(8): #8回繰り返す
        pic8_1 = int(C1_e[8*i:8*i+8].zfill(8))#i文字目から8文字(8桁)取り出して右寄せ0埋め
        toHex_1 = hex(pic8_1)[2:len(hex(pic8_1))]#文字列pic8を16進数にする
        C1 = str(C1) + toHex_1 #取り出した8文字を16進数に変換して足す
        pic8_2 = int(C2_e[8*i:8*i+8].zfill(8))#i文字目から8文字(8桁)取り出して右寄せ0埋め
        toHex_2 = hex(pic8_2)[2:len(hex(pic8_2))]#文字列pic8を16進数にする
        C2 = str(C2) + toHex_2 #取り出した8文字を16進数に変換して足す
        i = i + 1
    c9 = c0 + "*" + c1 + "*" +time
    C9 = Fo[2:len(Fo)-1] + str(C1) + "2a" + str(C2) + "2a" + Time[2:len(Time)-1]
#rec:受信したことを伝える
elif c0 == "rec" or c0 == "rssi" or c0 == "come" or c0 == "rqps" or c0 == "done":
    c9 = c0 + "*" + time
    C9 = Fo[2:len(Fo)-1] + "2a" + Time[2:len(Time)-1]
elif c0 == "rqrs":
    c1 = input('何秒間で:')
    c2 = input('何回送る:')#c1秒間でc2回送信
    c9 = c0 + "*" + c2 + "*" + c1 + "*" + time
    C9 = Fo[2:len(Fo)-1] + "2a" + Time[2:len(Time)-1]
    
elif c0 == "err":
    c1 = input()
    C1 = str(binascii.hexlify(c1.encode()))
    c9 = c0 + "*" + c1 + "*" + time
    C9 = Fo[2:len(Fo)-1] + str(C1[2:len(C1)-1]) + "2a" + Time[2:len(Time)-1]
    
elif c0 == "remi":
    c9 = c0
    C9 = str(binascii.hexlify(c9.encode()))
    C9 = C9[2:len(C9)-1]
    print(C9)
    
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
  C9 = str(binascii.hexlify(c9.encode()))
  C9 = C9[2:len(C9)-1]
  print(C9)
#後半: ]*]len
la = "]*" + str(len(c9))
La = str(binascii.hexlify(la.encode()))

Cmd0 = "5b" + C9 + La[2:len(La)-1]
Cmd1 = Cmd0[2:len(Cmd0)-1]

#len2
num2 = int(len(Cmd1) /2)
len2 = hex(num2)[2:] # num2に格納された数字を16進数の文字列にして代入

#len1
num1 = int((len(middle) + len(len2) + len(Cmd1))/2)
len1 = hex(num1)[2:] # num1に格納された数字を16進数の文字列にして代入

command = first + len1 +  middle + len2 + Cmd1 + last
print(command)
