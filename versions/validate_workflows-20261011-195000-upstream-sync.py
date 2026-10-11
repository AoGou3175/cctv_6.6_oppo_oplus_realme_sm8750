"""Validate the seven-version reusable workflow contracts and Bash syntax.

Run with PyYAML installed: python tests/validate_workflows.py
"""
from pathlib import Path
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / '.github' / 'workflows'
VERSIONS = {'build_30': '30', 'build_50': '50', 'build_56': '56',
            'build_57': '57', 'build_66': '66', 'build_89': '89',
            'build_89_mtk': '89_mtk'}
BASH = Path('C:/Program Files/Git/bin/bash.exe')
if not BASH.exists():
    BASH = 'bash'

def load(path):
    text = path.read_text(encoding='utf-8')
    assert not re.search(r'^(<<<<<<<|=======|>>>>>>>)', text, re.M), path
    return yaml.load(text, Loader=yaml.BaseLoader), text

parent, _ = load(WF / 'build-test_6.6_kpm.yml')
dispatch = parent['on']['workflow_dispatch']['inputs']
assert dispatch['ksu_type']['default'] == 'bakasu', 'obsolete default KSU branch'
assert 'bakasu' in dispatch['ksu_type']['options']
assert set(parent['jobs']) == set(VERSIONS) | {'release'}
assert set(parent['jobs']['release']['needs']) == set(VERSIONS)
assert parent['jobs']['release']['permissions']['contents'] == 'write'
files = [(WF / 'build-test_6.6_kpm.yml', parent)]
names = []
for job, version in VERSIONS.items():
    call = parent['jobs'][job]
    path = ROOT / call['uses'].removeprefix('./')
    assert path.name == f'fastbuild_6.6.{version}.yml'
    child, text = load(path)
    interface = child['on']['workflow_call']
    assert set(call['with']) == set(interface['inputs']) == set(dispatch)
    for name, value in dispatch.items():
        kind = 'string' if value['type'] == 'choice' else value['type']
        assert interface['inputs'][name]['type'] == kind, (version, name)
        assert call['with'][name] == '${{ inputs.' + name + ' }}'
    assert set(interface['outputs']) >= {'ksuver', 'ak3name'}
    for output in ('ksuver', 'ak3name'):
        assert interface['outputs'][output]['value'] == '${{ jobs.build.outputs.' + output + ' }}'
        assert output in child['jobs']['build']['outputs']
    assert child['env']['SUB_VERSION'] == version
    assert 'github.event.inputs.' not in text, path
    assert '"bakasu"' in text and 'Baka-SU/BakaSU' in text
    templates = re.findall(r'^\s+AK3_NAME=(.*)$', text, re.M)
    assert len(templates) == 2
    assert all('${{ env.KERNEL_VERSION }}.${{ env.SUB_VERSION }}' in t for t in templates)
    names.append(f'AnyKernel3_BakaSU_35203_6.6.{version}_AoGou.zip')
    files.append((path, child))
assert len(set(names)) == 7
count = 0
for path, workflow in files:
    for job in workflow['jobs'].values():
        for step in job.get('steps', []):
            if 'run' not in step or step.get('shell', 'bash') != 'bash':
                continue
            script = re.sub(r'\$\{\{.*?\}\}', 'test', step['run'])
            result = subprocess.run([str(BASH), '-n'], input=script, text=True,
                                    encoding='utf-8', capture_output=True)
            assert result.returncode == 0, (path.name, step.get('name'), result.stderr)
            count += 1
print(f'PASS: 7 versions (including 89_mtk), input/output contracts, unique ZIP names, {count} Bash steps')
