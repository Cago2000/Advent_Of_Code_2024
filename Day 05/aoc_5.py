def get_page_ruling_list():
    page_ruling = open('page_ruling.txt', 'r')
    page_ruling_list = {}
    for line in page_ruling:
        X, Y = map(int, line.strip().split('|'))
        if X not in page_ruling_list:
            page_ruling_list[X] = []
        if Y not in page_ruling_list:
            page_ruling_list[Y] = []
        page_ruling_list[X].append(Y)
    return page_ruling_list


def check_updates(updates):
    is_valid = True
    for i, _ in enumerate(updates):
        if not set(updates[i+1:]).issubset(set(pr_list[updates[i]])):
            is_valid = False
            break
    return is_valid


def correct_invalid_updates(updates):
    i = 0
    while i < len(updates)-1:
        if not set(updates[i+1:]).issubset(set(pr_list[updates[i]])):
            issues = [issue for issue in updates[i+1:] if issue not in pr_list[updates[i]]]
            for issue in issues:
                j = updates.index(issue)
                updates[i], updates[j] = updates[j], updates[i]
                i = j
            i = 0
        else:
            i += 1
    return updates


pr_list = get_page_ruling_list()


def main():
    updates = open('updates.txt', 'r')
    updates_list = []
    invalid_updates_list = []
    middle_page_sum = 0
    for line in updates:
        updates_list.append(list(map(int, line.strip().split(','))))

    for updates in updates_list:
        is_valid = check_updates(updates)
        if is_valid:
            middle_page_sum += updates[int(len(updates)/2)]
        else:
            invalid_updates_list.append(updates)
    print(middle_page_sum)

    middle_page_sum2 = 0
    for i, invalid_updates in enumerate(invalid_updates_list):
        invalid_updates_list[i] = correct_invalid_updates(invalid_updates)
        middle_page_sum2 += invalid_updates[int(len(invalid_updates)/2)]
    print(middle_page_sum2)


if __name__ == "__main__":
    main()
