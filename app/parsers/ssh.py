
def make_logs(lines: list[str]):


    #Analyzing block
    rejected = [el for el in lines if 'Failed password' in el]
    accepted = [el for el in lines if 'Accepted password' in el]

    # IP analyzing
    import re
    ip_pattern = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"

    # Rejected
    rejected_ips = []
    for line in rejected:
        found = re.findall(ip_pattern, line)
        rejected_ips.extend(found)

    unique_rej_ips = list(set(rejected_ips))

    # Accepted
    accepted_ips = []
    for line in accepted:
        found = re.findall(ip_pattern, line)
        accepted_ips.extend(found)

    unique_acc_ips = list(set(accepted_ips))

    return {
        "rejected_times" : len(rejected),
        "accepted_times" : len(accepted),
        "rejected_ips" : unique_rej_ips,
        "accepted_ips" : unique_acc_ips,
        "total for time" : len(lines)
    }