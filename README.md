# HFish-iKuai

将 HFish 蜜罐系统截获的 IP 加到 iKuai 的黑名单中去

## Usage

1. 在 iKuai 的 `网络设置 > 终端分组设置 > IP分组` 中添加一条名为 `hfish-attack-ip-list` 的规则，IP列表可随便填写，比如填 `8.8.8.8`
   + 请保证刚才创建的那条记录的 ID 为 1，否则请修改 `ikuai_request.json`
   + 如果不知道怎么看 ID，可在提交编辑 IP 分组的时候，在开发者工具中查看名为 `call`、`func_name` 为 `ipgroup` 的那条请求记录，将其 `payload` 复制进 `ikuai_request.json`
2. 设定环境变量，环境变量解释如下
   + `HFISH_API`：包含密钥的 HFish 蜜罐系统的 API，形如：`https://192.168.1.2:4433/api/v1/attack/ip?api_key=${key}`
   + `IKUAI_USERNAME`：iKuai 的用户名，比如 `admin`
   + `IKUAI_MD5PASSWORD`：iKuai 的密码的 md5 值，形如 `e10adc3949ba59abbe56e057f20f883e`
   + `IKUAI_API`：iKuai 的地址，比如 `http://192.168.1.1`
3. 前往 [github.com/Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip) 下载 `Country.mmdb`，放至运行目录下
4. 运行 `python3 main.py`
5. 按照预期 IP 分组中应该包含了蜜罐系统检测到的 IP，在 ACL 中引用该 IP 分组即可
