# Exercise 3

### Question 1
* the status code is "200", the status phrase is "OK" 

### Question 2
* the response suggests the file was last modified at the server at time "Last-Modified: Tue, 23 Sep 2003 05:29:00 GMT". There is also a date header, "Date: Tue, 23 Sep 2003 05:29:50 GMT
", which is the time that the message originated/was generated. 

### Question 3

### Question 4
* 73 bytes of content are being returned by the HTTP server to the browser.

### Question 5
* the 73 bytes of content are;
~~~
<html>\n
Congratulations.  You've downloaded the file lab2-1.html!
<html>\n
~~~

# Exercise 4

### Question 1
* no, there is no if-modified-since line. This makes sense because it is generally not useful for the first request and is more so used only for successive requests for an already requested resource that could have possibly changed.

### Question 2
* yes, Last-Modified: Tue, 23 Sep 2003 05:35:00 GMT

### Question 3
* yes, "If-Modified-Since: Tue, 23 Sep 2003 05:35:00 GMT" and "If-None-Match: "1bfef-173-8f4ae900"". Important to note, the I-M-S value is the same as the time the resource was last modified ^ - so this is essentially saying to only re-get the resource if it is different from the one that was last received. Furthermore, the I-N-M value seems to be an E-tag (specifically the one from the previous response) and this is also used for the same purpose. Apparently comparing E-tags is more reliable than the time stamps and so this takes precedence if the server supports it.

### Question 4
* status is "304", phrase is "Not Modified". 

### Question 5

# Exercise 5
