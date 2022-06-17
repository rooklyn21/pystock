import akshare as ak

stock_hsgt_north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")

stock_em_hsgt_north_cash_df = ak.stock_hsgt_north_cash_em(symbol="北上")

stock_hsgt_north_acc_flow_in_em_df = ak.stock_hsgt_north_acc_flow_in_em(symbol="北上")
print('北向净流入',stock_hsgt_north_net_flow_in_em_df)
# print('北向资金余额',stock_em_hsgt_north_cash_df)
# print('北向累计净流入',stock_hsgt_north_acc_flow_in_em_df)
for one in stock_hsgt_north_net_flow_in_em_df.values:
    # print(one[1])

    if one[1]<0:
        print(one)
"""遍历每一个交易日，对北上进行分析"""
signal = '无信号'
for index, row in stock_hsgt_north_net_flow_in_em_df.iterrows():
    # print(index)
    # print(row)
    if index<252:
        continue
    df_data_temp = stock_hsgt_north_net_flow_in_em_df.iloc[index-252:index]
    # 计算近 252 天的平均数和标准差
    average = df_data_temp['value'].sum()/252
    std = df_data_temp['value'].std()
    # 计算上下限
    up_line = float(format(average + std * 1.5, '.4f'))
    down_line = float(format(average - std * 1.5, '.4f'))
    # 判断并输出
    if row['value'] >= up_line:
        signal = '看多'
        print('{0}:<{1}> 北上净流入:{2}亿元，看多线:{3}亿元, 看空线:{4}亿元'.format(row['date'], signal, format(row['value'], '.4f'),
                                                                  up_line, down_line))
    elif row['value'] <= down_line:
        signal = '看空'
        print('{0}:<{1}> 北上净流入:{2}亿元，看多线:{3}亿元, 看空线:{4}亿元'.format(row['date'], signal, format(row['value'], '.4f'),
                                                                  up_line, down_line))

    if index == stock_hsgt_north_net_flow_in_em_df.shape[0] - 1:
        print('\n最新数据\n{0}: <{1}> \n北上净流入:{2}亿元，看多线:{3}亿元, 看空线:{4}亿元\n'.format(row['date'], signal,
                                                                               format(row['value'], '.4f'), up_line,
                                                                               down_line))