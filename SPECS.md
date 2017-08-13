# Overview

Messente has multiple backend services and API's that need to verify the credentials and the IP address of the request.

Authentication Service verifies user's credentials (username+password+IP) over HTTPS RESTful API.

## Configuration

Configuration files must be present in /etc/messente/authentication-api/ and you are able to configure db access credentials and log file location.

The service must be accessible only for Messente services, limited by IPv4/IPv6 address in the firewall.

## Database

The PostgreSQL database which contains API credentials for users and each user may have multiple API credentials with different IP address restrictions.

Database table definition:

```
CREATE TABLE api_users (
    id SERIAL NOT NULL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    username VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL,
    whitelisted_ips TEXT[]
);
```

Whitelisted IP addresses (IPv4/IPv6) can be regular IP address (127.0.0.1) or in CIDR notation (0.0.0.0/0).

This API should use a read-only connection to "messente" database and also resolve database connection, connection pooling, error handling (lost db connection), etc.

Messente's PostgreSQL database is accessed via Pgpool-II load-balancer.


## Request

Authentication Service accepts requests in application/json, for example:

```
{
    "service": "Verigator",
    "username": "some_user",
    "password": "some_password",
    "ip": "127.0.0.1"
}
```

## Response

Successful authentication response:

```
{
    "authenticated": true,
    "timestamp": 1489740091
}
```

In case of failed authentication, the response should just indicate that with the HTTP status code according to REST standards.


## Logging

Authentication Service logs authentication requests:
 - Timestamp
 - Name of the service the request originated from
 - Account ID (numeric)
 - Authentication result or
 - Failure reason in case authentication did not succeed (e.g. invalid password, user does not exist, database error)

## Performance

The service must handle 1000 req/sec.

# Bonus

- describe security concerns and mitigations
- propose a way to limit access to the api
- how to improve the whole setup
- extend this documentation where needed
- write systemd initscript
- write Debian package extras
