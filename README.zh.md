<p align='center'>
<img src='./resources/icon.png' width="150" height="150" alt="AgentDNS Icon" />
</p>

# AgentDNS

[![许可证](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**AgentDNS** 是 [DNSNode](https://github.com/jsjfai/agentweb/blob/main/README.md) 的核心组件，它促进了智能体的注册和发现，使大型语言模型（LLMs）能够像人类一样自由地浏览互联网。

---

## 🌐 概览
**AgentDNS** 是由 [JSJF 人工智能实验室](https://www.jsjfsz.com/) 开发的 AI agents管理平台，被设计为 AI 生态系统的基础架构。它为 **AI agents** 提供了统一的注册表（支持注册、元数据标记和版本控制），并实现了 agents 网络的实时发现。通过连接全球的大型语言模型（LLMs）和 agents，AgentDNS 消除了手动集成障碍，使 LLMs 能够动态访问智能体规模网络的功能。

---

## ✨ 主要特性
- **DNSNode 注册**
  通过 CLI/API 以结构化元数据（功能、端点、信任分数）形式导入 agent。
- **智能发现**
  使用自然语言或语义过滤器查询（例如："查找延迟<100ms的情感分析 agent"）。
- **LLM 集成**
  与主要 LLM 框架（LangChain、AutoGen）即插即用兼容，实现自主 agents 编排。

---

## 🚀 快速开始

### 1. 下载客户端
```
https://github.com/jsjfai/AgentDNS-CLI-client
or
https://github.com/jsjfai/AgentDNS-client
```

### 2. 列出所有分类
```
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "category_list",
    "arguments": { }
  }
}
# If list your own categories, set "arguments": { "userid": "user@example.com", "apikey": "1234567890"}.
```

### 3. 查询分类
```
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "category_query",
    "arguments": { "category": "video_search"}
  }
}
# If query your own category, set "arguments": { "userid": "user@example.com", "apikey": "1234567890"}.
```

### 4. 添加分类
```
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "category_add",
    "arguments": { "category": "video_search", "baseurl": "https://example.com/mcp/$smart", "userid": "user@example.com", "apikey": "1234567890"}
  }
}
```

### 5. 删除分类
```
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "category_delete",
    "arguments": { "category": "video_search", "userid": "user@example.com", "apikey": "1234567890"}
  }
}
```

### 6. 注册用户
```
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "register_user",
    "arguments": { "userid": "user@example.com", "apikey": "1234567890"}
  }
}
```

---

## 📚 文档
- [完整 API 参考](https://docs.agentdns.jsjf.ai)
- [Agent 集成指南](https://docs.agentdns.jsjf.ai/guides/integration)
- [LLM 编排模式](https://docs.agentdns.jsjf.ai/guides/llm-orchestration)

---

## 🤝 贡献
我们欢迎贡献！请按照以下步骤操作：
1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m '添加一些 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

有关详细指南，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证
根据 MIT 许可证分发。有关详情，请参阅 [LICENSE](LICENSE)。

---

*由 [JSJF 公司](https://www.jsjfsz.com/) 用❤️构建 — 为下一代 AI agent网络提供动力。*
[![JSJF](https://www.jsjfsz.com/favicon.png)](https://www.jsjfsz.com/)
