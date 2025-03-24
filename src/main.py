import speedtest


def init() -> None:
    pass

def measure(servers, threads) -> dict:
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)

    return s.results.dict()

def parse(data: dict):
    download = data["download"]
    upload = data["upload"]
    ping = data["ping"]

    return download, upload, ping

def save(data: dict) -> None:
    down, up, ping = parse(data)

def log(data: dict) -> None:
    pass

if __name__ == "__main__":
    servers = []
    threads = None

    init()

    res = measure(servers, threads)
    save(res)
    log(res)
