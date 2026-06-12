# Second Brain 产品规划

> 版本：v0.2
> 日期：2026-06-12
> 输入材料：群聊记录、两篇飞书/飞书 Wiki 实践文档、Karpathy LLM Wiki、Steph Ango 的 Obsidian/File over App 文章、`garrytan/gbrain`。

## 1. 一句话定位

Second Brain 是一个面向个人和 Agent 的长期记忆系统：它把群聊、飞书文档、日记、会议、阅读材料等原始信息，持续沉淀为可被人阅读、可被 Agent 调用、可被主动体检的个人 Brain。

MVP 仍然不先做 App，而是做一个 `second-brain` skill。但 v0.2 的定位从“Markdown Wiki”升级为 **skill-first, brain-ready**：先用 Markdown 文件夹跑通价值，再按 GBrain 的经验预留结构化检索、图谱、MCP、后台 job 和权限边界。

## 2. 核心判断

### 2.1 这不是“知识库”

普通知识库的核心问题是“我存了哪些信息”；Second Brain 的核心问题是“我是谁，我经历过什么，我如何形成判断”。群聊里最重要的洞察是：Second Brain 存的不是信息，而是个人记忆、人际关系、决策轨迹和偏好。

### 2.2 不是 Search，而是 Think

搜索工具返回页面列表；Brain 应该返回带引用的综合答案，并明确告诉用户“我还不知道什么”。GBrain 的关键启发是把 `search` 和 `think` 分开：`search` 找材料，`think` 读材料、合成答案、做 gap analysis。

### 2.3 中间层本身必须有价值

RAG 的中间层通常是 chunk、embedding、索引，对人不可读；LLM Wiki/GBrain 的中间层是 Markdown 页面、双链、实体页、时间线和日志，人和 Agent 都能消费。这个中间层既是索引，也是资产。

### 2.4 Compiled Truth + Timeline 是实体页核心

新飞书 Wiki 和 GBrain 都指向同一个结构：实体页上半部分放“当前结论”，下半部分放“证据时间线”。用户问“现在怎么看”读 Compiled Truth；用户问“发生过什么”读 Timeline。这样既避免每次查询从原始材料重算，也防止结论和证据混成一团。

### 2.5 MECE ownership 决定系统寿命

600+ 笔记实践里最明显的问题是：如果没有强约束，模型会偷懒、漏人、误分、重复建页。MVP 必须从第一天就有 `RESOLVER.md` 和目录 owner 表，保证每类实体只有一个主目录、一个 owner skill、一个 filing rule。

### 2.6 主动追问是产品分水岭

Second Brain 不能只等用户查询。它要在 ingest、query、lint、daily draft 后发现孤儿节点、缺失字段、矛盾信息、陈旧页面和待补关系，并主动追问。`wiki-lint` 不是边角功能，而是产品心跳。

## 3. 目标用户与使用场景

### 3.1 第一批用户

1. AI heavy user：每天使用 Agent、飞书、群聊、Obsidian/Codex/Claude Code，有大量上下文丢在聊天和文档里。
2. 创作者/研究者：需要长期积累素材、人物、观点、案例，并反复写作或输出。
3. 创业者/产品经理：需要把会议、客户反馈、产品判断、行业材料沉淀为可复用的业务记忆。

### 3.2 高频任务

1. 从群聊记录中抽取观点、人物、资源链接、产品机会。
2. 用飞书 CLI 读取群聊中的飞书文档/Wiki 链接，并沉淀为 Wiki 页面。
3. 把“今天发生了什么”自动生成日记草稿，再由用户补充感受。
4. 回答关于自己历史记录的问题，例如“上次谁提过 llm-wiki？”、“我为什么决定不用向量库？”。
5. 会前简报：给定一个人/会议，返回这个人是谁、上次互动、开放事项、缺失信息。
6. 定期发现未解释的人名、未归档资源、断链、重复实体、陈旧判断和 schema 缺口。

## 4. MVP 范围

### 4.1 MVP 形态

做一个本地 skill，而不是完整 SaaS。目录采用“Markdown 可读 + Brain 可演进”的结构：

```text
second-brain/
├── SKILL.md
├── README.md
├── brain/
│   ├── RESOLVER.md            # 主路由决策树，任何建页前必读
│   ├── schema.md              # 页面结构、frontmatter、证据规则
│   ├── index.md               # 人和 Agent 默认读取的入口
│   ├── log.md                 # ingest/query/lint 时间线
│   ├── inbox/                 # 无法归类或快速 capture 的临时入口
│   ├── people/
│   │   ├── README.md          # people owner rule
│   │   └── .raw/              # 原始证据 sidecar
│   ├── places/
│   ├── concepts/
│   ├── projects/
│   ├── ideas/                 # 用户原始想法，默认 AI 不自动写
│   ├── diary/
│   ├── resources/
│   └── sources/
│       ├── chats/
│       ├── feishu-docs/
│       └── web/
├── memory/
│   ├── USER.md
│   ├── PREFERENCES.md
│   └── OPEN_QUESTIONS.md
├── skills/
│   ├── RESOLVER.md
│   ├── brain-query.md
│   ├── chat-ingestion.md
│   ├── feishu-doc-ingestion.md
│   ├── entity-enrichment.md
│   └── brain-lint.md
├── evals/
│   ├── routing-cases.jsonl
│   ├── lint-cases.jsonl
│   └── query-cases.jsonl
└── scripts/
    ├── extract_links.sh
    ├── fetch_feishu_doc.sh
    ├── wiki_lint.py
    └── build_fts.py
```

### 4.2 MVP 必做

1. `capture`：把任意文本/文件/链接快速放入 `brain/inbox/`，形成低摩擦入口。
2. `ingest-chat`：读取本地群聊 Markdown，抽取人物、观点、资源、产品机会，生成 Wiki 初始页面。
3. `ingest-feishu-doc`：识别飞书 `docx/wiki` 链接，用 `lark-cli docs +fetch --api-version v2` 抓取目录和关键章节，保存到 `brain/sources/feishu-docs/`。
4. `resolver`：任何新建页面前必须读取 `brain/RESOLVER.md`，按 primary subject 决定归档位置。
5. `search`：返回候选页面和证据，不做综合。
6. `think`：读取候选页面，输出带引用的综合答案和 gap analysis。
7. `lint`：检查孤儿节点、断链、schema 缺失、重复实体、引用缺失、陈旧判断和安全风险。
8. `skill-eval`：至少提供路由评测、lint 输出评测、query 引用评测三个最小数据集。
9. `daily-draft`：先做半自动版本，允许用户提供日历/消费/日程文本，生成日记草稿和待补充问题。

### 4.3 MVP 不做

1. 不做硬件录音设备。
2. 不做完整 App 和移动端。
3. 不做企业多租户、OAuth、复杂权限和远程 MCP 服务。
4. 不默认接入向量库、图数据库或 Postgres，先把 Markdown 层跑顺。
5. 不自动读取私人日历、消费、聊天记录，除非用户显式提供或授权。
6. 不让 AI 自动改写 `ideas/` 中的原始想法，只能整理进入 drafting 后的内容。
7. 不做 24/7 全自动 cron，但预留 weekly lint / daily draft 的 job 形态。

## 5. 核心工作流

### 5.1 Capture

输入：一句话、一个文件、一段群聊、一个链接。

处理步骤：

1. 原样保存到 `brain/inbox/YYYY-MM-DD-{hash}.md`。
2. 标注来源、捕获时间、信任等级、是否含敏感信息。
3. 只做轻量分类建议，不自动深度改写。
4. 下一次 `triage-inbox` 才决定进入 `people/`、`concepts/`、`projects/`、`sources/` 或保持 inbox。

### 5.2 Ingest Chat

输入：群聊导出的 Markdown 文件。

处理步骤：

1. 复制原文到 `brain/sources/chats/`，保持 read-only。
2. 读取 `brain/RESOLVER.md` 和相关目录 `README.md`。
3. 先抽 3-10 个真实样本做小样本检查，确认人物、概念、资源、事件的分类质量。
4. 批量提取参与者、时间段、资源链接、明确观点、产品机会和待验证假设。
5. 按 primary subject 生成或更新实体页。
6. 对每个人物/项目调用 `entity-enrichment` 的轻量版：补 aliases、首次出现、关系、source refs、open threads。
7. 更新 `brain/index.md`、`brain/log.md` 和 `memory/OPEN_QUESTIONS.md`。

成功标准：生成不少于 10 个有效实体页、1 个项目页、1 个资源索引页、1 份追问清单，并且抽样页面的分类准确率超过 80%。

### 5.3 Ingest Feishu Doc

输入：飞书文档/Wiki URL 或从群聊中抽取出的链接。

推荐读取策略：

```bash
lark-cli docs +fetch --api-version v2 --doc "$URL" --scope outline --max-depth 3 --detail with-ids
```

```bash
lark-cli docs +fetch --api-version v2 --doc "$URL" --doc-format markdown --scope section --start-block-id "$BLOCK_ID"
```

处理步骤：

1. 先读 outline，选关键章节，避免全量盲抓。
2. 保存原文快照到 `brain/sources/feishu-docs/{title}.md`。
3. 将可复用内容提炼进 `concepts/`、`projects/`、`resources/` 或 `skills/`。
4. 对“体系化/方法论”内容优先生成 `concept` 或 `skill`，而不是丢进 `resources`。
5. 所有提炼页保留 provenance：来源 URL、抓取时间、章节 block id。

### 5.4 Search

输入：自然语言问题。

输出：候选页面列表、片段、来源、命中原因。

实现顺序：

1. v0.1：`rg` + `brain/index.md`。
2. v0.2：SQLite FTS5，记录 page、chunk、source、updated_at。
3. v0.3：混合检索，关键词 + FTS + 可选 embedding + rerank。

`search` 不直接给结论，避免把检索和综合混在一起。

### 5.5 Think

输入：自然语言问题。

处理步骤：

1. 调用 `search` 找候选页面。
2. 深读相关实体页的 Compiled Truth 和 Timeline。
3. 必要时沿 `[[wikilink]]` 做一跳关系遍历。
4. 输出综合答案、逐条引用、置信度和 gap analysis。
5. 如果答案本身有长期价值，询问用户是否沉淀为新页面或更新既有页面。

典型输出要比搜索更像会前简报：

```text
结论：你应该把 Second Brain 的 MVP 先做成 skill，但按 brain layer 预留接口。

证据：
- 群聊记录显示 wiki-lint 和主动追问是核心差异。
- 飞书 Wiki 600+ 笔记实践显示没有模板会漏人、漏别名、漏关系。
- GBrain 把 search 和 think 分开，并把 gap analysis 作为答案的一部分。

我还不知道：
- 你是否要优先做个人日记，还是先做群聊/飞书文档 ingest。
```

### 5.6 Wiki Lint

检查项：

1. 孤儿节点：被提到但没有页面的人、地点、概念。
2. schema 缺失：人物缺别名、关系、首次出现时间；资源缺 URL、来源、摘要。
3. 断链：`[[wikilink]]` 指向不存在页面。
4. 重复实体：同一人物/概念多种叫法未合并。
5. 引用缺失：Compiled Truth 中的判断没有 source refs。
6. 矛盾信息：同一实体页中出现互相冲突的描述。
7. 陈旧内容：旧判断被新材料挑战，但未更新。
8. 路由冲突：同一实体类型被多个 skill 或目录同时拥有。
9. 安全风险：来源文本中的指令不得升级为系统规则。

Lint 的输出不是“自动修完”，而是“可回答的追问 + 可执行修复计划”：

```text
1. [追问] Aisha 是谁？她和你是什么关系？
2. [修复] `people/李昕.md` 缺 aliases 和 relationship。
3. [合并候选] `concepts/llm-wiki.md` 与 `concepts/wiki.md` 可能重复。
4. [陈旧] `projects/second-brain.md` 仍写着“不做混合检索”，但 v0.2 已改为预留。
```

### 5.7 Skill Eval

MVP 需要最小评测，不然 skill 会越写越散。

1. 路由评测：自然语言意图 -> 期望 skill。
2. 文件归档评测：输入片段 -> 期望目录/实体类型。
3. 生成质量评测：页面是否有 Compiled Truth、Timeline、source refs、open threads。
4. 查询评测：回答是否引用来源，是否给出 gap analysis。
5. Lint 评测：是否发现断链、重复实体、缺 citation、schema 缺口。

## 6. 数据模型

### 6.1 通用页面结构

每个实体页都采用两层结构：

```markdown
# {Title}

> Executive summary: 30 秒知道这个实体现在意味着什么。

## State
## Assessment
## Open Threads
## See Also

---

## Timeline

- **YYYY-MM-DD** | 发生了什么。[Source: ...]
```

上半部分是可重写的 Compiled Truth；下半部分是追加式证据时间线。

### 6.2 Person

```yaml
---
type: person
title:
aliases: []
relationship:
importance: tier1 | tier2 | tier3 | unknown
first_seen:
last_seen:
source_refs: []
confidence: low | medium | high
open_threads: []
---
```

正文建议结构：

```text
# {name}

> Executive summary

## State
## What They Believe
## What They're Building
## Relationship
## Communication Style
## Assessment
## Network
## Open Threads
## See Also

---

## Timeline
```

人物页的高价值信息不是“简历”，而是关系、互动、信念、沟通风格和开放事项。所有判断必须标注 observed / self-described / inferred，并附置信度。

### 6.3 Concept

```yaml
---
type: concept
title:
aliases: []
status: emerging | established | validated
source_refs: []
related: []
---
```

正文建议结构：

```text
# {concept}

> Executive summary

## Definition
## Why It Matters
## My Current Read
## Counterexamples / Risks
## Related

---

## Timeline
```

### 6.4 Source

```yaml
---
type: source
source_kind: chat | feishu_doc | wiki | web | diary | meeting
url:
captured_at:
trust_level: user_provided | external | generated
read_only: true
sensitive: false
---
```

### 6.5 Project

```yaml
---
type: project
status: idea | mvp | active | paused
goal:
success_metrics: []
source_refs: []
open_threads: []
---
```

### 6.6 Brain-ready 数据原语

MVP 不实现完整数据库，但 schema 要能映射到这些原语：

1. `pages`：Markdown 页面与 canonical slug。
2. `sources`：原始来源、权限、信任等级。
3. `content_chunks`：可检索切片。
4. `links`：页面之间的 typed edge。
5. `timeline_entries`：追加式事件流。
6. `facts`：带 provenance 的结构化断言。
7. `page_versions`：页面版本历史。
8. `jobs`：后台 lint、sync、enrich、daily draft 的运行状态。

## 7. 技术架构

```text
Raw Sources
  ├─ chat markdown
  ├─ Feishu docs / wiki via lark-cli
  ├─ web articles
  ├─ diary drafts
  └─ meeting / calendar text
       ↓
Capture / Ingest
  ├─ preserve raw source
  ├─ read RESOLVER.md
  ├─ sample-first extraction
  ├─ entity resolution + aliases
  ├─ update Compiled Truth
  ├─ append Timeline
  └─ update log
       ↓
Brain Layer
  ├─ Markdown + frontmatter
  ├─ MECE directories
  ├─ wikilinks + typed links
  ├─ source refs + raw sidecars
  ├─ open threads
  └─ optional SQLite FTS5
       ↓
Agent Operations
  ├─ capture
  ├─ search
  ├─ think
  ├─ enrich
  ├─ lint
  ├─ daily draft
  └─ skill eval
```

### 7.1 渐进式检索策略

1. 小于 300 页：`rg` + `index.md` + 手动深读。
2. 300-3000 页：SQLite FTS5 + chunk 表。
3. 3000 页以上：混合检索，FTS + embedding + rerank + link traversal。
4. 涉及人/项目/关系的问题：优先读实体页和 Timeline，再考虑全文检索。

### 7.2 Operation 契约

未来从 skill 变成产品时，所有能力都应收敛为统一 operation：

```text
operation = name + description + params + handler + scope + localOnly + output
```

先在 `SKILL.md` 和 scripts 中手写约束，后续再升级为 CLI/MCP 共同契约。这样可以避免“一套 CLI 语义、一套 Agent 工具语义、一套 UI 语义”互相漂移。

## 8. 产品路线图

### Phase 0：规划与种子仓库，1-2 天

1. 完成 `second-brain` skill 目录结构。
2. 写好 `brain/RESOLVER.md`、`brain/schema.md`、目录 README、实体模板。
3. 用当前群聊记录和两份飞书文档跑第一轮手工 ingest。
4. 生成第一版 `OPEN_QUESTIONS.md`。

### Phase 1：可用 MVP，1 周

1. 实现 `capture`、`ingest-chat`、`ingest-feishu-doc`。
2. 实现 `search` 和 `think` 分层。
3. 实现 `lint` 的基础检查：孤儿节点、断链、schema 缺失、重复实体、缺 citation。
4. 实现最小 eval：routing、filing、query citation、lint。
5. 用 5 个真实问题做验收：
   - Second Brain 和知识库的差别是什么？
   - 为什么 MVP 不先做完整 GBrain？
   - 群聊里有哪些值得进入路线图的 idea？
   - 朱昌宏/飞书 Wiki 资料对 MVP 最大的修正是什么？
   - 会前我需要知道某个人的哪些开放事项？

### Phase 2：日记、主动追问和维护循环，2-3 周

1. 增加 `daily-draft`，支持用户贴入日历、消费、会议摘要。
2. 增加 `weekly-lint`，输出一周记忆健康报告。
3. 增加人物和地点的增量追问。
4. 增加别名和重复实体合并流程。
5. 支持 Obsidian 打开后的图谱体验验证。

### Phase 3：从 Markdown Wiki 到 Brain Layer，1-2 个月

1. 增加 SQLite FTS5、chunk 表、source 表、timeline 表。
2. 引入可选 mixed retrieval：关键词 + FTS + embedding + rerank。
3. 做轻量本地 TUI 或 Web UI 展示 lint 队列、实体图谱、最近记忆。
4. 接入可选自动化：飞书日历、会议纪要、飞书云文档变更。
5. 支持“图片 × Wiki”的记忆可视化实验。

### Phase 4：GBrain-like 产品化，2-4 个月

1. MCP server：让 Codex、Claude Code、Cursor 等 Agent 统一访问 brain。
2. 后台 jobs：sync、lint、enrich、daily draft、weekly report。
3. 权限边界：local trusted caller 与 remote untrusted caller 分离。
4. 可选团队模式：个人 slice、source scope、最小权限查询。

## 9. 成功指标

### 9.1 MVP 激活指标

1. 从第一份群聊记录到可查询 Brain 的时间小于 10 分钟。
2. 首次 ingest 后生成不少于 10 个有效实体页。
3. 首次 lint 至少提出 5 个用户愿意回答的问题。
4. 用户能用自然语言问出 5 个问题，并获得带来源和 gap analysis 的回答。

### 9.2 留存指标

1. 7 天内用户至少主动 capture/ingest 5 次。
2. 7 天内至少回答 10 个 lint 追问。
3. 用户至少把 2 个 think 结果反向沉淀为新页面或页面更新。
4. 至少 1 次会前简报被用户认为有实际帮助。

### 9.3 质量指标

1. 查询回答来源可追溯率大于 90%。
2. Compiled Truth 中无来源判断比例持续下降。
3. 人物/概念重复实体率持续下降。
4. Lint 追问被用户判定为“有价值”的比例大于 50%。
5. 小样本 ingest 分类准确率大于 80%，再进入批量处理。

## 10. 风险与对策

### 10.1 前期投入负收益

风险：用户第一周都在建结构，价值感不足。

对策：MVP 必须自带种子模板和一键 ingest 示例；先从用户已有群聊/飞书文档生成第一批页面，让用户当天就能问问题。

### 10.2 模型偷懒和漏抽

风险：600+ 笔记实践显示，约束不足时模型会漏掉重要人物、关系和别名。

对策：sample-first；每个 ingest skill 必须有 Contract、Phases、Output Format、Anti-Patterns、Verification；批量前先抽样验收。

### 10.3 路由和归档漂移

风险：同一实体被多个目录/skill 管理，系统很快不可维护。

对策：`RESOLVER.md` + 目录 README + ownership 表；新建页面前强制读 resolver；eval 检查 MECE overlap。

### 10.4 Agent 不查 Brain

风险：Agent 凭模型内置知识回答，绕过个人记忆。

对策：在 skill 规则中明确：涉及用户历史、偏好、项目、人物、资源时必须先 `search` 或读 `brain/index.md`，再按需深读实体页。

### 10.5 自动写入污染人格

风险：AI 把自己的推论混入用户原始想法。

对策：`sources/` read-only；`ideas/` 默认只允许用户写入；AI 生成内容必须进入明确的 derivative 区域，并标注 provenance。

### 10.6 Prompt Injection

风险：外部文档或网页中包含“忽略之前指令”等恶意内容，被系统吸收为规则。

对策：所有 source 默认标记为 untrusted；来源内容只能被总结和引用，不能改变 skill/system/schema 规则；高价值写入可增加二次审查。

### 10.7 搜索/向量成本失控

风险：过早引入 embedding、rerank、图谱和后台任务，会把 MVP 拖成基础设施项目。

对策：分阶段：`rg` -> FTS5 -> mixed retrieval；每次升级必须有真实查询失败样例和 eval 提升。

### 10.8 隐私与权限

风险：日历、消费、聊天记录高度敏感。

对策：本地优先；飞书 CLI 只在用户授权后读取；写操作前确认；原始材料可选择不进 Git 或加密存储；远程调用与本地可信调用分离。

## 11. 下一步执行清单

1. 创建 `second-brain` skill 骨架。
2. 写 `brain/RESOLVER.md` 和 `brain/schema.md`。
3. 把当前群聊记录复制进 `brain/sources/chats/`。
4. 用飞书 CLI 抓取已识别的飞书文档/Wiki，保存快照。
5. 生成第一版 `brain/index.md`、`concepts/llm-wiki.md`、`concepts/wiki-lint.md`、`concepts/compiled-truth.md`、`projects/second-brain.md`。
6. 写第一版 `SKILL.md`：定义 Capture / Ingest / Search / Think / Lint / Daily Draft。
7. 建最小 eval：10 条路由样例、10 条归档样例、5 条 query 样例、5 条 lint 样例。
8. 跑一次自测：问 5 个问题，跑 1 次 lint，检查是否产生有价值追问和可引用答案。

## 12. 参考资源

1. 群聊记录：`/Users/bytedance/Downloads/second-brain-群聊记录.md`
2. 飞书文档：`https://bytedance.sg.larkoffice.com/docx/EbcSdBVrJoBvzgxPGOplMGBVgzg`
3. 飞书 Wiki：`https://bytedance.larkoffice.com/wiki/L2bJwNBVUiWLaQk68iycclP4nnb`
4. GBrain：`https://github.com/garrytan/gbrain`
5. Karpathy LLM Wiki：`https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
6. Steph Ango - How I use Obsidian：`https://stephango.com/vault`
7. Steph Ango - File over app：`https://stephango.com/file-over-app`
8. 朱昌宏 LLM Wiki HTML 版：`https://laochonger.github.io/llm-wiki/`
