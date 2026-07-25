# Recovering A Linear Process From Noisy Observations

This is a curated report for the runnable example. It demonstrates the
scientific-writing rules in `shared/scientific-writing.md`: the narrative leads
with the question and the finding, numbers carry their context, and engineering
detail (config, run id) is referenced, not narrated.

The data are synthetic: `y = 2x + 1 + noise`, with `x` on `[0, 10]`, 200 points,
and Gaussian observation noise of standard deviation 0.5 (seed 42). The model is
one-feature linear regression trained by full-batch gradient descent.

A reader who wants to verify any number can follow the retained run archived
under `outputs/20260725-100000-linear/`.

---

## English Version

**Scientific question.** Can a simple linear model recover the parameters of the
process that generated the observations, and how closely does its residual error
approach the irreducible observation noise?

**Finding.** The fitted line recovers the generating slope and intercept to
within 0.8% and 1.8% of their true values (2.015 vs 2.0, 0.982 vs 1.0), and its
root-mean-square error (0.459) sits at the observation-noise floor (0.5). Over
the 200-point sample the model explains 99.4% of the variance in the target. The
small positive bias in the slope is paired with a small negative bias in the
intercept, consistent with the finite-sample correlation between the two
estimates rather than a misspecified model.

**Interpretation and limits.** Because the data are synthetic and the generating
process is exactly linear, this result confirms that the estimation procedure is
correct; it does not show that linearity holds for real measurements. The
residual error is dominated by the injected observation noise, so reducing it
further would require averaging repeated observations at each input value rather
than a more flexible model. The fit is evaluated on the same points used for
training, so it characterizes in-sample recovery, not generalization.

**Evidence.** The retained run, including the config, checkpoint, metrics, and
environment snapshot, is archived under `outputs/20260725-100000-linear/`.

---

## 中文版

**科学问题**：一个简单的线性模型能否从带噪观测中恢复出生成过程的真实参数，其残差误差距离不可约的观测噪声下限有多近？

**结论**：拟合直线将生成斜率与截距分别恢复到真实值的 0.8% 和 1.8% 以内（斜率 2.015，真值 2.0；截距 0.982，真值 1.0），其均方根误差 0.459 落在观测噪声水平 0.5 上。在 200 个样本点上，模型解释了目标方差的 99.4%。斜率的微小正偏与截距的微小负偏同时出现，这与有限样本下二者估计的统计相关一致，而非模型设定错误。

**解释与局限**：由于数据是合成的，且生成过程严格线性，这一结果验证了估计流程的正确性，并不能说明线性关系对真实观测同样成立。残差误差主要由注入的观测噪声决定；要进一步降低误差，应在同一输入处重复观测取平均，而不是改用更复杂的模型。本结果在训练所用样本上进行评估，因此刻画的是样本内参数恢复能力，而非泛化能力。

**证据**：完整结果（配置、模型权重、指标与环境快照）存档于
`outputs/20260725-100000-linear/`。

---

## What To Avoid

The following paragraph breaks the scientific-writing rules. It narrates the
engineering actions, leans on empty intensifiers, and presents run mechanics as
if they were findings:

> We ran a retained training run and recorded metrics.json. The pipeline
> produced an RMSE of 0.459 and an R-squared of 0.994, demonstrating a robust
> and scalable linear model. We leveraged full-batch gradient descent and the
> artifact was promoted to retained. State-of-the-art performance was achieved.

The Chinese equivalent below fails the same way, padding the result with
official-document flourish and engineering nouns instead of stating it:

> 在深度学习的背景下，我们运行了 retained run 并记录了 metrics.json。该
> pipeline 充分赋能了线性模型的训练，RMSE 达到 0.459，R 平方达到 0.994，
> 彰显了模型的鲁棒性与可扩展性，全面提升了拟合能力，达到了 state-of-the-art
> 的水平。

Contrast it with the versions above: those open with the question and the
physical finding, give every number its sample context, separate interpretation
from evidence, and keep the run machinery out of the narrative.
