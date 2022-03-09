#!/usr/bin/env python

import os
import sys
import json

import yaml
import conda.cli.python_api as conda_api

TMP_CONDA_PREFIX = '_conda/'


# SO: https://stackoverflow.com/a/39681672
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def check_and_add_plugin_cache(id_, version, cached_plugins):
    existing_version = cached_plugins.get(id_)
    if existing_version is not None and existing_version != version:
        raise Exception(f"Plugin {repr(id_)} has multiple requested versions:"
                        f" {repr(version)} and {repr(existing_version)}")
    cached_plugins[id_] = version


def check_and_add_distro_cache(name, cached_distros):
    if name in cached_distros:
        raise Exception(f"Distro named {repr(name)} is already defined.")
    cached_distros.add(name)


def setup_env(package, channel, version):
    env_name = f'{package}@{version}'
    env_prefix = os.path.join(TMP_CONDA_PREFIX, env_name)
    if not os.path.exists(env_prefix):
        print(f"CONDA CREATE: {env_prefix}", flush=True)
        conda_api.run_command(conda_api.Commands.CREATE, [
            '-p', env_prefix, '-c', 'conda-forge', '-c', 'bioconda',
            '-c', channel, f'{package}={version}'])
    else:
        print(f"CONDA USING: {env_prefix}", flush=True)

    def run(shell):
        print(f"RUNNING: {shell}", flush=True)
        stdout, stderr, exit = conda_api.run_command(
            conda_api.Commands.RUN, ['-p', env_prefix, *shell])
        if exit != 0:
            raise Exception(f"Non-zero exit code: {exit}")
        return stdout, stderr

    return run


def render_distro(distro_definition, depends, collections_dir):
    print(f"DISTRO RENDER: {distro_definition['name']}", flush=True)

    categories = set()
    for s in depends:
        categories.update(s['categories'])

    name = f"suite_qiime2dist_{distro_definition['name']}"
    shed = {
        'owner': 'qiime2',
        'categories': list(categories),
        'suite': {
            'name': name,
            'description': distro_definition['description'],
            'include_repositories': [
                dict(name=s['suite']['name'], owner=s['owner'])
                for s in depends]
        }
    }

    suite_dir = os.path.join(collections_dir, name)
    os.makedirs(suite_dir, exist_ok=True)
    with open(os.path.join(suite_dir, '.shed.yml'), 'w') as fh:
        fh.write(yaml.dump(shed, default_flow_style=False, sort_keys=False,
                           Dumper=Dumper))

    print(shed, flush=True)


def render_plugin(plugin, distro_definition, cached_plugins, tools_dir):
    id_ = plugin['id']
    package = plugin.get('package', distro_definition['default_package'])
    channel = plugin.get('channel', distro_definition['default_channel'])
    version = plugin.get('version', distro_definition['default_version'])
    cats = plugin.get('categories', distro_definition['default_categories'])

    check_and_add_plugin_cache(id_, version, cached_plugins)

    env_run = setup_env(package, channel, version)

    print(f"PLUGIN RENDER: {id_}", flush=True)
    stdout, _ = env_run(['q2galaxy', 'template', 'plugin', id_, tools_dir])

    paths = [json.loads(x)['path'] for x in stdout.split('\n') if x]
    if len(paths) > 1:
        out_dir = os.path.commonpath(paths)
    else:
        suite_dir = os.path.relpath(paths[0], tools_dir).split(os.path.sep)[0]
        out_dir = os.path.join(tools_dir, suite_dir)
    categories = ','.join(cats)

    stdout, _ = env_run(["repo-utils/create-plugin-suite-yaml.py",
                         id_, categories, out_dir])

    return json.loads(stdout)


def main(distros, dest):
    cached_distros = set()
    cached_plugins = {}
    tools_dir = os.path.join(dest, 'tools')
    collections_dir = os.path.join(dest, 'tool_collections')
    os.makedirs(tools_dir, exist_ok=True)
    os.makedirs(collections_dir, exist_ok=True)

    tool_collections = []
    for distro in distros:
        check_and_add_distro_cache(distro['name'], cached_distros)

        depends = []
        for plugin in distro['plugins']:
            shed = render_plugin(plugin, distro, cached_plugins, tools_dir)
            depends.append(shed)

        tool_collections.append((distro, depends))

    for distro, depends in tool_collections:
        render_distro(distro, depends, collections_dir)

    print("DONE", flush=True)


# repo-utils/render.py distros.yaml tools/
if __name__ == '__main__':

    _, distros_yaml, dest = sys.argv
    with open(distros_yaml, 'r') as fh:
        distros = yaml.safe_load(fh)

    main(distros['distributions'], dest)
