# Trellis for Research

[English guide](README.md)

本仓库提供两个科研 Spec 模板和一个可选的任务工作流：

- `research-computational`：分析、模拟、传统机器学习和数据处理。
- `research-deep-learning`：深度学习训练和模型比较。
- `research` workflow：跨会话保留问题、数字和复现信息。

## 科研默认行为

- 从 `shared/research-minimal.md` 和相关项目事实开始，其余规范按具体问题查阅。
- 复用现有代码或直接写脚本、notebook。额外的包、配置层和包装在有具体理由时添加；错误直接报出，实际失败再定位。
- 运行能回答问题的最小计算。比较、seed 或输入检查在能回答问题或避免结果被悄悄改变时添加。
- 在现有记录中保留数字，以及复现它所需的命令、数据、代码、seed 和环境信息；大输出默认不进 Git。
- 按项目声明的规则分开用于最终评估的数据；完成一个任务后可以继续探索。
- 跨会话上下文、独立交付或明确要求时建任务；普通工作由主会话完成。
- 写作直接陈述数字、条件、解释和真实限制，使用领域已有术语，写清数据、方法和设置。

版本间差异见 [CHANGELOG.md](CHANGELOG.md)。

## 安装固定版本

当前版本标签为 `v0.6.11`，对应 Trellis `0.7.0-beta.4`。使用下面的固定版本命令：

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.4
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.11 \
  --template research-computational \
  --claude --codex
```

深度学习项目把模板改为 `research-deep-learning`。取消标签会使用开发分支内容，安装结果不再固定。随后按下一节选择科研 workflow。

## 选择科研 Workflow

把同一发布版本的 workflow 保存为独立变体；已有项目先检查现有 workflow 改动：

```sh
trellis workflow \
  --save research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.11 \
  --force
```

把以下字段合并进 `.trellis/config.yaml`，保留其他设置；深度学习项目把模板改为 `research-deep-learning`：

```yaml
default_workflow: research
codex:
  dispatch_mode: inline
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.11
    template: research-computational
```

`--save` 写入 `.trellis/workflows/research.md`，原生 `.trellis/workflow.md` 继续随官方更新；`default_workflow` 让科研变体成为项目默认 workflow。workflow 和 spec 来源应选同一发布标签，修改上下文后重启 Agent 会话。`inline` 让 Codex 默认在主会话工作；不设置时，Codex 默认把实现和检查交给子代理。问题需要时再使用子代理。

保留 Trellis 原生脚本、hooks、skills 和 agents，让它们随官方更新。`AGENTS.md` 中由 Trellis 管理的区块描述原生 workflow；在该区块之后指向 `.trellis/workflows/research.md` 和 `.trellis/spec/shared/research-minimal.md`，保留项目自己的约定。registry 使用受支持的远端来源。

## 已有项目与升级

Trellis 与科研模板各自有版本：

| 更新对象 | 官方入口 |
| --- | --- |
| 本机 Trellis CLI | `trellis upgrade`，跟随当前 npm channel |
| 项目原生文件和已登记的 spec | `trellis update`，使用本机 CLI 和配置的 spec 来源 |
| 科研模板版本 | 修改 spec 来源标签，并选择同版本 workflow |

需要采用较新的受支持版本时再升级 CLI；`trellis upgrade --dry-run` 只预览包升级，不更新项目文件。更新项目前先保存现有工作：

```sh
trellis update --dry-run
trellis update
```

项目未改动的模板文件自动更新。改动过的文件进入冲突处理：合并时保留项目事实，`--skip-all` 保留本地修改，`--force` 覆盖冲突文件。固定的 spec 来源不会自动跳到新标签。命令区别见[官方升级说明](https://docs.trytrellis.app/zh/start/everyday-use)。

首次接入已有项目时，在临时目录安装所选模板，再合并需要的文件，保留数据约定、路径、任务和结果。以前手动复制的模板需一次性登记正式版本，供以后更新区分通用文件和项目改动。`init --append` 只补缺失文件；`init --overwrite` 替换整个 spec 目录，仅适合未修改的通用默认规范。

## 日常使用

从 `shared/research-minimal.md` 开始。直接描述科研问题，小任务不必建 task 或输入 slash 命令；会话 hook 正常的平台自动加载上下文和科研 workflow 摘要，没有自动加载能力的平台才需要 `/trellis:start`。需要任务记录时，在 `prd.md` 留下问题和下一步，在任务的 `result.md` 或项目现有结果记录中写结果和复现信息；参数变体默认留在同一科研问题下。

后续会话从任务的 `prd.md` 和 `result.md` 继续。`task.py finish` 结束当前任务，记录留在原路径，结果、代码和报告中的引用继续有效；`/trellis:finish-work` 会归档任务，把目录移到 `.trellis/tasks/archive/` 下并写 journal，适用于没有被引用的记录。

项目自己的事实和规则（数据约定、源文件路径、术语、可复用决定）写在项目专用的 spec 层，例如 `.trellis/spec/project/index.md` 及其链接的文件，实际任务需要时再补规则。会话启动时会列出该索引；模板文件保持原样，升级时不产生冲突。[官方业务场景](https://docs.trytrellis.app/zh/start/real-world-scenarios)可作参考，选择与当前科研任务有关的部分。最小示例保留标准库脚本、实际结果和说明；目录参考只列出当前使用的文件。

仓库结构检查可运行 `python3 scripts/validate.py`。
