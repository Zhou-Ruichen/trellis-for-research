# Trellis for Research

[English guide](README.md)

本仓库提供两个科研 Spec 模板和一个可选的任务工作流：

- `research-computational`：分析、模拟、传统机器学习和数据处理。
- `research-deep-learning`：深度学习训练、模型比较和 checkpoint。
- `research` workflow：跨会话保留问题、状态和证据。

## 科研默认行为

- 默认只读最小科研规则和相关项目事实，其余规范按具体问题查阅。
- 可以直接写脚本或 notebook，不要求拆包、配置系统、兼容层或测试套件。
- 只检查可能悄悄改变科学结果的数据条件。文件和库错误直接报出，实际失败再定位。
- 完成计划中的比较、seed 和 fold。正、负、零结果都是观察，不作为任务通过门槛。
- 记录解释结果所需的输入、实际参数、代码状态、环境和输出。复用现有日志、配置或笔记，不强制 manifest 格式，也不要求搬动输出。
- 小任务直接做。跨会话或独立交付才按需建任务，不要求声明模式和运行级别。
- 子代理按需使用，不自动增加检查代理、多轮审查或未要求的软件验证。
- 科学写作保留发现、证据、解释和真实限制，Methods 保留必要技术细节，不编造结论或使用套话代替事实。

以上精简属于 [CHANGELOG.md](CHANGELOG.md) 的 Unreleased 内容，尚未包含在下面固定标签的安装命令中。

## 安装已发布版本

当前发布标签为 `v0.4.3`，使用 Trellis `0.7.0-beta.3`：

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --claude --codex
```

深度学习项目把模板改为 `research-deep-learning`。取消标签会使用已发布到开发分支的内容，安装结果不再固定。

## 已有项目

保留项目自己的数据约定、路径、任务和结果。先保存现有改动，在临时目录安装所选版本，再比较并合并需要的规则。

`--append` 只补缺失文件，不更新已有规范：

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-computational \
  --append --claude --codex
```

`--overwrite` 会替换整个 `.trellis/spec/`，仅适合仍未修改的通用默认规范。

## 更新 Workflow

检查现有 workflow 改动后执行：

```sh
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --force
```

项目配置使用 `default_workflow: research`。修改后重启 Agent 会话。
更换 workflow 不会改写另外安装的原生 skill 或 agent；调用它们仍需遵守当前任务的科研和验证要求。

## 日常使用

从 `shared/research-minimal.md` 开始。需要任务记录时，把问题、计划和状态保留在 `prd.md`，结果写一次 `result.md`，或引用已有记录。seed、fold、参数变体默认留在同一科研问题下。

目录和示例供参考，不要求照搬。用户要求验证时，可运行 `python3 scripts/validate.py` 检查仓库结构；它不验证科学结论。

历史上的 `v0.4.2` 安装检查不能证明本次未发布修改已经通过验证。
