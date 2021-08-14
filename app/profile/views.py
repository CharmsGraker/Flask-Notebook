from flask import render_template
from . import profile


class Intro:
    def __init__(self):
        self.title = ''
        self.body = ''


@profile.route('/')
def my_document():
    allgrades = {'数据结构': 88, '离散数学A': 95, '常微分方程': 92,'计算方法': 92, \
                 '数学分析A3': 80, '高等代数（下）': 96}
    subjects = allgrades.keys()
    make_up_courses_5 = [
        ['信号处理基础', 2],
        ['数字电路与逻辑设计实验A', 2],
        ['数字电路与逻辑设计', 3.5],
        ['计算机组织与架构', 3.5],
        ['智能游戏开发与设计', 2]]
    make_up_courses_6 = [
        ['C语言程序设计(下)', 2],
        ['计算机网络A', 4],
        ['软件工程A', 2.5],
        ['大数据分析与处理', 2]
    ]
    return render_template('my_document.html', allgrades=allgrades, make_up_courses_5=make_up_courses_5,\
                           make_up_courses_6=make_up_courses_6)


@profile.route('/coding')
def coding():
    return render_template('coding.html')


@profile.route('/make_up_course', methods=['GET'])
def make_up_course():
    make_up_courses_5 =[
        ['信号处理基础', 2],
        ['数字电路与逻辑设计实验A',2],
        ['数字电路与逻辑设计',3.5],
        ['计算机组织与架构',3.5],
        ['智能游戏开发与设计',2]]
    make_up_courses_6 = [
        ['C语言程序设计(下)',2],
        ['计算机网络A',4],
        ['软件工程A',2.5],
        ['大数据分析与处理',2]
    ]
    return render_template('make_up.html',\
                           make_up_courses_5=make_up_courses_5,\
                           make_up_courses_6=make_up_courses_6)
