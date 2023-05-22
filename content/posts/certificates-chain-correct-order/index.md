---
title: "Certificates chain correct order"
tags: ['Certificates', 'OpenSSL', 'Quick Note', 'TLS']
date: 2022-08-04T09:35:07.590872+00:00
aliases: ["/certificates-chain-correct-order"]
canonicalURL: "/certificates-chain-correct-order"
summary: Certificates in a chain file should start with the “final” certificate (the cert issued to you). Each following certificate should be the issuer of the previous one.
---
Making honor to the name of this blog, here's a very quick note for my future self.

Certificates in a chain file should start with the "final" certificate (the cert issued to you). Each following certificate should be the issuer of the previous one.

```plain
-----BEGIN CERTIFICATE-----
... # 0
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
... # 1
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
... # 2
-----END CERTIFICATE-----
```

```plain
$ openssl storeutl -certs -noout -text gabnotes.org.crt | grep -E "Certificate:|: Certificate|Issuer:|Subject:"
0: Certificate
Certificate:
        Issuer: C=US, O=Let's Encrypt, CN=R3
        Subject: CN=gabnotes.org
1: Certificate
Certificate:
        Issuer: C=US, O=Internet Security Research Group, CN=ISRG Root X1
        Subject: C=US, O=Let's Encrypt, CN=R3
2: Certificate
Certificate:
        Issuer: O=Digital Signature Trust Co., CN=DST Root CA X3
        Subject: C=US, O=Internet Security Research Group, CN=ISRG Root X1
```
