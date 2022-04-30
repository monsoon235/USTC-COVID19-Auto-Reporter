# USTC-COVID19-Auto-Reporter

[https://weixine.ustc.edu.cn/2020/home](https://weixine.ustc.edu.cn/2020/home) 打卡程序，可使用 `crontab` 部署后自动打卡。

## 配置

编辑 `info.yaml`，支持多个用户

```yaml
## 示例
- id: PBxxxxxxxx  # 学号，必选
  password: xxxxxxxx  # 密码，必选
  jinji_lxr: 张三  # 紧急联系人，必选
  jinji_guanxi: 父亲  # 紧急联系人关系，必选
  jiji_mobile: xxxxxxxxxxx  # 紧急联系人电话，必选
# 以下为可选项
  juzhudi: 安徽省合肥市蜀山区
  body_condition: 1  # 当前身体状况 1:正常 2:疑似 3:确诊 4:其他
  body_condition_detail:   # 具体情况，当前身体状况为“其他”时填写
  now_status: 1  # 当前状态 1:正常在校园内 2:正常在家 3:居家留观 4:集中留观 5:住院治疗 6:其他
  now_status_detail:   # 具体情况，当前状态选择“其他”时填写
  has_fever: 0  # 目前有无发热症状 0:无 1: 有
  last_touch_sars: 0  # 是否接触过疑似患者  0:无 1:有
  last_touch_sars_date:   # 最近一次接触日期，当是否接触过疑似患者为“有”时填写
  last_touch_sars_detail:   # 具体情况，当是否接触过疑似患者为“有”时填写
  is_danger: 0   # 当前居住地是否为疫情中高风险地区 0:无 1:有
  is_goto_danger: 0   # # 14天内是否有疫情中高风险地区旅居史 0:无 1:有
  other_detail:   # 其他情况说明

## 支持多个账户配置
- id: PByyyyyyyy
  password: yyyyyyyy
# ......
```

## 部署 & 运行

安装依赖：

```shell script
pip3 install -r requirements.txt
```

### 手动运行

```shell script
python3 reporter.py
```

### crontab 计划任务

```shell script
crontab -e
```

添加一行

```text
# 每小时运行一次
0 * * * * cd <reporter.py 所在的路径> && python3 reporter.py
```

### 利用 Github CI/CD 计划执行

**首先确保不要在 public repo 中存储你的密码，应当在 private repo 中部署。**

**但即使是 private repo 也不推荐存储敏感信息，这种部署方式仅当无 VPS 可用时推荐使用。**

**USTC 学生可以在 [https://vlab.ustc.edu.cn/](https://vlab.ustc.edu.cn/) 中建立一个免费的虚拟主机。**

新建一个私有仓库

```shell script
git clone <私有仓库地址>
cd <私有仓库名称>
git remote add upstream https://github.com/yjh1021317464/USTC-COVID19-Auto-Reporter.git
git pull upstream master
# ... 编辑 info.yaml
mv github .github # 启用 github CI/CD
git add .
git commit -m 'set private info'
git push
```
