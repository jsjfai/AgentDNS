from zoneinfo import ZoneInfo

TARGET_TIMEZONE = ZoneInfo('Asia/Shanghai')

NODE_MAPPING = {
    'node1': 'http://firstweb-service.agent-dns.svc.cluster.local:3000',
    'node2': 'http://secondweb-service.agent-dns.svc.cluster.local:3000',
    'node3': 'http://thirdweb-service.agent-dns.svc.cluster.local:3000',
}

EXTERNAL_PREFIXES = [
    'https://aitest.jsjfsz.com:8300',
    'https://ai.jsjfsz.com:8302',
]

NODE_PATHS = ['/agentdns/node1', '/agentdns/node2', '/agentdns/node3']


def _resolve_internal_baseurl(category_baseurl: str) -> str:
    for prefix in EXTERNAL_PREFIXES:
        for node_path in NODE_PATHS:
            if category_baseurl.startswith(f'{prefix}{node_path}'):
                node_name = node_path.rsplit('/', 1)[-1]
                return category_baseurl.replace(prefix, NODE_MAPPING[node_name])
    return category_baseurl


def get_metric_baseurl(category_baseurl: str) -> str:
    return _resolve_internal_baseurl(category_baseurl)


def get_api_baseurl(category_baseurl: str) -> str:
    api_baseurl = _resolve_internal_baseurl(category_baseurl)
    if api_baseurl.endswith('/mcp/$smart'):
        api_baseurl = api_baseurl.replace('/mcp/$smart', '')
    return api_baseurl
