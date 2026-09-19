# API references

Every endpoint below is generated from the specification that declares it. Each one has its own page with the headers, the body and a request you can send.

This page lists every module, including any that the role you have chosen does not use. The sidebar shows only yours.

In M2 and M3 a call is acknowledged now and answered later. The answer arrives as a callback, a POST from ABDM to the URL you registered, declared in the specification as a webhook. Each callback is shown on the call it belongs to, and has a page of its own under that module.

## Gateway session

11 endpoints across 2 use cases: Bridge and providers, Session and certificates. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-gateway)

## M1 ABHA identity

109 endpoints across 7 use cases: Session, tokens and certificate, ABHA creation, ABHA login, Find ABHA, Profile management, Benefit programmes, Other operations. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m1)

## M2 Linking and sharing

21 endpoints across 5 use cases: HIP initiated linking, User initiated linking, Link token, Patient share, Consent and data flow. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m2)

## M3 Consent and fetching

12 endpoints across 1 use case: Consent and data flow. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m3)

## M4 HPR and HFR

100 endpoints across 4 use cases: HPID, HFR, HRP bridge services, HPR. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-m4)

## P1 Registration and login

48 endpoints across 4 use cases: Create ABHA number, Aadhaar OTP, Create ABHA address, PHR login, PHR certificate and session token. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p1)

## P2 Management

47 endpoints across 5 use cases: PHR profile, Link ABHA number, Patient share, User initiated linking, Consent manager. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p2)

## P3 Subscription

8 endpoints across 1 use case: Subscription approval and management, PHR side. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p3)

## P4 Locker

4 endpoints across 1 use case: Locker. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-p4)

## Subscriptions

6 endpoints across 1 use case: Subscription request and notifications, HIU side. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-subscription)

## Scan and Pay

18 endpoints across 2 use cases: Scan and pay, Scan and pay details and version update. Each endpoint has its own page in the sidebar.

[Read the whole specification](/reference/hiecm-scan-and-pay)

## Callbacks with no documented trigger

3 callbacks are declared at module level with no call named against them. Which call produces each one is not documented, so this page does not say.

| Module                 | Method | Arrives at                                                                                                                                                        | What it carries                                                                                                                                                                           |
| ---------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M2 Linking and sharing | POST   | [`/api/v3/hip/patient/care-context/discover`](/docs/hiecm/v3/api/m2/endpoints/m2-abdm-user-initiated-linking-hip/01-m2-post-v3-hip-patient-care-context-discover) | This API endpoint is used to discover care contexts associated with a patient. It allows healthcare information providers (HIPs) to retrieve and manage patient care context information. |
| M2 Linking and sharing | POST   | [`/api/v3/hip/patient/share`](/docs/hiecm/v3/api/m2/endpoints/m2-abdm-patient-share-hip/01-m2-post-v3-hip-patient-share)                                          | This API will be invoked to the HIP for sharing the response of HIECM's /api/hiecm/patient-share/v3/share API                                                                             |
| Scan and Pay           | POST   | [`/v3/patient/share/open-order`](/docs/hiecm/v3/api/scan-and-pay/endpoints/scan-and-pay-abdm-scan-pay-hip/01-scan-and-pay-post-v3-patient-share-open-order)       | This is an API is called by HIU to check the status of reports.                                                                                                                           |
