# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import sys
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import cx_Oracle
import sqlalchemy
from dateutil.relativedelta import *

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
enginex = sqlalchemy.create_engine(
    'oracle://xiaohu:82626296@192.168.201.77:1521/?service_name=pdborcl')
rs = enginex.execute('select uuid,name from organization1')
hospital_table = rs.fetchall()


def get_hospital_id(hospital_str):
    print('hospital_str: %s' % hospital_str)
    for item in hospital_table:
        if item[1] in hospital_str:
            return item[0]
    return 0


now_date = datetime.datetime.now()
last_month = (now_date - relativedelta(months=1)).strftime("%Y%m")
working_month = last_month
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
""".split())
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
sql_columns = """hospital_id
reporting_month
healthy_card_issued
smart_consumption_times
smart_consumption_amount
counter_recharge_times
counter_recharge_amount
machine_recharge_times
machine_recharge_amount
""".split()


def to_sql(month = last_month):
    working_month = month
    os.chdir(
    "E:/sync360/documents/VVV项目方案VVV/智慧医疗诊间结算/统计数据/{}".format(working_month))

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
    df3 = pd.merge(srx, df3, on='医院名称', how='outer')
    df3 = df3.loc[:, sorted_columns]

    # prepare for sql insert
    df3.insert(loc=1, column='reporting_month', value=working_month)
    df3.columns = sql_columns
    df3.loc[:, 'hospital_id'] = df3.loc[:, 'hospital_id'].apply(get_hospital_id)

    print(df3)

    sql_values = []
    for s in sql_columns:
        sql_values.append(':' + s)
    insert_sql = '''insert into 
                    smk_statistic(hospital_id,reporting_month,healthy_card_issued,smart_consumption_times,smart_consumption_amount,counter_recharge_times,counter_recharge_amount,machine_recharge_times,machine_recharge_amount) 
                    values (:hospital_id,to_date(:reporting_month, '%Y%m'),:healthy_card_issued,:smart_consumption_times,:smart_consumption_amount,:counter_recharge_times,:counter_recharge_amount,:machine_recharge_times,:machine_recharge_amount)'''
    con = enginex.connect()
    for row in df3.itertuples(index=False):
        con.execute(sqlalchemy.text(insert_sql), row._asdict())
        print(row)
    con.close()

def print_usage():
    print("usage: statistic_to_sql %Y%m or statistic_to_sql %Y%m-%Y%m")

def add_months(dt,months): 
    #返回dt隔months个月后的日期，months相当于步长 
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

def getBetweenMonth(begin_month, end_month):  
    month_list = []
    begin_month = datetime.datetime.strptime(begin_month, "%Y%m")
    end_month = datetime.datetime.strptime(end_month, "%Y%m")
    while begin_month <= end_month:
        date_str = begin_month.strftime("%Y%m")
        month_list.append(date_str)
        begin_month = add_months(begin_month, 1)
    return month_list



if __name__ == '__main__':
    months = []
    if len(sys.argv) == 2:
        re_obj = re.fullmatch(r'(?P<month1>20[0-9]{2}(0[1-9]|1[012]))-(?P<month2>20[0-9]{2}(0[1-9]|1[012]))', sys.argv[1])
        if re_obj != None:
            try:
                months = getBetweenMonth(re_obj.group('month1'), re_obj.group('month2'))
            except ValueError as e:
                print(e)
                print_usage()
        elif re.fullmatch(r'20[0-9]{2}(0[1-9]|1[012])', sys.argv[1]) != None:
            try:
                mx = datetime.datetime.strptime(date_string=sys.argv[1], format="%Y%m")
                months.append(mx)
            except ValueError as e:
                print(e)
                print_usage()
    else:
        print_usage()
    for m in months:
        to_sql(m)



#df3.to_sql('smk_statistic1', engine, if_exists='append', index=False)

#df3.to_excel('汇总智慧医疗{}.xls'.format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")), na_rep=0)

#engine = sqlalchemy.create_engine('sqlite:///foo.db')
#engine = sqlalchemy.create_engine('oracle://xiaohu:82626296@192.168.201.77:1521/?service_name=pdborcl')

#df3.to_sql('test', engine)
