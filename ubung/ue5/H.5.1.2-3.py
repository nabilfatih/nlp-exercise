def substitution_cost(a, b):
    return 0 if a == b else 1

def edit_distance_and_alignment(ref, hyp):
    len_a = len(ref)
    len_b = len(hyp)
    D = [[{'cost': 0, 'pre_i': 0, 'pre_j': 0} for _ in range(len_b +1)] for _ in range(len_a +1)]

    # Initialize first row and column
    for j in range(1, len_b +1):
        D[0][j] = {'cost': D[0][j-1]['cost'] +1, 'pre_i': 0, 'pre_j': j-1}
    for i in range(1, len_a +1):
        D[i][0] = {'cost': D[i-1][0]['cost'] +1, 'pre_i': i-1, 'pre_j': 0}

    # Fill the matrix
    for i in range(1, len_a +1):
        for j in range(1, len_b +1):
            del_cost = D[i][j-1]['cost'] +1
            ins_cost = D[i-1][j]['cost'] +1
            sub_cost = D[i-1][j-1]['cost'] +substitution_cost(ref[i-1], hyp[j-1])

            # Find minimum cost
            if del_cost <= ins_cost and del_cost <= sub_cost:
                D[i][j] = {'cost': del_cost, 'pre_i': i, 'pre_j': j-1}
            elif ins_cost <= sub_cost:
                D[i][j] = {'cost': ins_cost, 'pre_i': i-1, 'pre_j': j}
            else:
                D[i][j] = {'cost': sub_cost, 'pre_i': i-1, 'pre_j': j-1}

    # Traceback
    alignment = []
    i, j = len_a, len_b
    while i > 0 or j > 0:
        h = D[i][j]
        if h['pre_i'] == i-1 and h['pre_j'] == j:
            alignment.append((ref[h['pre_i']], None))
        elif h['pre_i'] == i and h['pre_j'] == j-1:
            alignment.append((None, hyp[h['pre_j']]))
        elif h['pre_i'] == i-1 and h['pre_j'] == j-1:
            alignment.append((ref[h['pre_i']], hyp[h['pre_j']]))
        i, j = h['pre_i'], h['pre_j']
    alignment.reverse()

    return alignment, D[len_a][len_b]['cost']

# Example usage
ref = "regensburg"
hyp = "regNsbU6k"
alignment, distance = edit_distance_and_alignment(ref, hyp)

# Compute Phoneme Error Rate (PER)
total_phonemes = len(ref)  # Total phonemes in the reference
phoneme_error_rate = distance / total_phonemes

# Output results
print("Alignment:", alignment)
print("Edit Distance:", distance)
print("Phoneme Error Rate (PER):", phoneme_error_rate * 100, "%")


"""
Output:
Alignment: [('r', 'r'), ('e', 'e'), ('g', 'g'), ('e', 'N'), ('n', None), ('s', 's'), ('b', 'b'), ('u', 'U'), ('r', '6'), ('g', 'k')]
Edit Distance: 5
Phoneme Error Rate (PER): 50.0 %
"""