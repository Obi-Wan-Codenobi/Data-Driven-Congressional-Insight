# System overview:
1. load all the vote data
2. load all polictians data
3. load all bills 

## Data extracted from votes
- politicians id
- vote status
- bill 

## Data extracted from politicians 
- name
- state
- party 

## Data extracted from bills
- bill text
- date 

# Process of ingesting data:
1. Query the topic
2. Expand query
3. Use BM25 for the top bills on the query
4. Classify the documents to be 'for' or 'against' the query topic
3. Perform boolean search on whether the candidate voted against or for it in relation to the nature of the bill


## Testing Queries:
- District of Columbia
    Most relevant: District of Columbia Zoning Commission Home Rule Act

