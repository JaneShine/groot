# groot: Make your flash of thought tradable
<p align="center">
  <img src="https://raw.githubusercontent.com/JaneShine/groot/master/picture/logo.png" width="45%">
</p>

<p align="center">
  <a href="https://github.com/JaneShine/groot/stargazers/">
    <img src="https://img.shields.io/github/stars/JaneShine/groot" alt='pypi'>
  </a>
  <a href="https://pypi.org/project/groot-quant/">
    <img src="https://img.shields.io/badge/pypi-v0.2.1-brightgreen.svg?style=popout" alt='pypi'>
  </a>

  <a href="https://github.com/JaneShine/groot/issues">
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=popout" alt="contributions">
  </a>
  <a href="https://github.com/JaneShine/groot?tab=MIT-1-ov-file">
    <img src="https://img.shields.io/github/license/JaneShine/groot.svg?style=popout" alt="license">
  </a>
</p>

一个通过大模型语义理解选股并完成A股策略回测与策略报告输出的量化玩具，目的是**快速验证投资小念头**。

`groot`是一个将某种投资思维进行量化验证的尝试，其目的在于把一些投资思路转化为可交易的信号。

---
 A quantitative tool that selects stocks through a large model semantic filtering and completes *A-share* strategy backtesting and strategy report output, aiming to **quickly verify investment ideas.**

`groot` is an attempt to quantitatively verify institutional subjective thinking, with the goal of transforming some investment ideas into **tradable** signals.

## 立刻开始
安装
```
pip install groot-quant
```
输入指令
```bash
imgroot
```
然后在浏览器中访问[http://127.0.0.1:8050/](http://127.0.0.1:8050/)

![alt text](https://raw.githubusercontent.com/JaneShine/groot/master/picture/start.png)

### 向groot提出一个投资思路
#### 可以尝试各种prompt
- 中外资加仓持股股数前十的股票
- 连续10日资金流入前十的股票
- 周平均换手率大于10%的5G概念股中市值前10的股票

### 另外一些可定义的参数
| 参数             | 参数说明                                                   |
| ---------------- | ---------------------------------------------------------- |
| StartDate        | 回测开始时间                                               |
| EndDate          | 回测结束时间                                               |
| BacktestFreq     | 再平衡周期                                                 |
| Actual Book Size | 账户实际初始资金                                           |
| Commision        | 交易佣金，默认千二                                         |
| Multiper         | 交易乘数，股票按手买卖，默认100<br>回测指数的话可以设置为1 |


## 得到直观结果
### 结果图表

![alt text](https://raw.githubusercontent.com/JaneShine/groot/master/picture/pnl.png)
![alt text](https://raw.githubusercontent.com/JaneShine/groot/master/picture/trade.png)

### 在交易记录台查看日志
![alt text](https://raw.githubusercontent.com/JaneShine/groot/master/picture/log0.png)
![alt text](https://raw.githubusercontent.com/JaneShine/groot/master/picture/log1.png)

#### 感谢
- [x] [挖地兔tushare](https://www.tushare.pro/document/2):提供股票日行情数据api接口,需要注册后完善个人资料，复制token方能获取A股日度行情数据
  - [x] 填写成功后的token下次浏览器刷新后可以不填
- [x] [同花顺问财](https://www.iwencai.com/unifiedwap/home/index)：提供标准的数据字典和免费的智能查询；也要感谢[zsrl提供的开源工具](https://github.com/zsrl/pywencai#loop)


#### 最后
1. 需要**有明确的语义定位到有限个股票**，范围太大的模糊语义容易卡死；
2. 如果请求股票代码报错，大概率是网络问题，请刷新浏览器重新点击`Go`；
3. 大模型选股的语义理解步骤需要在时间轴反复提交prompt请求，性能上暂时无法提速，效率考虑不开放日频等回测频率。
4. 需要安装[node.js v16+](https://nodejs.org/download/docs/v0.12.7/)
