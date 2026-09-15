# API references

Every endpoint below is generated from the specification that declares it. Each one has its own page with the headers, the body and a request you can send.

This page lists every module, including any that the role you have chosen does not use. The sidebar shows only yours.

In M2 and M3 a call is acknowledged now and answered later. The answer arrives as a callback, a POST from ABDM to the URL you registered, declared in the specification as a webhook. Each callback is shown on the call it belongs to, and has a page of its own under that module.

A page carries a Mandatory or Conditional badge where a certification case names that call, with the case ids beside it. No badge means no published certification requirement for that module, which is not the same as optional.

## Gateway session

11 endpoints across 4 use cases: Session and tokens, Gateway & Bridge, Bridge, Provider directory. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-gateway)

## M1 ABHA identity

44 endpoints across 14 use cases: ABHA creation, ABHA verification, Share patient profile, Profile update, ABHA QR code, Session and tokens, Fetch ABHA by mobile number, Fetch ABHA by Aadhaar number, Authentication, Login & Verification, ABHA Profile, PHR & ABHA Address, Gateway & Bridge, Scan & Share. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m1)

## M2 Linking and sharing

20 endpoints across 5 use cases: Hip linking, Deep linking, User linking, Data transfer, Webhooks. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m2)

## M3 Consent and fetching

14 endpoints across 3 use cases: Consent, Data retrieval, Webhooks. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m3)

## M4 HPR and HFR

2 endpoints across 2 use cases: HPR login, HFR master data. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m4)

## P1 PHR identity and profile

63 endpoints across 6 use cases: Login, Family\_management, Global\_collection, Profile, Registration, Digilocker\_apis. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p1)

## P2 PHR linking and records

49 endpoints across 4 use cases: Care\_context\_link, Health\_locker, Scan\_and\_share, User\_initiated\_linking. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p2)

## P3 PHR consent and notifications

35 endpoints across 2 use cases: Consent\_management, Notification\_collection. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p3)

## PHR application services

61 endpoints across 7 use cases: Ambulance, Blood\_bank, Nearby\_health\_search, Pmjay\_panel\_facility\_discovery, Teleconsulting, Nhcx, Scan\_and\_pay. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-phr-services)

## Callbacks with no documented trigger

3 callbacks are declared at module level with no call named against them. Which call produces each one is not documented, so this page does not say.

| Module                  | Method | Arrives at                                                                                               | What it carries                                                                   |
| ----------------------- | ------ | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| M2 Linking and sharing  | POST   | [`/api-hiu/data/notification`](/docs/hiecm/v3/api/m2/endpoints/m2-on-data-notification)                  | The provider pushes encrypted health information to the URL named in the request. |
| M3 Consent and fetching | POST   | [`/api/v3/consent/request/hip/notify`](/docs/hiecm/v3/api/m3/endpoints/m3-on-consent-request-notify-hip) | The patient's decision, sent to the record holder                                 |
| M3 Consent and fetching | POST   | [`/health-information/transfer`](/docs/hiecm/v3/api/m3/endpoints/m3-on-health-information-transfer)      | The encrypted health data itself, pushed to the URL you supplied                  |
