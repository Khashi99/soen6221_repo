#!/usr/bin/env python3
"""Acquire fresh pinned research input caches, or restore an existing manifest."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

FRAMEWORKS = [
    ('LlamaIndex', 'run-llama/llama_index'), ('LangChain', 'langchain-ai/langchain'),
    ('AutoGen', 'microsoft/autogen'), ('OpenAI Agents SDK', 'openai/openai-agents-python'),
    ('LangGraph', 'langchain-ai/langgraph'), ('MetaGPT', 'FoundationAgents/MetaGPT'),
    ('Semantic Kernel', 'microsoft/semantic-kernel'), ('CrewAI', 'crewAIInc/crewAI'),
    ('Haystack', 'deepset-ai/haystack'), ('smolagents', 'huggingface/smolagents'),
]
EXCLUSIONS = ['.git', '.venv', 'venv', 'env', '__pycache__', 'node_modules',
              '.mypy_cache', '.pytest_cache', '.tox', '.nox', '.eggs',
              'vendor', 'vendored', 'third_party', 'site-packages']


def acquire(framework, repository, cache, pinned=None):
    root = cache / repository.replace('/', '__')
    url = 'https://github.com/' + repository + '.git'
    env = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1', GIT_TERMINAL_PROMPT='0')
    if not root.exists():
        if pinned:
            subprocess.run(['git', 'init', '-q', str(root)], check=True, env=env)
            subprocess.run(['git', '-C', str(root), 'remote', 'add', 'origin', url], check=True, env=env)
            subprocess.run(['git', '-C', str(root), 'fetch', '-q', '--depth=1', 'origin', pinned], check=True, env=env)
            subprocess.run(['git', '-C', str(root), 'checkout', '-q', '--detach', pinned], check=True, env=env)
        else:
            subprocess.run(['git', 'clone', '-q', '--depth=1', '--single-branch', url, str(root)], check=True, env=env)
    actual_url = subprocess.check_output(['git', '-C', str(root), 'remote', 'get-url', 'origin'], text=True).strip()
    if actual_url != url:
        raise ValueError(f'Unexpected cached origin for {framework}')
    sha = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if pinned and sha != pinned:
        raise ValueError(f'Cached SHA differs from pinned manifest for {framework}; not resetting existing files.')
    if subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip():
        raise ValueError(f'Cached source changes for {framework}; not overwriting.')
    return dict(framework=framework, repository=repository, commit=sha, checkout=str(root),
                selection='fresh default branch snapshot' if not pinned else 'restored exact pinned snapshot',
                acquired_at_utc=datetime.now(timezone.utc).isoformat())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, default=Path('/workspace/satd-source-cache'))
    p.add_argument('--manifest', type=Path, default=Path('snapshots.json'))
    args = p.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    old = json.loads(args.manifest.read_text()) if args.manifest.exists() else None
    pins = {r['repository']: r['commit'] for r in old['repositories']} if old else {}
    results = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(acquire, f, repo, args.cache, pins.get(repo)): f for f, repo in FRAMEWORKS}
        for future in as_completed(futures):
            r = future.result()
            results[r['framework']] = r
            print(r['framework'], r['commit'], flush=True)
    manifest = dict(study='fresh independent study; not pilot reproduction',
                    authorization='user authorized fresh independent study',
                    docstrings='exclude', tests='include', source_files='tracked Python .py files',
                    excluded_directory_names=EXCLUSIONS,
                    repositories=[results[f] for f, _ in FRAMEWORKS])
    if not old:
        args.manifest.write_text(json.dumps(manifest, indent=2) + '\n')
    else:
        print('Verified existing pins; original manifest preserved.')


if __name__ == '__main__':
    main()
