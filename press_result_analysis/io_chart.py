#! /usr/bin/python
from pychartdir import *

PALERED = 0xffdddd #pale red  
BLACK = 0x000000
WHITE = 0xffffff
GRAY = 0xcccccc
DARKRED = 0x880000

LINEWIDTH = 2  #线宽


class IOChart:
    def __init__(self, width, height, title = ""):
        self.width = width
        self.height = height
        self.chart_back_groud_clr = 0xeeeeff         #pale red
        self.chart_border_clr = 0x000000               #black
        self.title = title
        self.chart = None
        self.layer = None
        
    def new_data_chart(self):
        # 创建一个chart
        self.chart = XYChart(self.width, self.height, self.chart_back_groud_clr, self.chart_border_clr, 0)
        # self.chart.setRoundedFrame()

        # 设置画布在chart中的起始位置，以及大小
        self.chart.setPlotArea(80, 30, self.width - 160, self.height - 80, WHITE, -1, -1, GRAY, GRAY)

        # 添加一个图例
        self.chart.addLegend(80, 30, 0, "arialbd.ttf", 9).setBackground(Transparent)

        # 添加一个标题
        # self.chart.addTitle(self.title, "timesbi.ttf", 15).setBackground(0xccccff, 0x000000, glassEffect())
        self.chart.addTitle(self.title, "timesbi.ttf", 12)

        self.chart.setDefaultFonts("宋体")

    '''设置Y轴'''
    def set_y_axis(self, name = "", width = 1, left_or_right = 'left', color = 0x130c0e):
        self.chart.yAxis2().setTitle(name)

        yAxis_func = getattr(self.chart, 'yAxis') if left_or_right == 'left' \
            else getattr(self.chart, 'yAxis2')

        yAxis_func().setTitle(name, "黑体", 11)
        if width > 0:
            yAxis_func().setWidth(width)

        yAxis_func().setColors(0x130c0e, color, color)

    # 设置x轴
    def set_x_axis(self, xdata=[], xname="", xwidth=1):

        self.chart.xAxis().setLabels(xdata)
        self.chart.xAxis().setTitle(xname)
        if xwidth > 0:
            self.chart.xAxis().setWidth(xwidth)

    def add_layer(self, layer_type = "spline", width = 2, left_or_right = 'left'):
        layer = None
        if layer_type == "spline":
            layer = self.chart.addSplineLayer()     # 点线图
        elif layer_type == "line":
            layer = self.chart.addLineLayer2()     # 线图
        elif layer_type == "bar":
            layer = self.chart.addBarLayer()    # bar

        if layer_type.find('line') != -1:
            layer.setLineWidth(width)

        elif layer_type.find('bar') != -1:
            layer.setBarWidth(width)

        if left_or_right != 'left':
            layer.setUseYAxis2()

        return layer

    @staticmethod
    def add_data_set(layer, data_list, data_name, layer_clr, sytle=1):
        if sytle == 0:
            # layer.addDataSet(data_list, layer_clr, data_name).setDataSymbol(CircleSymbol, 5, layer_clr)
            layer.addDataSet(data_list, layer_clr).setDataSymbol(CircleShape, 9, layer_clr, layer_clr)
        elif sytle == 1:
            layer.addDataSet(data_list, layer_clr, data_name).setDataSymbol(DiamondSymbol, 5,  layer_clr)

        else:
            layer.addDataSet(data_list, layer_clr, data_name)

    def draw_data_chart(self, pic_nam_path):
        self.chart.makeChart(pic_nam_path)


# if __name__ == "__main__":
#     x_data = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
#     y_data0 = [10000, 8000, 7000, 6000, 5000, 4000, 2000, 1000, 500]
#     y_data1 = [8, 16, 18, 20, 25, 30, 35, 40, 50]
#
#     c = IOChart(800, 300, "ceph io test")
#     c.new_data_chart()
#     c.set_y_axis("IOPS", 1, 'left', 0x2a5caa)
#     c.set_y_axis("Latency", 1, 'right', 0xfcaf17)
#     c.set_x_axis(x_data, "time", 1)
#
#     #------------------
#     # latency_layer = c.add_layer('line', 2, 'right')
#     # latency_layer.addDataSet(y_data1, 0xfcaf17).setDataSymbol(CircleShape, 5, 0xfcaf17, 0xfcaf17)
#     #
#     #
#     # iops_layer = c.add_layer('bar', 20, 'left')
#     # iops_layer.addDataSet(y_data0, 0x2a5caa, 'iops')
#     #---------------------
#
#     latency_layer = c.add_layer('line', 2, 'right')
#     c.add_data_set(latency_layer, y_data1, "test2", 0xfcaf17)
#
#     iops_layer = c.add_layer('bar', 20, 'left')
#     c.add_data_set(iops_layer, y_data0, "test1", 0x2a5caa, 0)
#
#     # 注意当点线和柱状有重合是，请先画线，否则重合的部分将被遮盖
#     #
#
#     #
#     # # iops_layer.setUseYAxis2()
#     #
#     # # latency_layer.setUseYAxis2()
#     #
#     # # iops_layer.setBarWidth(20)
#
#     c.draw_data_chart("ceph_io.png")