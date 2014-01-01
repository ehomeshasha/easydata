#-*- encoding: gb2312 -*-
import codecs, sys

print '-'*60
# 创建gb2312编码器
look  = codecs.lookup("gb2312")
# 创建utf-8编码器
look2 = codecs.lookup("utf-8")

a = "我爱北京天安门"

print len(a), a
# 把a编码为内部的unicode, 但为什么方法名为decode呢，我的理解是把gb2312的字符串解码为unicode
b = look.decode(a)
# 返回的b[0]是数据，b[1]是长度，这个时候的类型是unicode了
print b[1], b[0], type(b[0])
# 把内部编码的unicode转换为gb2312编码的字符串，encode方法会返回一个字符串类型
b2 = look.encode(b[0])
# 发现不一样的地方了吧？转换回来之后，字符串长度由14变为了7! 现在的返回的长度才是真正的字数，原来的是字节数
print b2[1], b2[0], type(b2[0])
# 虽然上面返回了字数，但并不意味着用len求b2[0]的长度就是7了，仍然还是14，仅仅是codecs.encode会统计字数
print len(b2[0])