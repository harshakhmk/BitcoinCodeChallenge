import csv
class MempoolTransaction():
    def __init__(self, filename = "mempool.csv"):
        self.filename = filename
        self.transaction_data = {}
        self.transaction_ids = []
    def read_file_data(self):
        try:
           with open(self.filename, "r") as f:
                count  = 0
                reader = csv.reader(f)
                for row in reader:
                    if count == 0:
                        count = count + 1
                        continue
                    key = row[0]
                    self.transaction_ids.append(key)
                    self.transaction_data[key] = {}
                    self.transaction_data[key]["fee"] = int(row[1])
                    self.transaction_data[key]["weight"] = int(row[2])
                    self.transaction_data[key]["parents"] = []
                    parents_str = ''.join(row[3:])
                    parents = parents_str.split(";")
                    for parent in parents:
                        self.transaction_data[key]["parents"].append(parent)

        except Exception as exception_obj:
            print(f"Unable to read {self.filename}, due to {exception_obj}")

    def get_parent_value(self, tx_id, key):
        if self.transaction_data[tx_id]["parents"] == ['']:
           return 0

        ans = 0
        for parent in self.transaction_data[tx_id]["parents"]:
            ans = ans  + self.get_parent_value(parent) + self.transaction_data[tx_id][key]
        return ans

    def internal_sort_helper(self, tx_id):
        fee = self.transaction_data[tx_id]["fee"]
        weight = self.transaction_data[tx_id]["weight"]
        if not self.transaction_data[tx_id]["parents"]:
            fee = fee + self.get_parent_value(tx_id, "fee")
            weight = weight + self.get_parent_value(tx_id,"weight")
        return 1.0*fee, 1.0*weight

    def sort_calculator(self, tx_id):
        fee, weight = self.internal_sort_helper(tx_id)
        return fee/weight
    def sort_transaction_ids(self):
        self.transaction_ids = sorted(self.transaction_ids, key=self.sort_calculator, reverse = True)