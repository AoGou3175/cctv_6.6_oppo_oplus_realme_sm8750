"""Validate the seven-version reusable workflow contracts and Bash syntax.

Run with PyYAML installed: python tests/validate_workflows.py
"""
from pathlib import Path
import re
import subprocess
import os
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
assert dispatch['susfs_enable']['default'] == 'false', 'BakaSU currently forbids SUSFS builds'
assert set(parent['jobs']) == set(VERSIONS) | {'prepare', 'release'}
assert set(parent['jobs']['release']['needs']) == set(VERSIONS) | {'prepare'}
guard = next(s for s in parent['jobs']['prepare']['steps'] if s.get('id') == 'compat')
for enabled, expected in [('false', 0), ('true', 1)]:
    result = subprocess.run([str(BASH), '-s'], input=guard['run'], text=True,
                            encoding='utf-8', capture_output=True,
                            env={**os.environ, 'SUSFS_ENABLE': enabled})
    assert result.returncode == expected, (enabled, result.stderr)
assert parent['jobs']['release']['permissions']['contents'] == 'write'
files = [(WF / 'build-test_6.6_kpm.yml', parent)]
names = []
release_tags = []
for job, version in VERSIONS.items():
    call = parent['jobs'][job]
    path = ROOT / call['uses'].removeprefix('./')
    assert path.name == f'fastbuild_6.6.{version}.yml'
    child, text = load(path)
    interface = child['on']['workflow_call']
    assert set(call['with']) == set(interface['inputs']) == set(dispatch) | {'ksu_ref'}
    assert call['needs'] == 'prepare'
    assert interface['inputs']['ksu_ref']['type'] == 'string'
    assert child['on']['workflow_dispatch']['inputs']['susfs_enable']['default'] == 'false'
    for name, value in dispatch.items():
        kind = 'string' if value['type'] == 'choice' else value['type']
        assert interface['inputs'][name]['type'] == kind, (version, name)
        assert call['with'][name] == '${{ inputs.' + name + ' }}'
    assert set(interface['outputs']) >= {'ksuver', 'ak3name', 'ksu_sha'}
    for output in ('ksuver', 'ak3name', 'ksu_sha'):
        assert interface['outputs'][output]['value'] == '${{ jobs.build.outputs.' + output + ' }}'
        assert output in child['jobs']['build']['outputs']
    assert child['env']['SUB_VERSION'] == version
    assert 'github.event.inputs.' not in text, path
    assert '"bakasu"' in text and 'Baka-SU/BakaSU' in text
    templates = re.findall(r'^\s+AK3_NAME=(.*)$', text, re.M)
    assert len(templates) == 2
    assert all('${{ env.KERNEL_VERSION }}.${{ env.SUB_VERSION }}' in t for t in templates)
    names.append(f'AnyKernel3_BakaSU_35203_6.6.{version}_AoGou.zip')
    release_script = next(s['run'] for s in child['jobs']['release']['steps']
                          if s.get('id') == 'create_release')
    tag_expression = re.search(r'gh release create ("[^"\n]+")', release_script).group(1)
    for run_id in ('38188659698', '38188659699'):
        for attempt in ('1', '2', '3'):
            values = {'env.TAG_HEAD': 'OPPO-OPlus-Realme-build',
                      'env.TIME': '261012084323', 'env.KERNEL_VERSION': '6.6',
                      'env.SUB_VERSION': version, 'github.run_id': run_id,
                      'github.run_attempt': attempt}
            expression = re.sub(r'\$\{\{\s*(.*?)\s*\}\}',
                                lambda m: values[m.group(1)], tag_expression)
            result = subprocess.run([str(BASH), '-s'],
                                    input="printf '%s' " + expression, text=True,
                                    encoding='utf-8', capture_output=True)
            assert result.returncode == 0, result.stderr
            release_tags.append(result.stdout)
    files.append((path, child))
assert len(set(names)) == 7
assert len(set(release_tags)) == 42, 'Release tags collide across versions, runs or retries in the same second'
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
print(f'PASS: 7 versions (including 89_mtk), input/output contracts, unique ZIP names, 42 unique Release tags, {count} Bash steps')
