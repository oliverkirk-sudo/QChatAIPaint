import base64
import os.path
import random

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
from plugins.aipaint.config.config import default_config
from plugins.aipaint.pkg.holara import gen_img
from mirai import Image


def response_process(images, remain, generation_cost):
    msg_list = []
    img_obj = [Image(base64=i.replace('\n', '')) for i in images]
    msg_list += img_obj
    msg_list.append('剩余积分：{}\n'.format(remain))
    msg_list.append('使用成本：{}'.format(generation_cost))
    return msg_list


def default_random_gen():
    return gen_img(True,
                   '',
                   default_config['negative_prompt'],
                   default_config['model'],
                   default_config['width'],
                   default_config['height'],
                   default_config['steps'],
                   default_config['cfg_scale'],
                   default_config['strength'],
                   str(random.randint(10 ** 8, 10 ** 10 - 1)),
                   default_config['history'],
                   default_config['random_autogen'],
                   default_config['variations_autogen'],
                   default_config['quality_tags'],
                   default_config['num_images'],
                   '',
                   default_config['skip'],
                   default_config['continuous_mode'])


def condition_random_gen(con_list):
    return gen_img(True,
                   '',
                   default_config['negative_prompt'],
                   con_list[0],
                   con_list[1] if default_config['user_resize'] else default_config['width'],
                   con_list[2] if default_config['user_resize'] else default_config['height'],
                   con_list[3],
                   con_list[4],
                   default_config['strength'],
                   str(random.randint(10 ** 8, 10 ** 10 - 1)),
                   default_config['history'],
                   default_config['random_autogen'],
                   default_config['variations_autogen'],
                   default_config['quality_tags'],
                   con_list[5] if not default_config['gen_limit'] else '1',
                   '',
                   default_config['skip'],
                   default_config['continuous_mode'])


def condition_gen(con_list):
    return gen_img(False,
                   con_list[0],
                   default_config['negative_prompt'] + con_list[1],
                   con_list[2],
                   con_list[3] if default_config['user_resize'] else default_config['width'],
                   con_list[4] if default_config['user_resize'] else default_config['height'],
                   con_list[5],
                   con_list[6],
                   default_config['strength'],
                   str(random.randint(10 ** 8, 10 ** 10 - 1)),
                   default_config['history'],
                   default_config['random_autogen'],
                   default_config['variations_autogen'],
                   default_config['quality_tags'],
                   con_list[7] if not default_config['gen_limit'] else '1',
                   '',
                   default_config['skip'],
                   default_config['continuous_mode'])


def default_condition_gen(con_list):
    return gen_img(False,
                   con_list[0],
                   default_config['negative_prompt'] + con_list[1],
                   default_config['model'],
                   default_config['width'],
                   default_config['height'],
                   default_config['steps'],
                   default_config['cfg_scale'],
                   default_config['strength'],
                   str(random.randint(10 ** 8, 10 ** 10 - 1)),
                   default_config['history'],
                   default_config['random_autogen'],
                   default_config['variations_autogen'],
                   default_config['quality_tags'],
                   default_config['num_images'],
                   '',
                   default_config['skip'],
                   default_config['continuous_mode'])


def send_msg(kwargs, msg):
    host: pkg.plugin.host.PluginHost = kwargs['host']
    host.send_person_message(kwargs['launcher_id'], msg) if kwargs[
                                                                'launcher_type'] == 'person' else host.send_group_message(
        kwargs['launcher_id'], msg)


# 注册插件
@register(name="paint", description="ai绘画", version="0.1", author="oliverkirk")
class HelloPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        pass

    # 当收到个人消息时触发
    @on(PersonNormalMessageReceived)
    @on(GroupNormalMessageReceived)
    def normal_message_received(self, event: EventContext, **kwargs):
        msg: str = kwargs['text_message'].strip()
        if msg.startswith('paint'):
            if not default_config['open']:
                event.add_return("reply", ['ai绘画功能未开启'])
            elif default_config['sessionid'] == '' or default_config['holara_r'] == '':
                event.add_return("reply", ["请设置sessionid与holara_r"])
            else:
                logging.debug("{}使用了ai绘画工具".format(kwargs['sender_id']))
                if msg.replace('paint', '').strip() in ['随机图片', '随机生成', '随机']:
                    images, remain, generation_cost = default_random_gen()
                    msg_list = response_process(images, remain, generation_cost)
                    logging.debug("{}使用了随机图片生成".format(kwargs['sender_id']))
                elif '条件随机' in msg.replace('paint', '').strip():
                    con_list = msg.replace('paint', '').replace('条件随机', '').strip().split('?')
                    images, remain, generation_cost = condition_random_gen(con_list)
                    msg_list = response_process(images, remain, generation_cost)
                    logging.debug("{}使用了条件随机生成".format(kwargs['sender_id']))
                elif '默认生成' in msg.replace('paint', '').strip():
                    con_list = msg.replace('paint', '').replace('默认生成', '').strip().split('?')
                    images, remain, generation_cost = default_condition_gen(con_list)
                    msg_list = response_process(images, remain, generation_cost)
                    logging.debug("{}使用了默认配置图片生成".format(kwargs['sender_id']))
                elif '条件生成' in msg.replace('paint', '').strip():
                    con_list = msg.replace('paint', '').replace('条件生成', '').strip().split('?')
                    images, remain, generation_cost = condition_gen(con_list)
                    msg_list = response_process(images, remain, generation_cost)
                    logging.debug("{}使用了条件图片生成".format(kwargs['sender_id']))
                else:
                    msg_list = ["意外参数"]
                send_msg(kwargs, msg_list)
            event.add_return("reply", ["生成完毕"])
            event.prevent_default()
            event.prevent_postorder()

    @on(PersonCommandSent)
    @on(GroupCommandSent)
    def normal_message_received(self, event: EventContext, **kwargs):
        command = kwargs['command']
        params = kwargs['params']
        if command == 'paint':
            if params[0] == 'help':
                help_str = '''欢迎使用ai绘图工具，本工具基于https://holara.ai/网站逆向爬虫\n绘图功能分为：\n1. 随机图片生成：【paint随机图片】或【paint随机】或【paint随机生成】\n2. 条件随机图片生成：【paint条件随机model?width?height?steps?cfg_scale?num_images】\n3. 默认配置条件生成：【paint默认生成tag?ntag】\n4. 条件图片生成：【paint条件生成tag?ntag?model?width?height?steps?cfg_scale?num_images】\n其中，model包含：\n1、Vibrance #Vibrant and bright\n2、Chroma #Inspired by ghostmix/AOM3\n3、Aika #Holara's aesthetic model\n4、Tranquility #Inspired by counterfeit3\n5、Lucid #Realistic and smooth\n6、Furry #Anthropomorphic furry model\n7、Akasha #Holara's traditional model\n8、Yami #Holara's alternative model\n管理员功能为：\n!paint on 开启ai绘画功能\n!paint off 关闭ai绘画功能\n!paint set user_resize <true/false> 是否允许用户设置图片大小\n!paint set gen_limit <true/false> 是否开启生成数量限制\n#该软件仅供学习交流，一切由该软件产生的不良影响由使用者承担#\n最后更新日期：2023年8月10日'''
                event.add_return("reply", [help_str])
            if kwargs['is_admin']:
                if params[0] == 'on':
                    default_config['open'] = True
                    event.add_return("reply", ["ai绘画已开启"])
                    logging.debug("{}ai绘画已开启".format(kwargs['sender_id']))
                elif params[0] == 'off':
                    default_config['open'] = False
                    event.add_return("reply", ["ai绘画已关闭"])
                    logging.debug("{}ai绘画已关闭".format(kwargs['sender_id']))
                elif params[0] == 'set':
                    if params[1] == 'user_resize':
                        if params[2] == 'true':
                            default_config['user_resize'] = True
                            event.add_return("reply", ["允许用户设置图片大小"])
                        elif params[2] == 'false':
                            default_config['user_resize'] = False
                            event.add_return("reply", ["禁止用户设置图片大小"])
                    if params[1] == 'gen_limit':
                        if params[2] == 'true':
                            default_config['gen_limit'] = True
                            event.add_return("reply", ["开启生成数量限制"])
                        elif params[2] == 'false':
                            default_config['gen_limit'] = False
                            event.add_return("reply", ["关闭生成数量限制"])
                    if params[1] == 'ntag':
                        default_config['negative_prompt'] = params[2]
                        event.add_return("reply", [f"设置默认负面词条为:{params[2]}"])
                    if params[1] == 'model':
                        default_config['model'] = params[2]
                        event.add_return("reply", [f"设置默认生成模型为:{params[2]}"])
                    if params[1] == 'width':
                        default_config['width'] = params[2]
                        event.add_return("reply", [f"设置默认宽为:{params[2]}"])
                    if params[1] == 'height':
                        default_config['height'] = params[2]
                        event.add_return("reply", [f"设置默认高为:{params[2]}"])
                    if params[1] == 'steps':
                        default_config['steps'] = params[2]
                        event.add_return("reply", [f"设置默认步数为:{params[2]}"])
                    if params[1] == 'cfg_scale':
                        default_config['cfg_scale'] = params[2]
                        event.add_return("reply", [f"设置默认词条相关度为:{params[2]}"])
                    if params[1] == 'num_images':
                        default_config['num_images'] = params[2]
                        event.add_return("reply", [f"设置默认生成数量为:{params[2]}"])
                    if params[1] == 'quality_tags':
                        default_config['quality_tags'] = params[2]
                        event.add_return("reply", [f"设置质量标签状态为:{params[2]}"])
            else:
                event.add_return("reply", ["你没有权限调用"])
            event.prevent_default()
            event.prevent_postorder()

    # 插件卸载时触发
    def __del__(self):
        pass

