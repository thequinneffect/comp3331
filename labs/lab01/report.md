# z5117408 - Nicholas Quinn

# Question 1

* IP address(es) of the website www.koala.com.au : 104.18.60.21 , 104.18.61.21
* It has multiple IP addresses because it is using multiple servers (clustered servers) to balance the load better (DNS load balancing). 
* IP address 127.0.0.1 has the name "localhost". It is also referred to as the "loopback address".
* This IP address is special as it is the IP address your computer uses to refer to itself

# Question 2

| host                  | reachable (ping, web) | reason                                                           |
|-----------------------|-----------------------|------------------------------------------------------------------|
| www.unsw.edu.au       | y, y                  |                                                                  |
| www.getfittest.com.au | n, n                  | name or service not known                                        |
| www.mit.edu           | y, y                  |                                                                  |
| www.intel.com.au      | y, y                  |                                                                  |
| www.tpg.com.au        | y, y                  |                                                                  |
| www.hola.hp           | n, n                  | name or service not known (guessing it should be www.holahp.com) |
| www.amazon.com        | y, y                  |                                                                  |
| www.tsinghua.edu.cn   | y, y                  |                                                                  |
| www.kremlin.ru        | n, y                  | ping is sometimes blocked because for security (prevent DOS      |
| 8.8.8.8               | y, n                  | it is the google public DNS server (no web interface/service)    |

# Question 3

~~~
$ traceroute www.columbia.edu
traceroute to www.columbia.edu (128.59.105.24), 30 hops max, 60 byte packets
 1  * * *
 2  ufw1-ae-1-3161.gw.unsw.edu.au (149.171.253.92)  2.676 ms  7.315 ms  7.314 ms
 3  libwdr1-vl-3090.gw.unsw.edu.au (149.171.253.66)  7.919 ms  7.928 ms  7.910 ms
 4  ombcr1-te-4-5.gw.unsw.edu.au (149.171.255.77)  7.893 ms  7.805 ms  7.768 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  9.253 ms * *
 6  138.44.5.0 (138.44.5.0)  48.137 ms  45.743 ms  41.037 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  40.909 ms  40.305 ms  40.248 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  120.516 ms  121.568 ms  121.555 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  177.054 ms  175.847 ms  158.879 ms
10  abilene-1-lo-jmb-706.sttlwa.pacificwave.net (207.231.240.8)  159.852 ms  159.837 ms  159.807 ms
11  et-4-0-0.4079.rtsw.miss2.net.internet2.edu (162.252.70.0)  160.415 ms  189.410 ms  189.381 ms
12  et-4-0-0.4079.rtsw.minn.net.internet2.edu (162.252.70.58)  189.361 ms  189.342 ms  189.324 ms
13  et-1-1-5.4079.rtsw.eqch.net.internet2.edu (162.252.70.106)  190.944 ms  194.258 ms  194.689 ms
14  ae-0.4079.rtsw3.eqch.net.internet2.edu (162.252.70.163)  192.283 ms  189.605 ms  191.005 ms
15  ae-1.4079.rtsw.clev.net.internet2.edu (162.252.70.130)  199.549 ms  206.273 ms  205.475 ms
16  buf-9208-I2-CLEV.nysernet.net (199.109.11.33)  218.302 ms  205.937 ms  210.242 ms
17  syr-9208-buf-9208.nysernet.net (199.109.7.193)  215.310 ms  223.124 ms  223.134 ms
18  nyc111-9204-syr-9208.nysernet.net (199.109.7.94)  236.115 ms  229.747 ms  229.727 ms
19  nyc-9208-nyc111-9204.nysernet.net (199.109.7.165)  229.707 ms  229.704 ms  229.667 ms
20  columbia.nyc-9208.nysernet.net (199.109.4.14)  229.650 ms  229.635 ms  229.622 ms
21  cc-core-1-x-nyser32-gw-1.net.columbia.edu (128.59.255.5)  229.608 ms  229.593 ms  229.579 ms
22  cc-conc-1-x-cc-core-1.net.columbia.edu (128.59.255.21)  317.033 ms  291.332 ms  314.293 ms
23  ci.columbia.edu (128.59.105.24)  313.894 ms  313.016 ms  325.494 ms
~~~

# Question 4
