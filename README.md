# groot
一个通过大模型语义理解选股并完成策略回测与策略报告输出的量化玩具，目的是**快速验证投资小念头**。

## 框架

## 使用方法

## 结果查询



# 感谢
- [x] [挖地兔tushare](https://www.tushare.pro/document/2):提供股票日行情数据api接口
- [x] [同花顺问财](https://www.iwencai.com/unifiedwap/home/index)：提供标准的数据字典和免费的智能查询；也要感谢[zsrl提供的开源工具](https://github.com/zsrl/pywencai#loop)




# 最后
1. 需要有明确的语义定位到股票，范围太大的模糊语义容易卡死
2. 如果请求报错，可能是网络问题，请刷新浏览器重试
3. 大模型语义理解需要在时间轴反复请求查询，性能上暂时无法提速，效率考虑不开放日频等回测频率
