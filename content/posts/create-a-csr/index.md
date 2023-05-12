---
title: "Create a CSR with SAN"
tags: ['Certificates', 'OpenSSL', 'Quick Note', 'TLS']
date: 2022-12-20T13:56:56.467033+00:00
aliases: ["/create-a-csr"]
---
Another quick note today: how to generate a CSR for a basic certificate supported by modern browsers (includes `Subject Alternative Name`).

## Config file

```toml
# example.conf
[req]
prompt = no
distinguished_name = dn
req_extensions = req_ext

[dn]
CN = example.com
O = Company Name
L = Lyon
C = FR

[req_ext]
subjectAltName = DNS: example.com, IP: 192.168.1.1
```

Of course, remember to adjust the settings according to the organization you're creating the CSR for:

* `[dn]` (distinguished name) section
* `subjectAltName` line (DNS and IP)

## Private key

```bash
openssl genrsa -out example.key 4096
```

## CSR

```bash
openssl req -new -config example.conf -key example.key -out example.csr
```
