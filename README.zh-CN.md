# Trellis for Research

[English guide](README.md)

本仓库提供两个科研 Spec 模板和一个可选的任务工作流：

- `research-computational`：分析、模拟、传统机器学习和数据处理。
- `research-deep-learning`：深度学习训练、模型比较和 checkpoint。
- `research` workflow：跨会话保留问题、状态和证据。

## 科研默认行为

- 从 `shared/research-minimal.md` 和相关项目事实开始，其余规范按具体问题查阅。
- 复用现有代码或直接写脚本、notebook，不要求拆包或配置系统；错误直接报出，实际失败再定位。
- 工作所需的聚焦检查属于工作本身：匹配条件的比较与计划内的 seed、在数据边界检查可能悄悄改变结论的假设、用实验自身输出作为证据。默认不添加测试套件、lint 或类型检查、检查代理，也不重复跑成功的命令。
- 指标是观察，包括负结果和零结果，不作为任务通过门槛。
- 保留解释结果所需的输入、实际参数、代码状态、环境和输出，复用现有记录；不强制 manifest，也不要求搬动输出。
- 按项目声明的规则隔离 held-out 数据；任务完成不代表结果定稿或探索结束。
- 跨会话上下文、独立交付或明确要求才建任务；子代理按需使用，不自动增加检查代理或多轮审查。
- 写作保留发现、证据、解释和真实限制，Methods 保留必要技术细节；不编造结论，不用软件运行状态冒充科学结果。

以上默认行为是主分支上尚未发布的修订；最后发布的版本仍为 `v0.5.0`，差异见 [CHANGELOG.md](CHANGELOG.md)。

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

深度学习项目把模板改为 `research-deep-learning`。取消标签会使用开发分支内容，安装结果不再固定。

## 已有项目与升级

Trellis 与科研模板各自有版本：

| 更新对象 | 官方入口 |
| --- | --- |
| 本机 Trellis CLI | `trellis upgrade`，跟随当前 npm channel |
| 项目原生文件和已登记的 spec | `trellis update`，使用本机 CLI 和配置的 spec 来源 |
| 科研模板版本 | 修改 spec 来源标签，并选择同版本 workflow |

需要采用较新的受支持版本时再升级 CLI；`trellis upgrade --dry-run` 只预览包升级，不更新项目文件。更新项目前先保存现有工作：

```sh
trellis update --migrate --dry-run
trellis update --migrate
```

修改过的文件进入冲突处理：合并时保留项目事实，`--skip-all` 保留本地修改，`--force` 覆盖冲突文件。固定的 spec 来源不会自动跳到新标签。命令区别见[官方升级说明](https://docs.trytrellis.app/zh/start/everyday-use)。

首次接入已有项目时，在临时目录安装所选模板，再合并需要的文件，保留数据约定、路径、任务和结果。以前手动复制的模板需一次性登记正式版本，供以后更新区分通用文件和项目改动。`init --append` 只补缺失文件；`init --overwrite` 替换整个 spec 目录，仅适合未修改的通用默认规范。

## 选择科研 Workflow

检查现有 workflow 改动后，将所选版本保存为独立文件：

```sh
trellis workflow \
  --save research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --force
```

把以下字段合并进 `.trellis/config.yaml`，保留其他设置；深度学习项目把模板改为 `research-deep-learning`：

```yaml
default_workflow: research
codex:
  dispatch_mode: inline
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0
    template: research-computational
```

`--save` 写入 `.trellis/workflows/research.md`，保留原生全局 workflow，但不设置项目默认值。workflow 和 spec 来源应选同一发布标签，修改上下文后重启 Agent 会话。`inline` 让 Codex 默认在主会话工作，需要独立分析时仍可用子代理。

保持 Trellis 原生脚本、hooks、skills 和 agents 不变，让它们随官方更新；带有独立流程的原生 skills 不会被本 workflow 自动调用。在项目 `AGENTS.md` 的 Trellis 托管区之外，指向 `.trellis/workflows/research.md` 和 `.trellis/spec/shared/research-minimal.md`，保留项目自己的约定。若未来 Trellis 改变 workflow 格式或加载接口，仍需更新模板。普通更新不会替换模板中不存在的自定义 skill 路径；registry 来源必须是支持的远端来源，不能填本地目录。

## 日常使用

从 `shared/research-minimal.md` 开始。直接描述科研问题，小任务不必建 task 或输入 slash 命令；会话 hook 正常的平台自动加载上下文，没有自动加载能力的平台才需要 `/trellis:start`。需要任务记录时，问题、计划和状态保留在 `prd.md`，结果写一次 `result.md` 或引用已有记录；seed、fold、参数变体默认留在同一科研问题下。

`/trellis:continue` 推进当前任务；`/trellis:finish-work` 在工作提交后归档任务并写 journal。这些原生命令按需使用，不增加逐阶段确认。

项目 spec 写真实的数据约定、源文件路径和可复用决定，实际任务需要时再补规则。[官方业务场景](https://docs.trytrellis.app/zh/start/real-world-scenarios)可作参考，选择与当前科研任务有关的部分。最小示例保留标准库脚本、实际结果和说明；目录参考不再附带空目录或占位配置。

仓库结构检查可运行 `python3 scripts/validate.py`。本次未发布修订的验证覆盖仓库检查，以及临时 Trellis `0.7.0-beta.3` 项目的原生上下文加载；尚未部署到已有科研项目。
