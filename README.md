# Solution for Summer of Bitcoin Code Challenge
## problem statement
### Given an pool of transactions which consists of
 - tx_id of that transaction
 - fee to the miner
 - weight of the transaction
 - parents which consists of list of parent tx_ids


### select the transactions that gives the maximum possible fee to the miner <br /> such that total weight of a transaction doesn't exceed maximum limit = 4,000,000 <br/> and the order in which tx_ids should apper after their parent_ids are appered

## My Solution Approach:
- Take the input from csv file and convert that data into python data  structures
- I have choosen dictionary to hold the enter data and a list of tx_ids which is used for sorting based on the condition
- Dictionary holds the key as tx_id and value as dictionary of fee,weight,parents, which looks something like below
```
  data =
         { "tx_id" :
            {
                 "fee" :<int-value> ,
                      "weight" : <int-value>,
                      "parents" : list of parent tx_ids
             }
          }
```
- Greedily select those tx_ids which gives maximum fee with minimum weight
- Sort the tx_id list based on the above condition
- While taking a tx_id, along with it's fee parent tx_id fee and weight are also added and parent tx_id should be placed before child tx_ids
- So stack like data structure is used to push parent tx_ids into final answer before child tx_id

## for running the project
 - Enter a file name (default = mempool.csv)
 - ``` python main.py ```
 - clear the block.txt file if present already