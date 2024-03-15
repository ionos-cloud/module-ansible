The source files for this tutorial can be downloaded from its [GitHub repository](https://github.com/ionos-cloud/module-ansible/tree/master/docs/),or cloned into your current working directory using the command `git clone https://github.com/ionos-cloud/module-ansible.git` before changing into the `module-ansible/docs/tutorials/06__introducing_the_nat_gateway_and_network_load_balancer` sub-directory.

{% code title="01__create_jumpbox_and_nlb.yml" overflow="wrap" lineNumbers="true" %}
```patch
diff -ruN dist/etc/nginx/nginx.conf patched/etc/nginx/nginx.conf
--- dist/etc/nginx/nginx.conf	2023-03-14 16:19:32.000000000 +0100
+++ patched/etc/nginx/nginx.conf	2024-01-03 09:30:58.341522265 +0100
@@ -36,8 +36,14 @@
 	##
 	# Logging Settings
 	##
+        proxy_set_header X-Real-IP       $proxy_protocol_addr;
+        proxy_set_header X-Forwarded-For $proxy_protocol_addr;
 
-	access_log /var/log/nginx/access.log;
+        log_format combined_real_ip '$proxy_protocol_addr - $remote_user [$time_local] '
+                        '"$request" $status $body_bytes_sent '
+                        '"$http_referer" "$http_user_agent"';
+
+	access_log /var/log/nginx/access.log combined_real_ip;
 
 	##
 	# Gzip Settings
diff -ruN dist/etc/nginx/sites-available/default patched/etc/nginx/sites-available/default
--- dist/etc/nginx/sites-available/default	2024-01-03 09:39:08.370834184 +0100
+++ patched/etc/nginx/sites-available/default	2024-01-03 09:37:55.691237318 +0100
@@ -19,8 +19,11 @@
 # Default server configuration
 #
 server {
-	listen 80 default_server;
-	listen [::]:80 default_server;
+	listen 80 default_server proxy_protocol;
+	listen [::]:80 default_server proxy_protocol;
+
+	set_real_ip_from 192.168.8.0/24;
+	real_ip_header proxy_protocol;
 
 	# SSL configuration
 	#

```
{% endcode %}