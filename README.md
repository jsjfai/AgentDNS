<p align='center'>
<img src='./resources/icon.png' width="150" height="150" alt="AgentDNS Icon" />
</p>

# AgentDNS

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**AgentDNS** is the core component of [AgentWeb](https://github.com/jsjfai/agentweb/blob/main/README.md) that facilitates agent registration and discovery, enabling large language models (LLMs) to browse the internet freely, just like humans.

---

## 🌐 Overview
**AgentDNS** is an AI Agent management platform developed by [JSJF AILab](https://www.jsjfsz.com/), designed as the foundational infrastructure for AI ecosystems. It offers a unified registry for **AI agents** (supporting registration, metadata tagging, and versioning) and enables real-time discovery of specialized agent networks. By connecting large language models (LLMs) with agents worldwide, AgentDNS removes manual integration barriers, allowing LLMs to dynamically access web-scale capabilities.

---

## ✨ Key Features
- **DNSNode Registration**  
  Onboard agents with structured metadata (capabilities, endpoints, trust scores) via CLI/API.
- **Intelligent Discovery**  
  Query agents using natural language or semantic filters (e.g., "Find sentiment analysis agents with <100ms latency").
- **LLM Integration**  
  Plug-and-play compatibility with major LLM frameworks (LangChain, AutoGen) for autonomous agent orchestration.

---

## 🚀 Quick Start

### 1. Download Client
```
https://github.com/jsjfai/AgentDNS-CLI-client
or
https://github.com/jsjfai/AgentDNS-client
```

### 2. List all categories
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

### 3. Query category
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

### 4. Add category
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

### 5. Delete category
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

### 6. Register an user
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

## 📚 Documentation
- [Full API Reference](https://docs.agentdns.jsjf.ai)
- [Agent Integration Guide](https://docs.agentdns.jsjf.ai/guides/integration)
- [LLM Orchestration Patterns](https://docs.agentdns.jsjf.ai/guides/llm-orchestration)

---

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built with ❤️ by [JSJF Company](https://www.jsjfsz.com/) — Powering the next generation of AI agent network.*  
[![JSJF](https://www.jsjfsz.com/favicon.png)](https://www.jsjfsz.com/)
