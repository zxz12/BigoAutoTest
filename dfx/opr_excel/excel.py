# _*_coding:utf-8 _*_
'''
Created on 2021年3月18日

@author: 011305
'''

import os

import xlrd, xlwt
from xlutils.copy import copy

from dfx.CONSTANT import CONSTANT
from dfx.logger.logging import log


def get_file_list(file_path=''):
    '''
    * @Title: get_xls_list
    * @Description:从指定的文件夹下遍历文件
    * @parameter:
    * @author: 011305
    * @date 2021年3月24日 下午5:27:21
    '''
    file_lists=[]
    import os
    file_path=CONSTANT.RES_PATH
    files=os.walk(file_path)
    for root, dirs, files in files:
        for f in files:
            if r'~$' not in f:
                file_lists.append(os.path.join(root, f))
    # print(len(file_lists))
    return file_lists


class read_excel(object):

    def __init__(self, filename=''):
        '''
        Constructor
        '''
        if CONSTANT.RES_PATH in filename:
            self.file=filename
        else:
            self.file=os.path.join(CONSTANT.RES_PATH, filename)
        log.info("==========正在打开的表格名称：%s============"%self.file)
        self.rb=xlrd.open_workbook(filename=self.file)

    def get_sheets(self):
        """
                        获取表格的所有sheets页
        :return:sheet页列表
        """
        sheet_names=self.rb.sheet_names()
        log.info("表格的sheet页： %s"%sheet_names)
        return sheet_names
    
    def get_sheet(self, sheet):
        if isinstance(sheet, int):
            sht=self.rb.sheet_by_index(sheet)
        elif isinstance(sheet, str):
            sht=self.rb.sheet_by_name(sheet)
        else:
            raise TypeError("参数类型错误")
        return sht

    def get_lines(self, sheet):
        """
                        读取表格指定sheet页的所有行
        :param sheet_name:sheet页名称
        :return:所有行列表，合并单元格默认等于同一列的第一格数据
        """
        lines=[]
        sht=self.get_sheet(sheet)
        rows=sht.nrows
        cols=sht.ncols
        for i in range(rows):
            line=sht.row_values(rowx=i, start_colx=0, end_colx=cols)
            lines.append(line)
        log.info("表格sheet页 ‘%s’ 的数据如下："%sheet)
        for l in lines:
            log.info(l)
        return lines
    
    def get_cols(self, sheet):
        """
                        读取表格指定sheet页的所有列
        :param sheet_name:sheet页名称
        :return:所有行列表，合并单元格默认等于同一列的第一格数据
        """
        colus=[]
        sht=self.get_sheet(sheet)
        rows=sht.nrows
        cols=sht.ncols
        for i in range(cols):
            col=sht.col_values(colx=i, start_rowx=0, end_rowx=rows)
            colus.append(col)
        log.info("表格sheet页 ‘%s’ 的数据如下："%sheet)
        for c in colus:
            log.info(c)
        return colus
    
    def close(self):
        self.rb.release_resources()
        log.info("=========正在关闭表格：%s=========="%self.file)


class write_excel:

    def __init__(self, filename):
        if filename:
            if CONSTANT.RES_PATH in filename:
                self.file=filename
            else:
                self.file=os.path.join(CONSTANT.RES_PATH, filename)
            log.info("===========正在打开的表格名称：%s================"%self.file)
            rb=xlrd.open_workbook(filename=self.file)
            self.wb=copy(rb)
            
        else:
            log.info("新建表格")
            self.wb=xlwt.Workbook()
            
    def get_one_sheet(self, sheet):
        sht=self.wb.get_sheet(sheet)
        return sht
        
    def write_value(self, sheet, i, j, value):
        sheet=self.wb.get_sheet(sheet)
        sheet.write(i, j, value)
        
    def save_wxcel(self, filename):
        self.wb.save(filename)
