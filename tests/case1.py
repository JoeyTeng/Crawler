import json
from __init__ import downloader
from __init__ import parser

configs = json.load(open('config.json', 'rb'))
parsed = []

def test(config):
    template = config['template']
    content = downloader.Downloader().get(url=config['url'], params=config['params']).content
    return parser.parse(content, template=template)

for config in configs:
    parsed.append(test(config))
