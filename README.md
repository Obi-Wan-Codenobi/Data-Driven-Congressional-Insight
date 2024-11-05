# Requirements
- Python3.12.*
- Make (should handle all python packages)
  
# How to run
```bash
cd data_collection && make
```

# Test
input:
```
district of colombia 
```
```
covid 19 research
```

# Test
```
Covid related files:
H.R. 1346
H.R. 1376
H.R. 117
H.R. 348
H.R. 991
H.R. 301
H.R. 1621
```

# Process of ingesting data:
1. Query the topic
2. Expand query
3. Use BM25 for the top bills on the query
4. Perform boolean search on whether the candidate voted against or for it


## Testing Queries:
- District of Columbia
    Most relevant: District of Columbia Zoning Commission Home Rule Act
- COVID-19
    Most relevant: To prohibit any requirement that a member of the Armed Forces receive a vaccination against COVID-19

