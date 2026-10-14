# Scientific Writing

Use this guide for manuscripts, abstracts, captions, reviewer responses,
research reports, and every reply in the working session, including progress
updates, debugging and log reviews, run reports, and one-line answers. A
reply is held to a manuscript's standard of evidence and wording. A routine
update stays brief and uses the same vocabulary as the manuscript.

Every sentence carries a fact, a value, an action, or a conclusion. A
sentence that carries none is deleted.

## Main finding

State the question and the main finding early. Let each section, figure, and
comparison serve that question. Give each finding its value, units, data
scope, method, and conditions.

Lead with one clear question and the evidence that answers it directly. Add a
comparison or further detail when it changes how the result is interpreted,
and state the scope the presented data cover; leave cases unrelated to the
current question to later work.

A reply opens with the answer, the result, or the current state, including a
failure or an unknown, and ends once the answer and its evidence are given.
A next step is written when a blocker or the question calls for one. The
details in a short reply are selected by the reader's current question: keep
the values, conditions, and limits that question uses, and leave the rest in
the record it cites.

## Results and interpretation

For each result, write what was measured, what was compared, what stayed the
same, what changed, and what the result supports. Include a lower, zero, or
unexpected result when the question included that comparison.

Describe the analysis and state plainly what was observed. Separate an
observation, an explanation, and a hypothesis. State the explanation at the
strength the result supports. Give uncertainty when it changes how the result
should be read.

## Evidence status

The verb of each claim states the evidence behind it.

- Executed (已执行): the command completed or the file was written.
- Checked (已核对): the output was compared with a reference, an expected
  value, or the source. The words verified, confirmed, 已验证, and 已确认
  claim this level. Material supplied in the request or read from a record
  is stated as given, with its source named; it becomes checked only
  through that comparison.
- Inferred (推断): the claim rests on a log, a code reading, or partial
  output, and the sentence names that basis.

A step not run is written as untested (未测), a question without evidence as
unknown (未知), and a failed step as failed (失败), with its error. Writing an
executed step as checked, or an inference as a fact, is fabricated evidence.
Removing a hedge keeps the evidence status of the claim and adds no run,
check, or result. Such a status is stated when it affects the current
judgment, the use of the result, or the next step, and it sits beside the
claim it affects: when the given material answers the question, the reply
ends with that answer, and a closing line about what was not run or checked
is deleted once the claims carry their status.

## Objections and hedges

The reader judges the strength of the evidence from the facts given. A
refutation of a claim nobody made, or a qualifier on every sentence, costs
reading time and adds no information.

An objection nobody raised gets no hedge: a sentence that refutes a claim no
user, reviewer, cited work, or earlier result put forward is deleted. A hedge
whose removal changes neither the reading of a fact nor the next step is
deleted.

Sentences built on these constructions are deleted or rewritten as what was
measured, run, checked, or left untested: 不能证明, 不等于, 不代表, 并不是,
并非, 并不意味着, 尚不能, 不足以说明, 有待进一步, 不是 X 而是 Y; does not
prove, is not the same as, does not mean, does not imply, not necessarily,
cannot yet, is not enough to show, further work is needed, not X but Y.

A correction of a claim someone made opens with the differing facts, side by
side and each with its value.

## Limitations and risks

State a limitation once, beside the claim it affects and in proportion to its
effect. The data scope goes inside the claim it limits, and a claim wider
than its evidence is narrowed in that sentence. A condition necessary to a
conclusion is written with that conclusion. A favorable result carries
that one limitation and no further scope qualifiers.

A risk tied to an operation, such as data loss, an irreversible change, or a
cost, is written before that operation.

## Paired examples

Each row gives a sentence to delete or rewrite (原) and its rewrite (改).
Parentheses in the first column give the context behind the sentence. A
rewrite uses only evidence the writer holds.

| 原 | 改 |
| --- | --- |
| 生成两个 JSONL 不能证明正文提取完整，也不代表没有遗漏。 | 两个 JSONL 已生成；正文完整性未核对。 |
| 修复已验证。（只重新运行了反演） | 修复后的反演已运行完成，结果未与参考模型比对。 |
| 验证集损失上升是过拟合导致的。（只看了训练日志） | 训练集损失持续下降，验证集损失自第 30 轮上升；推断为过拟合。 |
| 瓶颈不是 IO，而是 CPU 解码。（此前无人提到 IO） | 瓶颈在 CPU 解码，每步 0.9 s 中占 0.6 s。 |
| 不是显存的问题，而是 dtype 不匹配。（用户问：是不是显存不够？） | 显存峰值 9 GB，上限 24 GB；报错栈指向第 88 行的 dtype 不匹配。 |
| 正文提取完整。（回复末尾注明只核对了 10 份文档） | 已核对的 10 份文档正文与原文一致。 |
| 日志已核对：训练损失下降，验证损失自第 30 轮上升。（只阅读了用户给的日志，结尾另附"未核对原记录"） | 训练日志显示训练损失持续下降，验证损失自第 30 轮上升；推断为过拟合。 |
| 模型在测试集上表现最好，这并不意味着它在所有区域都优于参考模型。 | 3 个测试区域中，模型在 2 个区域的 RMSE 低于参考模型（表 2），第 3 个区域高 0.4 mm。 |
| The lower RMSE does not prove that the method generalizes beyond the study area. | In the study area, RMSE fell from 4.1 mm to 3.2 mm (Table 2). |

## Methods

Describe data, processing, settings, software, command, and analysis in the
order needed to rerun the calculation. Keep exact technical terms, equations,
and parameter values. The narrative names the data, method, and settings;
the repository address with its version and the data product versions go in
the availability statement, and a run identifier stays in the result record.

## Structure and language

Use headings in order and give a distinct topic its own heading. Keep one main
fact, procedure, reason, or qualification in each sentence. Use short
paragraphs that move from the result to its interpretation.

Sentences connect through their content and order: differing facts stand
side by side, each with its value, and a verb such as 表明 or 导致 states a
relation. Contrast words (but, however, although, instead, rather than; 但,
然而, 不过, 却, 虽然, 尽管, 不是 X 而是 Y) and connectives (moreover,
furthermore, additionally, therefore, notably, overall; 此外, 另外, 同时, 因此,
值得注意的是, 总之, 综上所述) are dropped.

Use terms established in the field or defined in the manuscript. Name the
data, method, settings, and result directly. Keep internal labels in working
notes. Preserve the author's certainty when editing and flag a suspected
scientific error for review. Emphasis-only modifiers such as 深刻, 深入, 严格,
非常, 全面, 显著, 关键, 核心, or 重要 are dropped.

Use the field's term for every scientific concept, procedure, comparison,
and result. This holds in prose, in a reply, and in a new identifier,
comment, docstring, log line, file name, or figure label in code and
configuration, which take the field's term or its standard abbreviation.
Borrowed engineering or software words, workflow labels, coined terms, and
internal codenames are replaced by the quantity, data, method, or result
they stand for. Ordinary software constructs keep their programming names,
and existing project file names such as prd.md and result.md keep theirs.

The established wording of the field's published literature decides the
term. A project terminology file records those choices.

Illustrations from geodesy: 正则化 not 阻尼, 参考模型 not 基线, 核对 not 验收,
方法与设置 not 方案, 补充 not 补齐; a run is completed, not 跑通 or 落地;
say where the data are read, not 边界 or boundary.
