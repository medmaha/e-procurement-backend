import re


def generate_unique_id(prefix, instance_id, z=5):
    """
    Generates a unique id for a given model with the prefix argument
    * e.g. RFQ000250
    """

    zeros = ["0" for _ in range(z)]
    for _ in str(instance_id):
        try:
            zeros.pop()
        except IndexError:
            break
    return "%s%s%s" % (prefix if prefix else "", "".join(zeros), instance_id)


def revert_generated_unique_id(prefix, unique_id):
    """
    Reverts the generated unique id to its original id
    * e.g. RFQ000250 -> 250
    """
    pk = "0"
    unique_id = re.sub(r"[a-zA-z]", "", str(unique_id), 0)

    try:
        integer_i = int(unique_id)
        if len(unique_id) < 2:
            return integer_i
    except:
        return pk
    for index, s in enumerate(unique_id):
        try:
            integer_i = int(s)
            if integer_i == 0:
                continue
        except:
            continue
        return unique_id[index:]

    return pk
