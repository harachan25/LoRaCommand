import binascii
import struct
import sys

i = 0

f_max = sys.float_info.max
f0 = -3.141519
#f1 = struct.unpack('>Q', struct.pack('>d', f_max))[0] # 9218868437227405311 struct.pack()でfloatをバイト列bytesに変換，第二引数の値を64bitビッグエンディアンの浮動小数点数としてバイト列に変換
#f2 = hex(struct.unpack('>Q', struct.pack('>d', f_max))[0]) # 0x7fefffffffffffff f1を16進数にしたもの
#f3 = f2[2:len(f2)+1] # 7fefffffffffffff
C1_1 = struct.pack('>d', f0) #b'\xc0\t!\xd4\xb6\xa6\x19\xdb'
C1_2 = struct.unpack('>Q', C1_1)[0] #13837628527553681883
C1_3 = bin(C1_2) #'0b1100000000001001001000011101010010110110101001100001100111011011'
C1_4 = str(C1_3)[2:len(C1_3)] #'1100000000001001001000011101010010110110101001100001100111011011'

print(f0)
print(C1_1)
print(C1_2)
print(C1_3)
print(C1_4)
