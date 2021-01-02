### 🦀 RUST - Actix Web - r2d2_postgres - Sat Jan  2 22:00:46 GMT 2021

Pool size - max_con: 10, min_con: 1

```
Running 1m test @ http://localhost:8000/apikeys
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   292.15ms   39.54ms 664.82ms   75.79%
    Req/Sec   429.68     55.81   616.00     70.57%
  102456 requests in 1.00m, 7.33MB read
  Socket errors: connect 0, read 631, write 0, timeout 0
Requests/sec:   1705.17
Transfer/sec:    124.89KB
```
---
### Python - psycopg2 - Sat Jan  2 22:01:51 GMT 2021

Pool size - max_con: 10, min_con: 1

```
Running 1m test @ http://localhost:8000/apikeys
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.81s   185.12ms   2.00s    90.52%
    Req/Sec    65.88     24.98   170.00     69.13%
  15235 requests in 1.00m, 1.54MB read
  Socket errors: connect 0, read 2613, write 8, timeout 2562
Requests/sec:    253.55
Transfer/sec:     26.25KB
```
---
### Python - Async pg - Sat Jan  2 22:03:04 GMT 2021

Pool size - max_con: 10, min_con: 1

```
Running 1m test @ http://localhost:8000/apikeys
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   632.57ms  332.14ms   2.00s    74.36%
    Req/Sec   198.69     53.02   454.00     67.50%
  47052 requests in 1.00m, 4.76MB read
  Socket errors: connect 0, read 856, write 0, timeout 271
Requests/sec:    783.85
Transfer/sec:     81.14KB
```
---
### 🦀 RUST - Actix Web - r2d2_postgres - Sat Jan  2 22:05:26 GMT 2021

Pool size - max_con: 50, min_con: 1

```
Running 1m test @ http://localhost:8000/apikeys
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   186.46ms   19.38ms 310.49ms   69.11%
    Req/Sec   673.06     89.90     1.01k    70.28%
  160644 requests in 1.00m, 11.49MB read
  Socket errors: connect 0, read 613, write 0, timeout 0
Requests/sec:   2674.78
Transfer/sec:    195.91KB
```
---
### Python - psycopg2 - Sat Jan  2 22:06:31 GMT 2021

Pool size - max_con: 50, min_con: 1

```
Running 1m test @ http://localhost:8000/apikeys
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.76s   305.61ms   2.00s    86.46%
    Req/Sec    64.87     20.08   141.00     67.79%
  15061 requests in 1.00m, 1.52MB read
  Socket errors: connect 0, read 1844, write 0, timeout 3462
Requests/sec:    250.69
Transfer/sec:     25.95KB
```
---
### Python - Async pg - Sat Jan  2 22:07:43 GMT 2021

Pool size - max_con: 50, min_con: 1

```
Running 1m test @ http://localhost:8000/apikeys
  4 threads and 500 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   556.06ms  334.07ms   2.00s    63.63%
    Req/Sec   228.99     53.47   404.00     72.09%
  54544 requests in 1.00m, 5.51MB read
  Socket errors: connect 0, read 989, write 0, timeout 167
Requests/sec:    908.24
Transfer/sec:     94.02KB
```
---
