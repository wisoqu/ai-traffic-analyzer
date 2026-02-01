import re

class SSHLogParser:
    def __init__(self):
        self.rejected = []
        self.accepted = []
        self.rejected_ips = []
        self.accepted_ips = []

        self.ip_pattern = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")

    def feed(self, lines: list[str]):
        for line in lines:
            if "Failed password" in line:
                self.rejected.append(line)
                self.rejected_ips.extend(self.ip_pattern.findall(line))

            elif "Accepted password" in line:
                self.accepted.append(line)
                self.accepted_ips.extend(self.ip_pattern.findall(line))

    def result(self) -> dict:
        return {
            "rejected_events" : len(self.rejected),
            "accepted_events" : len(self.accepted),
            "rejected_ips" : list(set(self.rejected_ips)),
            "accepted_ips" : list(set(self.accepted_ips)),
        }