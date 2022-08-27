#!/usr/bin/env python

import sys

import lxml.etree as xml


def main(tool_fp, docker_image):
    tool = xml.parse(tool_fp)
    root = tool.getroot()

    new_reqs = xml.Element('requirements')
    container = xml.Element('container', dict(type='docker'))
    container.text = docker_image
    new_reqs.append(container)

    root.replace(root.find('requirements'), new_reqs)
    # HACK: set correct profile and hack version
    root.set('version', root.get('version') + '.2')
    root.set('profile', '22.05')

    xml.indent(tool, ' ' * 4)
    xmlbytes = xml.tostring(tool, pretty_print=True, encoding='utf-8',
                            xml_declaration=True)
    with open(tool_fp, 'wb') as fh:
        fh.write(xmlbytes)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
