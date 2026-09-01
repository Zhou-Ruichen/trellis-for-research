# Trellis for Research 中文安装指南

[English README](README.md)

本仓库提供两个科研 Spec 模板和一个 `research` Workflow：

- `research-computational`：计算科研、统计分析、模拟、传统机器学习和数据处理；
- `research-deep-learning`：使用深度学习训练和评估的科研项目；
- `research` Workflow：保留科研问题、必要决策和结果，不给日常工作增加审批步骤。

模板不限定学科。是否包含深度学习训练代码决定 Spec 选择，数据所属领域不决定模板名称。

## 版本

当前发布版 `v0.4.3` 使用 Trellis `0.7.0-beta.3` 的 Marketplace Workflow 接口，请显式安装该版本：

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
trellis --version
```

固定 Git 标签可以避免安装结果随 `main` 变化。

`v0.4.2` 已使用 Trellis `0.7.0-beta.3` 从 GitHub 完成远程安装检查，`research-deep-learning` 模板和 `research` Workflow 均可安装。

## 新项目

非深度学习科研：

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --claude --codex
```

深度学习科研：

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-deep-learning \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --claude --codex
```

## 已有项目

先确认目标仓库和当前改动：

```sh
trellis --version
git status --short --branch
```

已有自定义 Spec 时不要使用 `--overwrite`。先提交或另行保存现有改动，然后在临时目录安装新模板并比较差异：

```sh
tmpdir="$(mktemp -d)"
cd "$tmpdir"
git init
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-deep-learning \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --claude --codex -y
```

把 `research-deep-learning` 换成项目需要的 `research-computational`。比较临时目录和项目的 `.trellis/spec/`，只合并需要更新的规则。不要替换 `.trellis/tasks/`、`.trellis/workspace/` 或项目自己的 Spec 文件。

项目缺少部分模板文件且现有文件应保持不变时，可以使用 `--append`：

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-computational \
  --append \
  --claude --codex
```

`--append` 不更新已存在的文件。它适合补齐缺失文件，不适合替代差异比较。

## 更新 Workflow

已有 Trellis 0.7 项目可以独立选择或刷新 Workflow：

```sh
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --force
```

执行前检查当前 `.trellis/workflows/` 改动。`--force` 会替换同名 Workflow；它不会替换 `.trellis/spec/`、任务记录或项目代码。Trellis 将非原生 Workflow 视为项目管理的文件，后续 `trellis update` 不会自动恢复原生 Workflow。

确认 `.trellis/config.yaml` 使用：

```yaml
default_workflow: research
```

重新启动 Agent 会话后，新 Workflow 状态提示才会进入后续对话。

## 使用方式

- 单次会话内能完成的小任务不要求创建 Trellis 任务。
- 探索实验执行科学设计需要的比较、随机种子、折次和重复，不因软件式通过条件否定科学结果。
- 外部数据在进入项目时检查一次；只有具体故障会改变结果或下一步时才增加检查。
- 科学写作按发现、证据、解释组织，Methods 保留复现所需的技术细节，不编造指标、版本、引用或机制。
- 复用现有代码和依赖；变体放入配置或运行记录。替换代码经检查后删除旧实现，Git 历史保留旧版本。
- Sub-agent 是可选工具，不是 Workflow 的必经步骤。

## 检查安装结果

以下命令只读取配置和 Workflow：

```sh
trellis --version
grep -n 'default_workflow' .trellis/config.yaml
python3 .trellis/scripts/get_context.py --mode phase --step 2.2
git status --short
```

预期 Trellis 版本为 `0.7.0-beta.3`，默认 Workflow 为 `research`，Phase 2.2 能输出按任务类型区分的检查规则。提交前检查 `git diff`，确认没有项目代码、实验结果或无法解释的删除项。
