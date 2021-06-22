import os

import xlrd
from poium.common import logging

from webtest.aw.CONSTANT import CONSTANT


def get_xls_list(file_path=''):
    file_lists = []
    import os
    res = os.path.join(CONSTANT.RES_PATH)
    logging.info(res)
    files = os.walk(file_path)
    for root, dirs, files in files:
        for f in files:
            if r'~$' not in f:
                file_lists.append(os.path.join(root, f))
    # print(len(file_lists))
    return file_lists


class excel(object):
    def __init__(self, filename=''):
        '''
        Constructor
        '''
        if CONSTANT.RES_PATH in filename:
            self.file = filename
        else:
            self.file = os.path.join(CONSTANT.RES_PATH, filename)
        logging.info("==================================正在打开的表格名称：%s===============================" % self.file)
        self.rb = xlrd.open_workbook(filename=self.file)

    def get_sheets(self):
        """
        获取表格的所有sheets页
        :return:sheet页列表
        """
        sheet_names = self.rb.sheet_names()
        logging.info("表格的sheet页： %s" % sheet_names)
        return sheet_names

    def get_lines(self, sheet_name):
        """
        读取表格指定sheet页的所有行,并对合并行的值进行补充
        :param sheet_name:sheet页名称
        :return:所有行列表，合并单元格默认等于同一列的第一格数据
        """
        lines = []
        rows = self.rb.sheet_by_name(sheet_name).nrows
        cols = self.rb.sheet_by_name(sheet_name).ncols
        # logging.info("%s sheet页有 %s 行， %s 列" % (sheet_name, rows, cols))
        # logging.info("未经处理的行信息如下：")
        for i in range(rows):
            line = self.rb.sheet_by_name(sheet_name).row_values(rowx=i, start_colx=0, end_colx=cols)
            # logging.info(line)
            lines.append(line)
        sheet = self.rb.sheet_by_name(sheet_name)
        # 合并单元格的值统一等于第一行的值
        merged_cells = sheet.merged_cells
        # print(merged_cells)
        for m in merged_cells:
            for i in range(m[0], m[1]):  # 合并单元格的起始行和结束行
                for j in range(m[2], m[3]):  # 合并单元格的起始列和起始列
                    # print(i,j,m[0], m[2])
                    lines[i][j] = sheet.cell(m[0], m[2]).value
        # logging.info("处理之后的行信息如下：")
        logging.info("表格sheet页 ‘%s’ 的数据如下：" % sheet_name)
        for l in lines:
            logging.info(l)
        return lines[1:]

    def get_cols(self, sheet_name):
        """
        读取表格指定sheet页的所有列
        :param sheet_name:sheet页名称
        :return:所有行列表，合并单元格默认等于同一列的第一格数据
        """
        rows_v = []
        rows = self.rb.sheet_by_name(sheet_name).nrows
        cols = self.rb.sheet_by_name(sheet_name).ncols
        # logging.info("%s sheet页有 %s 行， %s 列" % (sheet_name, rows, cols))
        # logging.info("未经处理的行信息如下：")
        for i in range(cols):
            col = self.rb.sheet_by_name(sheet_name).col_values(colx=i, start_rowx=0, end_rowx=rows)
            rows_v.append(col)
        sheet = self.rb.sheet_by_name(sheet_name)
        merged_cells = sheet.merged_cells
        print(merged_cells)
        for m in merged_cells:
            for i in range(m[2], m[3]):  # 合并单元格的起始列和结束列
                for j in range(m[0], m[1]):  # 合并单元格的起始行和起始行
                    # print(i,j,m[0], m[2])
                    rows_v[i][j] = sheet.cell(m[0], m[2]).value
        # logging.info("处理之后的行信息如下：")
        for l in rows_v:
            logging.info(l)
        logging.info("***********sheet页 ‘%s’ 读取列数结束 **********************" % sheet_name)
        return rows_v

    def close(self):
        self.rb.release_resources()
        logging.info("==================================此表格全部添加完成，正在关闭表格：%s===============================" % self.file)
