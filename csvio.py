import csv


def csv_read(path):
    with open(path, 'r') as f:
        data = list(csv.reader(f))

    return data


def csv_write(row_data, path):
    with open(path, 'r') as f:
        data = list(csv.reader(f))

    data.append(row_data)

    with open(path, 'w', newline='/n') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def csv_modify(row_data, ind, path):
    with open(path, 'r') as f:
        data = list(csv.reader(f))

    data[ind] = row_data

    with open(path, 'w', newline='/n') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def csv_delete(ind, path):
    with open(path, 'r') as f:
        data = list(csv.reader(f))

    data.remove(data[ind])
    for i, row in enumerate(data):
        row[0] = i

    with open(path, 'w', newline='/n') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def csv_search(name, path):
    with open(path, 'r') as f:
        data = list(csv.reader(f))

    for row in data:
        if name == row[1]:
            return row

    else:
        return False