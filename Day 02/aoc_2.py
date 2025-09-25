def check_report(report: list) -> bool:
    asc, desc = False, False
    if len(report) <= 0:
        return False
    for i in range(0, len(report)-1):
        if abs(report[i] - report[i+1]) < 1 or abs(report[i] - report[i+1]) > 3:
            return False
        if report[i] < report[i+1]:
            asc = True
        if report[i] > report[i+1]:
            desc = True
        if asc and desc:
            return False
    return True


def main():
    file = open('reports.txt', 'r')
    reports = []
    for line in file:
        reports.append(list(map(int, line.strip().split(' '))))

    unsafe_reports = []
    safe_reports_count = 0
    for report in reports:
        if check_report(report):
            safe_reports_count += 1
        else:
            unsafe_reports.append(report)
    print(f'Part I: Out of the {len(reports)} reports, {safe_reports_count} are safe! ({safe_reports_count/len(reports)})')

    for report in unsafe_reports:
        for i, _ in enumerate(report):
            report_copy = list(report)
            report_copy.pop(i)
            if check_report(report_copy):
                safe_reports_count += 1
                break
    print(f'Part II: Out of the {len(reports)} reports, {safe_reports_count} are safe! ({safe_reports_count/len(reports)})')


if __name__ == "__main__":
    main()
