def compare_teams(a, b):

    # 1. Points
    if a.points != b.points:
        return a.points > b.points

    # 2. Wins
    if a.wins != b.wins:
        return a.wins > b.wins

    # 3. Score Difference
    if a.score_difference != b.score_difference:
        return a.score_difference > b.score_difference

    # 4. Alphabetical order
    return a.name.lower() < b.name.lower()


def merge_sort(teams):

    # Base case
    if len(teams) <= 1:
        return teams

    # Divide the list into two halves
    middle = len(teams) // 2

    left = teams[:middle]
    right = teams[middle:]

    # Sort both halves
    left = merge_sort(left)
    right = merge_sort(right)

    # Merge the sorted halves
    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    # Compare elements from both lists
    while i < len(left) and j < len(right):

        if compare_teams(left[i], right[j]):

            result.append(left[i])
            i += 1

        else:

            result.append(right[j])
            j += 1

    # Add remaining elements from left
    while i < len(left):

        result.append(left[i])
        i += 1

    # Add remaining elements from right
    while j < len(right):

        result.append(right[j])
        j += 1

    return result