def min_substr(arr: list):
    arr = list(map(lambda item: "E" if item == "E" else int(item), arr))
    substr = []
    i = 0
    while True:
        if i >= len(arr):
            break
        item = arr[i]
        if item == "E":
            sub_arr = arr[0:i]
            if not sub_arr:
                i += 1
                arr.remove(item)
            else:
                sub_min = min(sub_arr)
                substr.append(sub_min)
                arr.remove(sub_min)
                arr.remove(item)
                i = 0
            continue
        i += 1

    return substr


arr_str = ["E", "1", "2", "E", "3", "8", "E", "3"]
substr = min_substr(arr_str)
print(substr)
