# Fitting A Line To Noisy Synthetic Observations

## Result

Ordinary least squares fitted a slope of 2.0143 and an intercept of 0.9866 to
200 observations generated from `y = 2x + 1` with Gaussian noise of standard
deviation 0.5. On these same observations, RMSE was 0.4590 and R-squared was
0.9939. The fitted coefficients were close to the generating values for this
sample; this single fit does not establish performance on new data or validate
linearity in real measurements.

## Method And Evidence

The inputs are equally spaced over `[0, 10]`. Python's `random.Random(42)`
generates the noise; `statistics.linear_regression` fits the line. Metrics use
all 200 fitting observations. [The script](../analysis.py) contains the full
calculation, and [the recorded output](../result.json) contains the parameters,
metrics, and Python version. No independent evaluation sample was used.

## 中文结果

对 200 个带噪合成观测做最小二乘拟合，斜率为 2.0143，截距为 0.9866；生成关系为
`y = 2x + 1`，加入的高斯噪声标准差为 0.5。在同一批拟合样本上，均方根误差为
0.4590，决定系数为 0.9939。该样本的拟合参数接近生成值，但一次样本内拟合不能
说明新数据上的表现，也不能证明真实观测符合线性关系。计算和实际输出见上面的文件。
