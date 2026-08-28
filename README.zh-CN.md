# Trellis for Research 中文安装指南

[English README](README.md)

本仓库提供两类 Trellis marketplace 模板：

- spec 模板安装到 `.trellis/spec/`；
- `research` workflow 安装到 `.trellis/workflow.md`。

正常安装固定使用 `v0.4.0`，对应 Trellis CLI 0.6.16。不要在科研仓库中直接使用未固定版本的 `main`。

## 选择 spec 模板

| 模板 ID | 适用项目 | 典型内容 |
| --- | --- | --- |
| `research-core` | 非深度学习计算科研 | 统计分析、模拟、传统机器学习、数据处理、评估、论文结果整理 |
| `dl-earth-research` | 地学深度学习 | PyTorch 训练、checkpoint、ablation、地理空间数据、模型评估 |

是否使用神经网络训练代码决定模板选择。项目包含地学数据，不等于必须使用 `dl-earth-research`；以 sklearn、XGBoost、统计模型或数值模拟为主的项目使用 `research-core`。

## 安装前检查

进入目标仓库后执行：

```bash
trellis --version
git status --short --branch
```

只在 `trellis --version` 输出 `0.6.16` 时使用本指南。开始前确认当前分支或 worktree 是准备长期使用的版本，并保留已有未提交文件。

遇到以下情况时停止安装，先处理仓库状态：

- 当前目录是备份副本或不是 Git 仓库；
- 本地分支与目标分支存在尚未处理的分歧；
- 有正在执行的任务、代理进程或实验；
- `.codex`、`.claude` 或 `.agents` 的现有路径类型会阻止 Trellis 创建目录；
- `trellis update --dry-run` 显示无法确认来源的 `Modified by you` 文件。

不要删除 `.trellis/tasks/`、`.trellis/workspace/`、实验结果或项目自有 spec 来绕过冲突。

## 新仓库：同时安装 spec 和 workflow

这里的“新仓库”包括尚未存在 `.trellis/` 的已有代码仓库。不要添加 `--force`；如果仓库已经有 `AGENTS.md`、`.codex/` 或 `.claude/`，逐项审查 Trellis 的提示。

### 非深度学习科研

```bash
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --claude --codex
```

### 地学深度学习

```bash
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template dl-earth-research \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --claude --codex
```

安装完成后，在 `.trellis/config.yaml` 中显式启用 Codex inline 模式：

```yaml
codex:
  dispatch_mode: inline
```

Trellis 0.6.16 的默认值是 `auto`。不设置 `inline` 时，Codex 仍可能分派 implement/check 子代理，与本 workflow 的执行方式不一致。

`trellis init` 会记录 spec registry。配置应包含所选模板，例如：

```yaml
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0
    template: research-core
```

深度学习项目把最后一行改为 `template: dl-earth-research`。

## 老仓库：安全迁移 spec 和 workflow

这里的“老仓库”指已经存在 `.trellis/` 的项目。Trellis 0.6.16 没有一条可以无条件安全替换旧运行时、项目 spec 和自定义 workflow 的命令。迁移需要分别处理运行时/spec 与 workflow。

### 1. 只读预览

```bash
trellis update --dry-run
```

根据输出分两类处理：

- 没有 `Modified by you`：可以继续更新；
- 出现 `Modified by you`：确认每个文件的来源。无法确认时停止，不使用 `--force`。

旧 overlay 常见的冲突文件包括：

```text
.trellis/workflow.md
.trellis/agents/implement.md
.trellis/config.yaml
.claude/skills/trellis-check/SKILL.md
```

只有在文件与旧 overlay 完全一致、没有项目定制时，才可以把它当成已知迁移项。项目自己的 workflow、agent、skill 或 spec 修改必须保留并单独审查。

### 2. 确认 spec registry

在 `.trellis/config.yaml` 中设置固定版本和正确的模板类型：

```yaml
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0
    template: research-core
```

深度学习项目使用：

```yaml
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0
    template: dl-earth-research
```

如果项目原来使用了错误的模板类型，不要执行 `trellis init --overwrite`。先修改 `registry.spec.template`，再使用下一节的 `--dry-run` 和 `--create-new`。Trellis 会自动更新仍与旧 hash 一致的文件，为本地修改生成旁文件；旧模板独有的文件不会自动删除，需要逐项审查。

### 3. 更新 Trellis 运行时和 spec

修改 registry 后重新预览，因为目标 spec 已经变化：

```bash
trellis update --dry-run
```

确认新增文件、自动更新文件和冲突文件都符合预期后执行：

```bash
trellis update --create-new
```

该命令的行为是：

- 新文件直接加入；
- 未被项目修改的 Trellis 文件自动更新；
- 本地修改保留在原路径，新版本写入同名 `.new` 文件；
- `.trellis/tasks/` 和 `.trellis/workspace/` 保留。

逐个比较 `.new` 文件。不要把整个 `.trellis/` 目录替换成新版本。对于 `.trellis/config.yaml.new`，保留 0.6.16 新增的配置说明，同时恢复项目需要的 `registry.spec` 和下面的 Codex inline 设置。

旧 overlay 修改过 `.trellis/agents/implement.md` 时，让 Trellis 0.6.16 的版本恢复为受管理文件。新的 `research` workflow 不依赖自定义 implement/check agent，也不要把旧 agent 补丁复制回来。

### 4. 安装 marketplace workflow

如果上一步生成了 native `.trellis/workflow.md.new`，下面的 `--create-new` 会把该旁文件替换为 marketplace `research` workflow 的预览版本；当前 `.trellis/workflow.md` 仍然不变。

先生成旁文件，不改变当前 workflow：

```bash
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --create-new
```

比较 `.trellis/workflow.md` 与 `.trellis/workflow.md.new`。如果当前 workflow 仍与 Trellis 记录的模板 hash 一致，确认要替换后执行：

```bash
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0
```

旧 overlay 和其他 user-managed workflow 通常不再匹配模板 hash。此时命令会拒绝覆盖；只有在已审查并明确放弃旧 workflow 修改时才添加 `--force`：

```bash
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --force
```

非 native workflow 由项目管理。安装成功后，Trellis 0.6.16 会从模板 hash 管理中移除 `.trellis/workflow.md`，以后执行 `trellis update` 不会静默恢复 native workflow。

### 5. 启用 inline 并重启会话

确认 `.trellis/config.yaml` 包含：

```yaml
codex:
  dispatch_mode: inline
```

然后结束并重新启动 Codex 或 Claude 会话，使新的 workflow 状态提示生效。迁移本身属于配置和文档改动，只审查差异，不执行项目构建、训练或测试。

## 迁移后的科研执行规则

安装模板和 workflow 后，任务分为三类：

- 探索任务：一次产生研究结果的调用，同一次调用提供基本合理性观察；没有单独测试套件、自动重试或通过后的重复执行。
- 文档、归档和纯配置任务：只审查差异，不执行构建或测试。
- 持久代码：只执行用户和项目说明允许的最小相关检查，不反复执行完整测试套件。

异常或不符合预期的科学结果应记录为发现，不能自动调参将其消除。保留的科学结果仍需要记录输入、配置、代码版本、环境、输出、来源和限制。

## 常见错误

- 使用 `main` 而不是固定的 `#v0.4.0`。
- 对已有项目执行 `trellis init --overwrite`，删除项目自己的 spec。
- 重新执行旧 `research-workflow/apply.sh` 覆盖 Trellis 0.6.16 文件。该脚本已经弃用，只用于只读检查。
- 只安装 workflow，没有设置 `codex.dispatch_mode: inline`。
- 将 `.new` 文件视为已应用版本。`.new` 只是待审查旁文件。
- 把旧 `.trellis/agents/implement.md` 补丁复制回新运行时。
- 在有活动任务、分支分歧或无法解释的 `Modified by you` 文件时使用 `--force`。

## 安装结果检查

以下命令只读取配置，不执行项目代码：

```bash
trellis --version
grep -F '<!-- trellis-compatibility: 0.6.16 -->' .trellis/workflow.md
grep -A 3 '^registry:' .trellis/config.yaml
grep -A 2 '^codex:' .trellis/config.yaml
git status --short
```

预期结果：Trellis 版本为 0.6.16，workflow 含兼容性标记，registry 固定到 v0.4.0，Codex 使用 inline。`git status` 中只应出现已审查的 Trellis 迁移文件；如果出现项目代码、实验输出或无法解释的删除项，停止提交并检查来源。
