# -*- coding: utf-8 -*-
import os
import xlwt
import time


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font
    return style


def write_excel(data):
    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet
    data_sheet = workbook.add_sheet('data')
    row0 = [u'景区', u'热度', u'地区', u'价格', u'销量']
    # 生成第一行和第二行
    for i in range(len(row0)):
        data_sheet.write(0, i, row0[i], set_style(
            'Microsoft YaHei UI Light', 220, True))
    for item in range(len(data)):
        for i in range(len(row0)):
            data_sheet.write(
                item+1, i, data[item][i], set_style('Microsoft YaHei UI Light', 220))

    # 保存文件
    workbook.save('excel/data4.xls')


if __name__ == '__main__':
    print('创建data.xls文件成功')
