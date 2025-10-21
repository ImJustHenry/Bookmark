import random
def GetFakeUserAgent():
    fake_user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win68; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/107.0.1462.46",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4168.0 Safari/537.36 Edg/85.0.549.0",
        "Mozilla/5.0 (Win64; x64; Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.3485.81",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4442.3 Safari/537.36 Edg/91.0.4442.3",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4739.1 Safari/537.36 Edg/98.0.4739.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.4280.141",
        "Mozilla/5.0 (Windows NT 6.3: WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50",
        "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.0.0 Safari/537.36 Edg/76.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4_11) AppleWebKit/590.8 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/590.8 Edg/105.0.5749.16",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/552.7 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/552.7 Edg/105.0.2948.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/017.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_9) AppleWebKit/605.1 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/605.1 Edg/105.0.2402.38",
        "Mozilla/5.0 (Windows NT 10.0; Win94; x65) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
    ]
    return random.choice(fake_user_agents)

print(GetFakeUserAgent())
