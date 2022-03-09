#!/usr/bin/env python

import os
import sys
import json

import yaml
import qiime2.sdk


# SO: https://stackoverflow.com/a/39681672
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def main(plugin_id, categories, destination):
    pm = qiime2.sdk.PluginManager()
    plugin = pm.get_plugin(id=plugin_id)
    suite_name = os.path.basename(destination.rstrip("/"))

    shed = {
        'owner': 'qiime2',
        'homepage_url': plugin.website,
        'categories': categories,
        'auto_tool_repositories': {
            'name_template': '{{ tool_id }}',
            'description_template': 'Galaxy tool for QIIME 2 action:'
                                    ' "{{tool_name}}".'
        },
        'suite': {
            'name': suite_name,
            'description': f'Galaxy suite for QIIME 2 plugin: '
                           f'"qiime2 {plugin.name}".'
                           f' {plugin.short_description}',
            'long_description': plugin.description
        }
    }
    with open(os.path.join(destination, '.shed.yml'), 'w') as fh:
        fh.write(yaml.dump(shed, default_flow_style=False, sort_keys=False,
                 Dumper=Dumper))

    print(json.dumps(shed), flush=True)


if __name__ == '__main__':
    _, plugin_id, categories, destination = sys.argv
    main(plugin_id, categories.split(','), destination)
