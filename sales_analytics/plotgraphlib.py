import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

GDS = {'VAR'  : {'1_Var'     : {'Group By Name': ['ITEM_NAME']},
                 '2_Var_1'   : {'Group By Name': ['ITEM_NAME', 'SR_CODE'],
                                'Search': ['SR_CODE']},
                 '2_Var_2'   : {'Group By Name': ['ITEM_NAME', 'INV_QUARTER'],
                                'Search': ['INV_QUARTER']},
                 '2_Var_3'   : {'Group By Name': ['ITEM_NAME', 'INV_MONTH'],
                                'Search': ['INV_MONTH']},
                 '2_Var_4'   : {'Group By Name': ['ITEM_NAME', 'INV_WEEK_DAY'],
                                'Search': ['INV_WEEK_DAY']},
                 '3_Var_1'   : {'Group By Name': ['ITEM_NAME', 'SR_CODE', 'INV_QUARTER'],
                                'Search': ['SR_CODE', 'INV_QUARTER']},
                 '3_Var_2'   : {'Group By Name': ['ITEM_NAME', 'SR_CODE', 'INV_MONTH'],
                                'Search': ['SR_CODE', 'INV_MONTH']},
                 '3_Var_3'   : {'Group By Name': ['ITEM_NAME', 'SR_CODE', 'INV_WEEK_DAY'],
                                'Search': ['SR_CODE', 'INV_WEEK_DAY']},
                 '4_Var_1'   : {'Group By Name': ['ITEM_NAME', 'INV_NO'],
                                'Search': ['ITEM_NAME']},
                 '4_Var_2'   : {'Group By Name': ['CUSTOMER', 'INV_NO'],
                                'Search': ['CUSTOMER']}
                },
       'QTY'  : {'X_Label'   : 'PRODUCT QUANTITY (pcs.)',
                 'Title'     : 'TOP ?? QUANTITY OF PRODUCT SALES',
                 'SUM_Value' : 'QTY',
                 'Sample'    : 20,
                 'Y_Label'   : 'PRODUCT SELLING'
                },
       'VALUE': {'X_Label'   : 'PRODUCT PRICE (Million Baht)',
                 'Title'     : 'TOP ?? VALUE OF PRODUCT SALES',
                 'SUM_Value' : 'PRICE',
                 'Sample'    : 20,
                 'Y_Label'   : 'PRODUCT SELLING'
                },
       'CPROD': {'X_Label'   : 'COUNT OF PRODUCT SELLING',
                 'Title'     : 'TOP ?? THE MOST OFTEN PRODUCT BUYING BY CUSTOMER',
                 'SUM_Value' : 'COUNT',
                 'Sample'    : 20,
                 'Y_Label'   : 'PRODUCT SELLING'
                },
       'CCUST': {'X_Label'   : 'COUNT OF CUSTOMER BUYING',
                 'Title'     : 'TOP ?? THE MOST OFTEN CUSTOMER BUYING',
                 'SUM_Value' : 'COUNT',
                 'Sample'    : 20,
                 'Y_Label'   : 'CUSTOMER BUYING'
                }
      }

graph_path = 'GRAPH/'

def plotgraph(varno, gds, df_test, i=None, j=None):
    #avg = df100[gds[varno[0]]['SUM_Value']].quantile(q=0.90)
    plt.figure(figsize=(20, gds[varno[0]]['Sample'] / 2))
    chart = sb.barplot(data=df_test,
                       y=gds['VAR'][varno[1]]['Group By Name'][0],
                       x=gds[varno[0]]['SUM_Value'])
    #plt.axvline(x=avg, linestyle='--', color='deepskyblue') # Plot Quantile 90% Line from All Data
    chart.set_yticklabels(chart.get_yticklabels(), fontdict={'fontsize': 18, 'fontweight': 'bold'});
    chart.tick_params(labelsize=18)
    plt.ylabel(gds[varno[0]]['Y_Label'], fontdict={'fontsize': 24, 'fontweight': 'bold'})
    plt.xlabel(gds[varno[0]]['X_Label'], fontdict={'fontsize': 24, 'fontweight': 'bold'})
    plt.title(gds[varno[0]]['Title'], fontdict={'fontsize': 28, 'fontweight': 'bold'})
    plt.tight_layout()
    if str(varno[1])[0:5] == '1_Var':
        plt.savefig(f'{graph_path}{str(varno[0]).lower()}_top20_2019.png', dpi=150)
    elif str(varno[1])[0:5] == '2_Var':
        plt.savefig(f'{graph_path}{str(varno[2][i][0]).lower().replace(" ", "_")}_{str(varno[0]).lower()}_top20_2019.png', dpi=150)
    elif str(varno[1])[0:5] == '3_Var':
        plt.savefig(f'{graph_path}{str(varno[2][0][i][0]).lower().replace(" ", "_")}_{str(varno[2][1][j][0]).lower().replace(" ", "_")}_{str(varno[0]).lower()}_top20_2019.png', dpi=150)
    elif str(varno[1])[0:5] == '4_Var':
        plt.savefig(f'{graph_path}{str(varno[0]).lower()}_top20_2019.png', dpi=150)
    plt.show()

def varplotgraph(df, varno, gds):
    gds['QTY']['Title'] = str('TOP ?? QUANTITY OF PRODUCT SALES').replace('??', str(gds[varno[0]]['Sample']))
    gds['VALUE']['Title'] = str('TOP ?? VALUE OF PRODUCT SALES').replace('??', str(gds[varno[0]]['Sample']))
    gds['CPROD']['Title'] = str('TOP ?? THE MOST OFTEN PRODUCT BUYING BY CUSTOMER').replace('??', str(gds[varno[0]]['Sample']))
    gds['CCUST']['Title'] = str('TOP ?? THE MOST OFTEN CUSTOMER BUYING').replace('??', str(gds[varno[0]]['Sample']))

    if varno[1] == '1_Var':
        graph_title = gds[varno[0]]['Title']
        df_test = df[df.SELL_TYPE == 'PRODUCT'].groupby(gds['VAR'][varno[1]]['Group By Name'])[gds[varno[0]]['SUM_Value']].sum().to_frame().reset_index()
        df_test = pd.DataFrame(df_test.
                               sort_values(by=[gds[varno[0]]['SUM_Value']], ascending=False).
                               head(gds[varno[0]]['Sample']))
        gds[varno[0]]['Title'] = graph_title
        plotgraph(varno, gds, df_test)
        return df_test
    elif str(varno[1])[0:5] == '2_Var':
        df_test = []
        graph_title = gds[varno[0]]['Title']
        for i, vn in enumerate(varno[2]):
            df_temp = df[df.SELL_TYPE == 'PRODUCT'].groupby(gds['VAR'][varno[1]]['Group By Name'])[gds[varno[0]]['SUM_Value']].sum().to_frame().reset_index()
            df_temp = df_temp[df_temp[gds['VAR'][varno[1]]['Search'][0]] == vn[1]].sort_values(by=[gds[varno[0]]['SUM_Value']], ascending=False).head(gds[varno[0]]['Sample'])
            df_test.append(pd.DataFrame(df_temp)) # For Sample Setting in gds
            gds[varno[0]]['Title'] = graph_title + ' BY ' + varno[3] + varno[2][i][0]
            plotgraph(varno, gds, df_temp, i)
        return df_test
    elif str(varno[1])[0:5] == '3_Var':
        df_test = []
        start_title = gds[varno[0]]['Title']
        for i, vn1 in enumerate(varno[2][0]):
            df_test2 = []
            for j, vn2 in enumerate(varno[2][1]):
                graph_title = start_title
                df_temp = df[df.SELL_TYPE == 'PRODUCT'].groupby(gds['VAR'][varno[1]]['Group By Name'])[gds[varno[0]]['SUM_Value']].sum().to_frame().reset_index()
                df_test2.append(pd.DataFrame(df_temp[(df_temp[gds['VAR'][varno[1]]['Search'][0]] == vn1[1]) &
                                                     (df_temp[gds['VAR'][varno[1]]['Search'][1]] == vn2[1])].
                                             sort_values(by=[gds[varno[0]]['SUM_Value']], ascending=False).
                                             head(gds[varno[0]]['Sample']))) # For Sample Settng in gds
                gds[varno[0]]['Title'] = graph_title + ' BY ' + varno[3] + varno[2][0][i][0] + ' IN ' + varno[2][1][j][0]
                plotgraph(varno, gds, df_test2[j], i, j)
            df_test.append(df_test2)
        return df_test
    elif str(varno[1])[0:5] == '4_Var':
        df_test = pd.DataFrame(df[df.SELL_TYPE == 'PRODUCT'].groupby(gds['VAR'][varno[1]]['Group By Name'])[gds['VAR'][varno[1]]['Search'][0]].count())
        df_test.rename(columns={gds['VAR'][varno[1]]['Search'][0]: 'COUNT'}, inplace=True)
        df_test.reset_index(gds['VAR'][varno[1]]['Group By Name'], inplace=True)
        df_test = pd.DataFrame(df_test[gds['VAR'][varno[1]]['Search'][0]].value_counts()).reset_index()
        df_test.rename(columns={'index': gds['VAR'][varno[1]]['Search'][0], gds['VAR'][varno[1]]['Search'][0]: 'COUNT'}, inplace=True)
        df_test = df_test.head(gds[varno[0]]['Sample'])
        plotgraph(varno, gds, df_test)
        return df_test