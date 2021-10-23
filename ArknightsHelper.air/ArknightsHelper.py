# -*- encoding=utf8 -*-
__author__ = "Elysium"

from random import random
from airtest.core.api import *

auto_setup(__file__)

TIMEOUT = 300  # 普通找图5分钟超时
TIMEOUT_OFFSET = 600  # 关卡结算超时时间= TIMEOUT + TIMEOUTOFFSET 默认300+600秒（15分钟）
AUTO_SANITY = 300  # 自动用药回复体力上限, 小于60即不自动用药恢复
TIMES = 4  # 重复关卡次数，可以设置得很大，就可以用上面体力规定的值去限制耍关卡的次数

# 重复刷关：先选中关卡后运行
def repeater(times: int, auto_sanity: int):
    if times <= 0:
        return
    try:
        duration = 0.3
        sleep(1)
        start = wait(Template(r"tpl1635010723221.png", record_pos=(0.391, 0.229), resolution=(1920, 1080)),
                     timeout=TIMEOUT, intervalfunc=print("未选中"), interval=1)

        prts_false = exists(Template(r"tpl1635010573996.png", record_pos=(0.393, 0.182), resolution=(1920, 1080)))

        prts_true = exists(Template(r"tpl1635010657060.png", record_pos=(0.394, 0.182), resolution=(1920, 1080)))
        if prts_true is False and prts_false is not False:
            touch(prts_false)
        touch(start, duration=duration + random())
        sleep(1)
        # todo: 理智自动恢复
        try:
            med_sanity = wait(Template(r"tpl1635010988367.png", record_pos=(0.197, 0.115), resolution=(1920, 1080)),
                              timeout=5)
            if auto_sanity >= 0 and med_sanity is not False:
                
                med_60_text_pic = exists(
                    Template(r"tpl1635011004143.png", record_pos=(0.314, 0.115), resolution=(1920, 1080)))

                if med_60_text_pic is not False:
                    auto_sanity -= 60

                
                med_100_text_pic = exists(
                    Template(r"tpl1635011015354.png", record_pos=(0.316, 0.116), resolution=(1920, 1080)))

                if med_100_text_pic is not False:
                    auto_sanity -= 100

                if auto_sanity < 0:
                    log("AUTO SANITY: 已达到最大自动恢复值，停止" + str(auto_sanity))
                    touch(Template(r"tpl1635011028099.png", record_pos=(0.108, 0.17), resolution=(1920, 1080)),
                          duration=duration)
                    return
                else:
                    touch(Template(r"tpl1635011037397.png", record_pos=(0.351, 0.169), resolution=(1920, 1080)),
                          duration=duration)
        except TargetNotFoundError:
            log("AUTO SANITY: 理智尚足")

        sleep(1)
        start_op = wait(Template(r"tpl1635010684175.png", record_pos=(0.361, 0.112), resolution=(1920, 1080)),
                        timeout=TIMEOUT, interval=1)
        touch(start_op, duration=duration + random())
        sleep(10)

        op_finished = wait(Template(r"tpl1635010927096.png", record_pos=(0.234, 0.096), resolution=(1920, 1080)),
                           timeout=TIMEOUT + TIMEOUT_OFFSET, interval=5)
        sleep(2)
        touch((380 + random() * 50, 955 + random() * 50), duration=duration + random())

        start = exists(Template(r"tpl1635010723221.png", record_pos=(0.391, 0.229), resolution=(1920, 1080)))

        while start is False:
            op_finished = exists(Template(r"tpl1635010927096.png", record_pos=(0.234, 0.096), resolution=(1920, 1080)))
            if op_finished is not False:
                touch((380 + random() * 50, 955 + random() * 50), duration=duration + random())
            sleep(1)
            start = exists(Template(r"tpl1635010723221.png", record_pos=(0.391, 0.229), resolution=(1920, 1080)))

    except TargetNotFoundError:
        print("Start timeout")
    times = times - 1
    repeater(times, auto_sanity)


repeater(TIMES, AUTO_SANITY)
