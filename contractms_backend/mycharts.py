from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

def drawTable(maintitle:str,subtitle:str,colname:list,row:list) -> Table:
    # 希望实现得功能：
    # 传入参数，返回一个table
    table = Table()
    tableHeader = colname
    tableRow = row
    tableTitle = maintitle
    tableSubTitle = subtitle
    table.add(tableHeader,tableRow)
    if tableSubTitle != '':
        table.set_global_opts(
            title_opts=ComponentTitleOpts(title=tableTitle,subtitle=tableSubTitle)
        )
    else:
        table.set_global_opts(
            title_opts=ComponentTitleOpts(title=tableTitle)
        )
    return table