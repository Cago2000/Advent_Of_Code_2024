page_ruling = open('page_ruling.txt', 'r')
page_ruling_list = {}
for line in page_ruling:
    X, Y = map(int, line.strip().split('|'))
    if X not in page_ruling_list:
        page_ruling_list[X] = []
    if Y not in page_ruling_list:
        page_ruling_list[Y] = []
    page_ruling_list[X].append(Y)


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
    counter = 0
    print(len(invalid_updates_list))
    for updates in invalid_updates_list:
        updates = correct_invalid_updates(updates)
        is_valid = check_updates(updates)
        if is_valid:
            counter += 1
            middle_page_sum2 += updates[int(len(updates)/2)]
    print(middle_page_sum+middle_page_sum2, counter)



def check_updates(updates):
    is_valid = True
    for i, update in enumerate(updates):
        if not set(updates[i+1:]).issubset(set(page_ruling_list[update])):
            is_valid = False
            break
    return is_valid


def correct_invalid_updates(updates):
    print(updates)
    is_valid = True
    for i, update in enumerate(updates):
        if not set(updates[i+1:]).issubset(set(page_ruling_list[update])):
            issues = [issue for issue in updates[i+1:] if issue not in page_ruling_list[update]]
            print(f'{updates[i]}, {issues}')
            cur_index = i
            for j, _ in enumerate(updates[cur_index+1:]):
                if updates[cur_index+j] in issues:
                    updates[cur_index], updates[cur_index+1+j] = updates[cur_index+1+j], updates[cur_index]
                    cur_index += 1
    print(updates)
    print()
    return updates


if __name__ == "__main__":
    main()
