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

以上精简包含在 `v0.5.0` 中，变更见 [CHANGELOG.md](CHANGELOG.md)。

## 安装已发布版本

当前发布标签为 `v0.5.0`，使用 Trellis `0.7.0-beta.3`：

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --claude --codex
```

深度学习项目把模板改为 `research-deep-learning`。取消标签会使用已发布到开发分支的内容，安装结果不再固定。

## 已有项目与升级

Trellis 与科研模板各自有版本：

| 更新对象 | 官方入口 |
| --- | --- |
| 本机 Trellis CLI | `trellis upgrade`，跟随当前 npm channel |
| 项目原生文件和已登记的 spec | `trellis update`，使用本机 CLI 和配置的 spec 来源 |
| 科研模板版本 | 修改 spec 来源标签，并选择同版本 workflow |

需要采用较新的受支持版本时再升级 CLI；`trellis upgrade --dry-run` 可以预览包升级操作，但不会更新项目文件。更新项目时先保存现有工作，再预览并执行迁移：

```sh
trellis update --migrate --dry-run
trellis update --migrate
```

修改过的文件进入冲突处理，合并时保留项目事实。`--skip-all` 保留本地修改，`--force` 会覆盖冲突文件。固定的 spec 来源不会自动跳到新标签。命令区别见[官方升级说明](https://docs.trytrellis.app/zh/start/everyday-use)。

首次接入已有项目时，在临时目录安装所选模板，再合并需要的文件，保留数据约定、路径、任务和结果。以前手动复制的模板需要一次性登记正式版本，供以后更新区分通用文件和项目改动。

`init --append` 只补缺失文件，不能刷新已有定制规范；`init --overwrite` 会替换整个 spec 目录，仅适合未修改的通用默认规范。

## 选择科研 Workflow

检查现有 workflow 改动后，将所选版本保存为独立文件：

```sh
trellis workflow \
  --save research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --force
```

把以下字段合并进 `.trellis/config.yaml`，保留其他设置。深度学习项目将 spec 模板改为 `research-deep-learning`：

```yaml
default_workflow: research
codex:
  dispatch_mode: inline
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0
    template: research-computational
```

`--save` 写入 `.trellis/workflows/research.md`，保留原生全局 workflow，但不会设置项目默认值。workflow 和 spec 来源应选择同一个发布标签。修改上下文后重启 Agent 会话。
`inline` 让 Codex 默认在主会话工作，需要独立分析时仍可使用子代理。
更换 workflow 不会改写另外安装的原生 skill 或 agent；调用它们仍需遵守当前任务的科研和验证要求。

保持 Trellis 原生脚本、hooks、skills 和 agents 不变，让它们随官方更新。日常科研直接遵循 research workflow，按需使用其中的任务 CLI，不自动调用带有独立步骤和验证流程的原生 skills。

在项目 `AGENTS.md` 的 Trellis 托管区之外，用简短入口指向 `.trellis/workflows/research.md` 和 `.trellis/spec/shared/research-minimal.md`，保留项目自己的约定。这样无需维护改写过的原生 skills；如果未来 Trellis 改变 workflow 格式或加载接口，仍需更新模板。

普通更新不会替换模板中不存在的自定义 skill 路径。registry 来源必须是支持的远端来源，不能填写本地目录。

## 日常使用

从 `shared/research-minimal.md` 开始。需要任务记录时，把问题、计划和状态保留在 `prd.md`，结果写一次 `result.md`，或引用已有记录。seed、fold、参数变体默认留在同一科研问题下。

日常直接描述科研问题，小任务不必建 task 或输入 slash 命令。会话 hook 正常的平台会自动加载上下文；没有自动加载能力的平台才需要 `/trellis:start`。

`/trellis:continue` 推进当前任务；`/trellis:finish-work` 在工作提交后归档任务并写 journal。这些原生命令按需使用，仍遵守科研 workflow 的执行和验证要求，不增加逐阶段确认。

项目 spec 写真实的数据约定、源文件路径和可复用决定。实际任务需要时再补规则，不填满所有模板，也不把单次观察写成长期要求。[官方业务场景](https://docs.trytrellis.app/zh/start/real-world-scenarios)可作参考，选择与当前科研任务有关的部分。

目录和示例供参考，不要求照搬。用户要求验证时，可运行 `python3 scripts/validate.py` 检查仓库结构。

本次精简规则已在已有科研仓库中安装，并检查了 Trellis `0.7.0-beta.3` 的阶段和步骤读取。
