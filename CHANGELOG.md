# Changelog

All notable changes to AgentDNS will be documented in this file.

## [Unreleased]

### Added
- Docker Compose support for local development
- Health check endpoint at `/health`
- GitHub Actions CI/CD pipeline
- CONTRIBUTING.md for contributor guidelines
- CHANGELOG.md

### Changed
- Externalized hardcoded credentials to environment variables
- Refactored URL mappings in config.py to use constants

### Security
- Removed hardcoded API keys and database credentials from deployment manifests

## [0.1.0] - 2025-03-01

### Added
- Initial public release
- MCP Server for agent category management (list, query, add, delete)
- REST API with proxy endpoint and metrics
- User registration with email-based userid
- PostgreSQL backend with metrics tracking
- Kubernetes deployment manifests (agentdns + nginx proxy)
- Dockerfile for containerized deployment
- Node availability monitoring via metrics cron job
