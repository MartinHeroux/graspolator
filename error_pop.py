def remove_error_values(subject):
    for condition_ap in subject:
        remove_error(condition_ap)

def remove_error(condition_ap):
    actual = condition_ap[0]
    perceived = condition_ap[1]
    for i in range(len(perceived)-1,-1,-1):
        if perceived[i] == 999:
            actual.remove(perceived[i])
            perceived.remove(perceived[i])
        else:
            pass
    print(actual, perceived)




def find_error_indices(condition):
    indices = []
    actual = condition[0]
    error_indices_perceived = [i for i, x in enumerate(perceived) if x == 999]
    indices.append(error_indices_actual)
    indices.append(error_indices_perceived)
    #remove_error_by_index(condition, indices)
    print(indices)
