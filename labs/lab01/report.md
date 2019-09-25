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

~~~
$ traceroute  www.ucla.edu
traceroute to www.ucla.edu (164.67.228.152), 30 hops max, 60 byte packets
 1  * * *
 2  ufw1-ae-1-3161.gw.unsw.edu.au (149.171.253.92)  4.964 ms  5.447 ms  5.431 ms
 3  libwdr1-vl-3090.gw.unsw.edu.au (149.171.253.66)  5.892 ms  5.876 ms  5.851 ms
 4  ombcr1-te-4-5.gw.unsw.edu.au (149.171.255.77)  5.322 ms  5.298 ms  5.771 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  6.152 ms  6.412 ms  7.261 ms
 6  138.44.5.0 (138.44.5.0)  7.958 ms  4.540 ms  4.218 ms
 7  et-1-3-0.pe1.sxt.bkvl.nsw.aarnet.net.au (113.197.15.149)  4.690 ms  4.929 ms  4.934 ms
 8  et-0-0-0.pe1.a.hnl.aarnet.net.au (113.197.15.99)  98.432 ms  98.435 ms  98.416 ms
 9  et-2-1-0.bdr1.a.sea.aarnet.net.au (113.197.15.201)  149.561 ms  149.924 ms  150.155 ms
10  cenichpr-1-is-jmb-778.snvaca.pacificwave.net (207.231.245.129)  164.874 ms  165.335 ms  164.449 ms
11  hpr-lax-hpr3--svl-hpr3-100ge.cenic.net (137.164.25.73)  161.460 ms  160.750 ms  161.272 ms
12  * * *
13  bd11f1.anderson--cr00f2.csb1.ucla.net (169.232.4.4)  163.108 ms bd11f1.anderson--cr001.anderson.ucla.net (169.232.4.6)  161.874 ms  162.081 ms
14  cr00f1.anderson--dr00f2.csb1.ucla.net (169.232.4.55)  162.060 ms cr00f2.csb1--dr00f2.csb1.ucla.net (169.232.4.53)  161.205 ms cr00f1.anderson--dr00f2.csb1.ucla.net (169.232.4.55)  161.657 ms
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
~~~

~~~
$ traceroute www.u-tokyo.ac.jp 
traceroute to www.u-tokyo.ac.jp (210.152.243.234), 30 hops max, 60 byte packets
 1  * * *
 2  ufw1-ae-1-3161.gw.unsw.edu.au (149.171.253.92)  3.282 ms  3.593 ms  4.190 ms
 3  libwdr1-vl-3090.gw.unsw.edu.au (149.171.253.66)  4.185 ms  5.059 ms  5.042 ms
 4  libcr1-te-4-5.gw.unsw.edu.au (149.171.255.89)  5.021 ms  4.999 ms  6.003 ms
 5  unswbr1-te-1-9.gw.unsw.edu.au (149.171.255.101)  8.076 ms  8.073 ms  8.053 ms
 6  138.44.5.0 (138.44.5.0)  8.024 ms  4.902 ms  4.965 ms
 7  et-0-3-0.pe1.bkvl.nsw.aarnet.net.au (113.197.15.147)  6.065 ms  6.046 ms  7.524 ms
 8  ge-4_0_0.bb1.a.pao.aarnet.net.au (202.158.194.177)  160.449 ms  160.656 ms  161.040 ms
 9  paloalto0.iij.net (198.32.176.24)  163.669 ms  161.576 ms  161.267 ms
10  osk004bb01.IIJ.Net (58.138.88.189)  274.921 ms osk004bb00.IIJ.Net (58.138.88.185)  292.663 ms  293.366 ms
11  osk004ip57.IIJ.Net (58.138.106.162)  283.762 ms  282.162 ms osk004ip57.IIJ.Net (58.138.106.166)  273.652 ms
12  210.130.135.130 (210.130.135.130)  280.697 ms  280.163 ms  280.403 ms
13  124.83.228.58 (124.83.228.58)  300.389 ms  288.673 ms  280.064 ms
14  124.83.252.178 (124.83.252.178)  286.619 ms  295.013 ms  286.261 ms
15  158.205.134.26 (158.205.134.26)  286.515 ms  300.119 ms  277.247 ms
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
~~~

~~~
$ traceroute www.lancaster.ac.uk 
traceroute to www.lancaster.ac.uk (148.88.65.80), 30 hops max, 60 byte packets
 1  * * *
 2  ufw1-ae-1-3161.gw.unsw.edu.au (149.171.253.92)  1.740 ms  1.731 ms  1.703 ms
 3  libwdr1-vl-3090.gw.unsw.edu.au (149.171.253.66)  1.977 ms  1.957 ms  1.926 ms
 4  ombcr1-te-4-5.gw.unsw.edu.au (149.171.255.77)  2.822 ms  2.810 ms  2.780 ms
 5  unswbr1-te-2-13.gw.unsw.edu.au (149.171.255.105)  2.733 ms  2.718 ms  2.675 ms
 6  138.44.5.0 (138.44.5.0)  2.648 ms  2.645 ms  2.824 ms
 7  et-2-0-5.bdr1.sing.sin.aarnet.net.au (113.197.15.233)  94.365 ms  94.050 ms  94.138 ms
 8  138.44.226.7 (138.44.226.7)  314.685 ms  313.786 ms  313.912 ms
 9  janet-gw.mx1.lon.uk.geant.net (62.40.124.198)  314.055 ms  314.525 ms  314.235 ms
10  ae29.londpg-sbr2.ja.net (146.97.33.2)  315.127 ms  314.719 ms  314.069 ms
11  ae31.erdiss-sbr2.ja.net (146.97.33.22)  314.205 ms  288.911 ms  289.007 ms
12  ae29.manckh-sbr2.ja.net (146.97.33.42)  289.228 ms  269.932 ms  263.717 ms
13  ae24.lanclu-rbr1.ja.net (146.97.38.58)  269.818 ms  295.547 ms  295.590 ms
14  lancaster-university.ja.net (194.81.46.2)  309.516 ms  309.608 ms  309.816 ms
15  is-border01.bfw01.rtr.lancs.ac.uk (148.88.253.202)  308.808 ms  308.817 ms  308.771 ms
16  bfw01.iss-servers.is-core01.rtr.lancs.ac.uk (148.88.250.98)  308.774 ms  308.918 ms  308.944 ms
17  * * *
18  www.lancs.ac.uk (148.88.65.80)  303.117 ms !X  303.060 ms !X  303.029 ms !X
~~~

# Question 4
