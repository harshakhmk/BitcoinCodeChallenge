from CSV_handler import MempoolTransaction
from collections import deque

MAX_WEIGHT = 4000000

def visit_parents(tx_id,transaction_data, stack):
    if transaction_data[tx_id]["parents"] == ['']:
        return
    else:
        for parent in transaction_data[tx_id]["parents"]:
            stack.appendleft(parent)
            visit_parents(parent,transaction_data,stack)
    return

# write to sample_block greedly by selecting element with max fee
# Transaction_ids is a list of tx_ids which are sorted by descreasing order of fee/weight
def run(transaction_data, transaction_ids, mempool_obj):
    stack = deque()
    result = []
    visited = {}
    weight_remaining = MAX_WEIGHT
    for tx_id in transaction_ids:
        if weight_remaining <= 0:
            break
        if tx_id in visited:
            continue

        #Get the fee, weight for including current tx_id with its parent values too
        fee, weight = mempool_obj.internal_sort_helper(tx_id)
        if  "parents" in mempool_obj.transaction_data[tx_id]["parents"]:
            result.append(tx_id)
            visited[tx_id] = True
            weight_remaining = weight_remaining - weight
            continue
        if weight_remaining < weight:
            continue

        # else add it,as it must have weight <= remaining weight and can be included
        # Also visit all of its parents
        weight_remaining = weight_remaining - weight
        visit_parents(tx_id,transaction_data,stack)
        while 0 < len(stack):
            value = stack.popleft()
            visited[value] = True
            result.append(value)

    return result

def generate_output(result):
    with open('block.txt', 'w') as f:
        for tx_id in result:
            f.write("%s\n" % tx_id)

if __name__ == "__main__":
    filename = input("Enter a filename to read the data (Optional)")
    if filename == "":
        filename = "mempool.csv"
    mempool_obj = MempoolTransaction(filename)
    mempool_obj.read_file_data()
    mempool_obj.sort_transaction_ids()
    transaction_data, transaction_ids = mempool_obj.transaction_data, mempool_obj.transaction_ids
    result = run(transaction_data, transaction_ids, mempool_obj)
    generate_output(result)

