from zoneinfo import ZoneInfo

# 目标时区
TARGET_TIMEZONE = ZoneInfo('Asia/Shanghai')

def get_metric_baseurl(category_baseurl: str) -> str:
    if category_baseurl.startswith('https://aitest.jsjfsz.com:8300/agentdns/node1'):
        return category_baseurl.replace('https://aitest.jsjfsz.com:8300', 'http://firstweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://aitest.jsjfsz.com:8300/agentdns/node2'):
        return category_baseurl.replace('https://aitest.jsjfsz.com:8300', 'http://secondweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://aitest.jsjfsz.com:8300/agentdns/node3'):
        return category_baseurl.replace('https://aitest.jsjfsz.com:8300', 'http://thirdweb-service.agent-dns.svc.cluster.local:3000')

    if category_baseurl.startswith('https://ai.jsjfsz.com:8302/agentdns/node1'):
        return category_baseurl.replace('https://ai.jsjfsz.com:8302', 'http://firstweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://ai.jsjfsz.com:8302/agentdns/node2'):
        return category_baseurl.replace('https://ai.jsjfsz.com:8302', 'http://secondweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://ai.jsjfsz.com:8302/agentdns/node3'):
        return category_baseurl.replace('https://ai.jsjfsz.com:8302', 'http://thirdweb-service.agent-dns.svc.cluster.local:3000')

    return category_baseurl

def get_api_baseurl(category_baseurl: str) -> str:
    api_baseurl = category_baseurl
    if category_baseurl.startswith('https://aitest.jsjfsz.com:8300/agentdns/node1'):
        api_baseurl = category_baseurl.replace('https://aitest.jsjfsz.com:8300', 'http://firstweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://aitest.jsjfsz.com:8300/agentdns/node2'):
        api_baseurl = category_baseurl.replace('https://aitest.jsjfsz.com:8300', 'http://secondweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://aitest.jsjfsz.com:8300/agentdns/node3'):
        api_baseurl = category_baseurl.replace('https://aitest.jsjfsz.com:8300', 'http://thirdweb-service.agent-dns.svc.cluster.local:3000')

    if category_baseurl.startswith('https://ai.jsjfsz.com:8302/agentdns/node1'):
        api_baseurl = category_baseurl.replace('https://ai.jsjfsz.com:8302', 'http://firstweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://ai.jsjfsz.com:8302/agentdns/node2'):
        api_baseurl = category_baseurl.replace('https://ai.jsjfsz.com:8302', 'http://secondweb-service.agent-dns.svc.cluster.local:3000')
    if category_baseurl.startswith('https://ai.jsjfsz.com:8302/agentdns/node3'):
        api_baseurl = category_baseurl.replace('https://ai.jsjfsz.com:8302', 'http://thirdweb-service.agent-dns.svc.cluster.local:3000')

    if api_baseurl.endswith('/mcp/$smart'):
        api_baseurl = api_baseurl.replace('/mcp/$smart', '')

    return api_baseurl