# Authentication

Generated from the specifications. Every scheme and header below is declared in one of them.

## Gateway session

**bearerAuth**, `http` `bearer`. The access token from POST /api/hiecm/gateway/v3/sessions.

## M1 ABHA identity

**bearerAuth**, `http` `bearer`.

## M2 Linking and sharing

**bearerAuth**, `http` `bearer`.

## M3 Consent and fetching

**bearerAuth**, `http` `bearer`.

## M4 HPR and HFR

**bearerAuth**, `http` `bearer`. M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## P1 Registration and login

**bearerAuth**, `http` `bearer`. The access token from POST /api/hiecm/gateway/v3/sessions.

## P2 Management

**bearerAuth**, `http` `bearer`. The access token from POST /api/hiecm/gateway/v3/sessions.

## P3 Subscription

**bearerAuth**, `http` `bearer`.

## P4 Locker

**bearerAuth**, `http` `bearer`.

## Subscriptions

**bearerAuth**, `http` `bearer`.

## Scan and Pay

**bearerAuth**, `http` `bearer`.
