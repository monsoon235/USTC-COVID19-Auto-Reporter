# USTC-COVID19-Auto-Reporter

[https://weixine.ustc.edu.cn/2020/home](https://weixine.ustc.edu.cn/2020/home) 打卡程序，可使用 `crontab` 部署后自动打卡。

## 配置

编辑 `reporter.py` 中的如下部分，支持多个用户

```python
person_list = [
    {
        'id': 'PBxxxxxxxx',  # 学号，必选
        'password': 'xxxxxxxx',  # 密码，必选
        'now_province': 'xx0000',  # 所在省份行政代号，如江苏省为 320000，可选，如没有这条则默认为安徽
        'now_city': 'xxxx00',  # 所在城市行政代号，如江苏南京为 320100，可选，如没有这条则默认为合肥
    }, {
        # ...
    },
    # ...
]
```
