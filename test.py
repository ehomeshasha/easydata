#-*- encoding: gb2312 -*-
import codecs, sys

print '-'*60
# ����gb2312������
look  = codecs.lookup("gb2312")
# ����utf-8������
look2 = codecs.lookup("utf-8")

a = "�Ұ������찲��"

print len(a), a
# ��a����Ϊ�ڲ���unicode, ��Ϊʲô������Ϊdecode�أ��ҵ�����ǰ�gb2312���ַ�������Ϊunicode
b = look.decode(a)
# ���ص�b[0]�����ݣ�b[1]�ǳ��ȣ����ʱ���������unicode��
print b[1], b[0], type(b[0])
# ���ڲ������unicodeת��Ϊgb2312������ַ�����encode�����᷵��һ���ַ�������
b2 = look.encode(b[0])
# ���ֲ�һ���ĵط��˰ɣ�ת������֮���ַ���������14��Ϊ��7! ���ڵķ��صĳ��Ȳ���������������ԭ�������ֽ���
print b2[1], b2[0], type(b2[0])
# ��Ȼ���淵������������������ζ����len��b2[0]�ĳ��Ⱦ���7�ˣ���Ȼ����14��������codecs.encode��ͳ������
print len(b2[0])