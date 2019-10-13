Lab03 Report - z5117408

# Exercise 3

### Q1
* 150.203.161.98, it was a request for an address record ('A' record query type)

### Q2
* rproxy.cecs.anu.edu.au. is the CNAME given. If they need to change the underlying IP address then they need only do it for this one address. All other CNAMES will still resolve down to this one address and wont need to be changed. 

### Q3
~~~
$ dig www.cecs.anu.edu.au

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> www.cecs.anu.edu.au
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43626
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 4, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.cecs.anu.edu.au.		IN	A

;; ANSWER SECTION:
www.cecs.anu.edu.au.	1467	IN	CNAME	rproxy.cecs.anu.edu.au.
rproxy.cecs.anu.edu.au.	1467	IN	A	150.203.161.98

;; AUTHORITY SECTION:
edu.au.			72071	IN	NS	t.au.
edu.au.			72071	IN	NS	s.au.
edu.au.			72071	IN	NS	r.au.
edu.au.			72071	IN	NS	q.au.

;; ADDITIONAL SECTION:
q.au.			12642	IN	A	65.22.196.1
q.au.			18686	IN	AAAA	2a01:8840:be::1
r.au.			7374	IN	A	65.22.197.1
r.au.			12909	IN	AAAA	2a01:8840:bf::1
s.au.			588	IN	A	65.22.198.1
s.au.			4982	IN	AAAA	2a01:8840:c0::1
t.au.			16109	IN	A	65.22.199.1
t.au.			6950	IN	AAAA	2a01:8840:c1::1

;; Query time: 0 msec
;; SERVER: 129.94.242.2#53(129.94.242.2)
;; WHEN: Sun Oct 13 13:51:30 AEDT 2019
;; MSG SIZE  rcvd: 325
~~~
* the authority section seems to be listing the authority name servers for this request, the additional section is then showing the ipv4/v6 addresses for these name servers 

### Q4
* SERVER: 127.0.0.53#53(127.0.0.53)

### Q5
~~~
cecs.anu.edu.au.	3431	IN	NS	ns3.cecs.anu.edu.au. (ip address = 150.203.161.50)
cecs.anu.edu.au.	3431	IN	NS	ns2.cecs.anu.edu.au. (ip address = 150.203.161.36)
cecs.anu.edu.au.	3431	IN	NS	ns4.cecs.anu.edu.au. (ip address = 150.203.161.38)
~~~
* NS (name server) query for getting the nameservers, A (address) for the ip addresses 

### Q6
~~~
54.101.68.111.in-addr.arpa. 3600 IN	PTR	webserver.seecs.nust.edu.pk.
~~~
* this webserver name. The query type is PTR. 

### Q7
~~~
dig @129.94.242.33 yahoo.com MX

; <<>> DiG 9.11.3-1ubuntu1.8-Ubuntu <<>> @129.94.242.33 yahoo.com MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 6374
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	MX

;; Query time: 20 msec
;; SERVER: 129.94.242.33#53(129.94.242.33)
;; WHEN: Sun Oct 13 13:45:43 AEDT 2019
;; MSG SIZE  rcvd: 38
~~~
* the request is refused when using the CSE nameserver at home?
~~~
dig @129.94.242.33 yahoo.com MX

; <<>> DiG 9.9.5-9+deb8u18-Debian <<>> @129.94.242.33 yahoo.com MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40773
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 5, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	MX

;; ANSWER SECTION:
yahoo.com.		1111	IN	MX	1 mta7.am0.yahoodns.net.
yahoo.com.		1111	IN	MX	1 mta5.am0.yahoodns.net.
yahoo.com.		1111	IN	MX	1 mta6.am0.yahoodns.net.

;; AUTHORITY SECTION:
yahoo.com.		1094	IN	NS	ns5.yahoo.com.
yahoo.com.		1094	IN	NS	ns1.yahoo.com.
yahoo.com.		1094	IN	NS	ns4.yahoo.com.
yahoo.com.		1094	IN	NS	ns3.yahoo.com.
yahoo.com.		1094	IN	NS	ns2.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.		336007	IN	A	68.180.131.16
ns1.yahoo.com.		15639	IN	AAAA	2001:4998:130::1001
ns2.yahoo.com.		100642	IN	A	68.142.255.16
ns2.yahoo.com.		9157	IN	AAAA	2001:4998:140::1002
ns3.yahoo.com.		105	IN	A	27.123.42.42
ns3.yahoo.com.		105	IN	AAAA	2406:8600:f03f:1f8::1003
ns4.yahoo.com.		160083	IN	A	98.138.11.157
ns5.yahoo.com.		163281	IN	A	119.160.253.83

;; Query time: 1 msec
;; SERVER: 129.94.242.33#53(129.94.242.33)
;; WHEN: Sun Oct 13 13:48:54 AEDT 2019
;; MSG SIZE  rcvd: 371
~~~


### Q8

### Q9

### Q10

### Q11

# Exercise 4
* using python3
