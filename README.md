# QChatAIPaint
适用于QChatGPT的ai图像生成插件,基于[Holara](https://holara.ai/)
每天签到可领25token，可生成6张512x512图片
## 1、前置工作

- 下载本插件`!plugin get https://github.com/oliverkirk-sudo/QChatAIPaint.git`
- 在[Holara](https://holara.ai/)获取sessionid与holara_r(Cookie中)

## 2、修改配置文件

- 参数请参考网站[Holara](https://holara.ai/)

```python
default_config = {
    "open": True, #是否默认开启
    "user_resize": False, #是否允许用户修改图片尺寸
    "gen_limit": True, #是否限制每次只生成一张图片
    "negative_prompt": "nsfw", #默认的负面tag
    "model": "Vibrance", #默认使用的模型
    "width": "512", #默认宽度
    "height": "512", #默认高度
    "steps": "30", #默认步数
    "cfg_scale": "7", #默认关联度
    "strength": "60",
    "history": "true",
    "random_autogen": "false",
    "variations_autogen": "true",
    "quality_tags": "true",
    "num_images": "1", # 默认一次生成的图片数量
    "skip": "2",
    "continuous_mode": "off",
    "sessionid": "", #获取的sessionid
    "holara_r": "", #获取的holara_r
}

```
model包含：

- 1、Vibrance #Vibrant and bright
- 2、Chroma #Inspired by ghostmix/AOM3
- 3、Aika #Holara's aesthetic model
- 4、Tranquility #Inspired by counterfeit3
- 5、Lucid #Realistic and smooth
- 6、Furry #Anthropomorphic furry model
- 7、Akasha #Holara's traditional model
- 8、Yami #Holara's alternative model


## 3、包含的指令
用户使用命令：

- aipaint help 获取帮助
- 随机图片生成：【aipaint随机图片】或【aipaint随机】或【aipaint随机生成】
- 条件随机图片生成：【aipaint条件随机model?width?height?steps?cfg_scale?num_images】
- 默认配置条件生成：【aipaint默认生成tag?ntag】
- 条件图片生成：【aipaint条件生成tag?ntag?model?width?height?steps?cfg_scale?num_images】

管理员使用命令：

- !aipaint on  开启ai绘画
- !aipaint off 关闭ai绘画
- !aipaint set <option> 设置用户权限
- !aipaint <option> <value> 设置配置项的默认值

## 4、我的其他插件
- [oliverkirk-sudo/chat_voice](https://github.com/oliverkirk-sudo/chat_voice) - 文字转语音输出，支持HuggingFace上的[VITS模型](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer),azure语音合成,vits本地语音合成,sovits语音合成
- [oliverkirk-sudo/qchat_system_status](https://github.com/oliverkirk-sudo/qchat_system_status) - 以图片的形式输出系统状态
- [oliverkirk-sudo/QChatCodeRunner](https://github.com/oliverkirk-sudo/QChatCodeRunner) - 基于[CodeRunner-Plugin](https://github.com/oliverkirk-sudo/CodeRunner-Plugin)的代码运行与图表生成插件
- [oliverkirk-sudo/QChatWeather](https://github.com/oliverkirk-sudo/QChatWeather) - 生成好看的天气图片，基于和风天气
- [oliverkirk-sudo/QChatMarkdown](https://github.com/oliverkirk-sudo/QChatMarkdown) - 将机器人输出的markdown转换为图片，基于[playwright](https://playwright.dev/python/docs/intro)

</br>
<b>该软件仅供学习交流，一切由该软件产生的不良影响由使用者承担</b>
</br>
