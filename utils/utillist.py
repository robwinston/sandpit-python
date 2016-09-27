def remove_all_but_last_if_duplicated(list_to_examine):
    list_processed = []
    idx = 0
    for item in list_to_examine:
        if idx == len(list_to_examine) - 1 or item not in list_to_examine[idx+1:]:
            list_processed.append(item)
        idx += 1
    return list_processed
