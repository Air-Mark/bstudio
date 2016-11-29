import json


def pack(in_name, out_name):
    import gzip
    in_fp = open(in_name, 'r')
    out_fp = gzip.open('{0}.bsdesign'.format(out_name), 'wb')
    out_fp.write(in_fp.read())
    out_fp.close()
    in_fp.close()


def run():
    with open('index.html') as fp:
        html = fp.read()

    html_components = html.split('<!---->')[1:-1]

    html_components = [item.strip() for item in html_components]

    with open('components.json') as fp:
        components_attributes = json.load(fp)

    with open('all_components.json', 'r') as fp:
        all_components = json.load(fp)
        root_component = all_components['package']['component']
        json_components = root_component['children']
        for idx, child_component in enumerate(json_components):
            child_component['_html'] = html_components[idx]

    unique_components = {}

    def populate_components(in_component):
        unique_components.setdefault(in_component['class'], in_component)
        in_component['_attributes'] = components_attributes[in_component['class']]
        for c_component in in_component.get('children', []):
            populate_components(c_component)

    for component in json_components:
        populate_components(component)

    with open('all_components_processed.json', 'w') as fp:
        json.dump(json_components, fp, sort_keys=True, indent=4)

    for key, component in unique_components.items():
        component.pop('children', None)

    with open('unique_components.json', 'w') as fp:
        json.dump(unique_components, fp, sort_keys=True, indent=4)

if __name__ == '__main__':
    run()
    # pack('all_design.json', 'all1')
