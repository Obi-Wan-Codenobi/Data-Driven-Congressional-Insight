# Requirements
- Python3.12.*
- Make (should handle all python packages)
  
# How to run
```bash
cd server && make
```

# Process of ingesting data:
1. Query the topic
2. Expand query
3. Use BM25 for the top bills on the query
4. Perform boolean search on whether the candidate voted against or for it


# Final Release

## Testing Queries:
- ```District of Columbia```
    Most Relevant: District of Columbia Zoning Commission Home Rule Act
- ```COVID-19```
    Most Relevant: To prohibit any requirement that a member of the Armed Forces receive a vaccination against COVID-19
### Queries from People Tab
- ```Grijalva, Raul```
    Most Relevant: To authorize the President to award the Medal of Honor to Joseph M. Perez
- ```Porter, Katie```
    Most Relevant: Unhoused VOTE Act
- ```Lesko, Debie```
    Most Relevant: Protecting Our Kids Act

  
## Votes
- ```Viewed through the Results Tab```
    All Representatives will be displayed with a color association
- ```Colors```
    Green, Red, Grey, Black
- ```Meaning```
    Yay, Nay, Abstained, Not Available


### Data - folder definitions
HR (House of representives):
- EH (Enrolled House)
- IH (Introduced in House)
- PCS (Printed Copy of Substitute)

hconres (House Concurrent Resolution):
- EH (Enrolled House)
- ENR (Enrolled) - final version after both chambers approve 
- RDS (Referred to Committee) - sent to a committee for review
- IH (Introduced in House)
- RH (Reported in House)

### DownLoad the data
- https://drive.google.com/file/d/1pVIL8NFdyOED7QfzmSA2LsfQh8lIG3JK/view?usp=drive_link
- data.zip is the download
