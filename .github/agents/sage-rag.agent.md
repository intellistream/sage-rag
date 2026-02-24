---
name: sage-rag
description: Agent for RAG components (loaders/chunkers/retrievers/rerankers/pipelines) in isage-rag.
argument-hint: Provide target component/API, expected behavior, and validation scope.
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo', 'vscode.mermaid-chat-features/renderMermaidDiagram', 'github.vscode-pull-request-github/issue_fetch', 'github.vscode-pull-request-github/suggest-fix', 'github.vscode-pull-request-github/searchSyntax', 'github.vscode-pull-request-github/doSearch', 'github.vscode-pull-request-github/renderIssues', 'github.vscode-pull-request-github/activePullRequest', 'github.vscode-pull-request-github/openPullRequest', 'ms-azuretools.vscode-containers/containerToolsConfig', 'ms-python.python/getPythonEnvironmentInfo', 'ms-python.python/getPythonExecutableCommand', 'ms-python.python/installPythonPackage', 'ms-python.python/configurePythonEnvironment', 'ms-toolsai.jupyter/configureNotebook', 'ms-toolsai.jupyter/listNotebookPackages', 'ms-toolsai.jupyter/installNotebookPackages', 'ms-vscode.cpp-devtools/Build_CMakeTools', 'ms-vscode.cpp-devtools/RunCtest_CMakeTools', 'ms-vscode.cpp-devtools/ListBuildTargets_CMakeTools', 'ms-vscode.cpp-devtools/ListTests_CMakeTools']
---

# SAGE RAG Agent

## Scope
- `src/sage_libs/sage_rag/` and `tests/`.

## Rules
- Keep package lightweight and modular.
- Do not create new local virtual environments (`venv`/`.venv`); use the existing configured Python environment.
- Preserve standalone mode and optional SAGE integration.
- Maintain typed public APIs and clear docs/examples.
- Keep registration/export flow coherent (`_register.py`, `__init__.py`).
- Avoid silent fallback behavior.

## Workflow
1. Implement minimal component-level change.
2. Update tests and docs examples accordingly.
3. Validate with focused tests first.
