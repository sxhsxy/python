# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import cx_Oracle
import sqlalchemy
from dateutil.relativedelta import *


now_date = datetime.datetime.now()
last_month = (now_date - relativedelta(months=1))
working_dir = last_month.strftime("%Y%m")
sr = pd.Series("""杭州市萧山区第一人民医院
杭州市萧山区第二人民医院
杭州市萧山区第三人民医院
杭州市萧山区中医院
杭州市萧山区中医骨伤科医院
杭州市萧山区皮肤病医院
浙江萧山医院
萧山区计划生育宣传技术指导站
杭州市萧山区瓜沥镇社区卫生服务中心
杭州市萧山区河上镇社区卫生服务中心
""".split()
)
srx = pd.DataFrame(sr, columns=['医院名称'])
sorted_columns = """医院名称	
健康卡发卡数	
市民卡智慧结算交易数（次）	
市民卡智慧结算交易金额（元）	
窗口充值数（次）	
窗口充值金额（元）	
自助机充值数（次）	
自助机充值金额（元）
""".split()

os.chdir("E:/sync360/documents/VVV项目方案VVV/智慧医疗诊间结算/统计数据/{}".format(working_dir))

#智慧医疗窗口数据
df = pd.read_excel("市民卡智慧医疗业务量报表.xlsx", parse_cols='A,J,O')
df.columns = '医院名称 窗口充值数（次） 窗口充值金额（元）'.split()
df = df[df.iloc[:, 0].str.contains('萧山').fillna(value=False)]

#智慧医疗自助机数据
df2 = pd.read_excel('市民卡智慧医疗自助服务报表.xlsx', parse_cols='A,E,K,P,AK,AP')
df2.columns = '医院名称 健康卡发卡数 自助机充值数（次） 自助机充值金额（元） \
                市民卡智慧结算交易数（次）	市民卡智慧结算交易金额（元）'.split()
df2 = df2[df2.iloc[:, 0].str.contains('萧山').fillna(value=False)]

df3 = pd.merge(df, df2, how='outer', on='医院名称')
df3 = pd.merge(srx, df3, on='医院名称')
df3 = df3.loc[:, sorted_columns]
df3.to_excel('汇总智慧医疗{}.xls'.format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")), na_rep=0)

engine = sqlalchemy.create_engine('sqlite:///foo.db')
#df3.to_sql('test', engine)

