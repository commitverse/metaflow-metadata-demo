# Metaflow Metadata Service Request Improvements – Proof of Work

## What I Did

* Studied the GSoC idea on metadata service request improvements
* Built a Python prototype to simulate filtered and paginated metadata responses
* Tested pagination behavior using limit and offset
* Tested request-level filtering by tag and status

## What I Learned

* Why pagination is important for large metadata responses
* Why request-level filtering is more efficient than in-memory filtering
* How client-side handling must align with backend response structure
* How filtered and paginated responses reduce unnecessary payload size

## Output

* Working Python demo that supports:

  * filtering by tag
  * filtering by status
  * pagination with limit and offset
  * combined filtering and pagination

## Challenges

* Translating the GSoC problem statement into a small practical prototype
* Designing a simple response structure that reflects a paginated API
