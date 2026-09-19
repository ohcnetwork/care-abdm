# HIE-CM scan-and-pay build

Scaffolds an ABDM scan-and-pay integration one journey at a time. It covers open orders, patient selection and payment status between a facility and a PHR app.

## How this skill runs

Every journey below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the step matched below, decide the cheapest next action, act, and return to observe. A step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per step. Hitting the limit is an escalation: state what was observed, what was tried, and which operation page to read, then ask one question.

## Journeys

### Scan and pay, HIP side (`scan-and-pay-abdm-scan-pay-hip`)

**Act: the calls in this journey, in order**

#### 1. Check the status of reports (`scan-and-pay_post_v3_patient_share_open_order`)

Inbound to your bridge at `/v3/patient/share/open-order`. Acknowledge it and continue.

#### 2. Submit the HIE-CM to send all the open order for patient (`scan-and-pay_post_scan_gateway_v3_patient_on_share_open_order`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/on-share/open-order \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

#### 3. Receive the patient selection (`scan-and-pay_post_v3_patient_selection`)

Inbound to your bridge at `/v3/patient/selection`. Acknowledge it and continue.

#### 4. Share payment bundle alone with procedures of the patient (`scan-and-pay_post_scan_gateway_v3_patient_on_selection`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/on-selection \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

#### 5. Send the payment status to HIU (`scan-and-pay_post_scan_gateway_v3_patient_scan_pay_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "acknowledgement": {
    "status": "SUCCESS/ CANCELED/ PENDING/ FAIL/ REFUND_INITIATED/ REFUND_SUCCESS",
    "abhaAddress": "<username>@sbx",
    "transactionId": "string",
    "orderNumber": "string",
    "openOrderRequestId": "b767614f-153a-4aa3-946f-1622596f0fab",
    "paymentDate": "2025-01-20T07:47:49.102Z",
    "paymentRecipetLink": "PDF URL LINK of RECIPT"
  }
}'
```

#### 6. Receive the patient scan pay on notify (`scan-and-pay_post_v3_patient_scan_pay_on_notify`)

Inbound to your bridge at `/v3/patient/scan-pay/on-notify`. Acknowledge it and continue.

#### 7. Receive the patient scan pay order status (`scan-and-pay_post_v3_patient_scan_pay_order_status`)

Inbound to your bridge at `/v3/patient/scan-pay/order-status`. Acknowledge it and continue.

#### 8. Check the status of reports (`scan-and-pay_post_scan_gateway_v3_patient_scan_pay_on_ord_21f376`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/on-order-status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

**Exit condition (Observe until this is true)**

A 202 response. The specification gives no body for it, so read what comes back.

### Scan and pay, PHR side (`scan-and-pay-abdm-hiecm-scan-pay-phr`)

**Act: the calls in this journey, in order**

#### 1. Share patient open order (`scan-and-pay_post_scan_gateway_v3_patient_share_open_order`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/share/open-order \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "OPEN_PAYMENT_ORDER",
  "metaData": {
    "hipId": "HIP_1",
    "counterId": "123-456"
  },
  "profile": {
    "patient": {
      "abhaNumber": "91-7507-xxxx-xxxx",
      "abhaAddress": "<ABHA_ADDRESS>",
      "name": "name",
      "gender": "M",
      "dayOfBirth": "string",
      "monthOfBirth": "string",
      "yearOfBirth": "string",
      "address": {
        "line": "Address line 1",
        "district": "XXXXXXX",
        "state": "XXXXXX",
        "pincode": "XXXXXX"
      },
      "phoneNumber": "987654xxxx"
    }
  }
}'
```

#### 2. Receive the patient on-share (`scan-and-pay_post_v3_patient_on_share_open_order`)

Inbound to your bridge at `/v3/patient/on-share/open-order`. Acknowledge it and continue.

#### 3. Select the all open-order and send to HIP for a payment request detail (`scan-and-pay_post_scan_gateway_v3_patient_selection`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/selection \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

#### 4. Receive the patient on selection (`scan-and-pay_post_v3_patient_on_selection`)

Inbound to your bridge at `/v3/patient/on-selection`. Acknowledge it and continue.

#### 5. Notify patient scan pay (`scan-and-pay_post_v3_patient_scan_pay_notify`)

Inbound to your bridge at `/v3/patient/scan-pay/notify`. Acknowledge it and continue.

#### 6. Notify to HIP so that confirm that the HIU received the payment status (`scan-and-pay_post_scan_gateway_v3_patient_scan_pay_on_notify`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/on-notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '"<VALUE>"'
```

#### 7. Check the status of reports (`scan-and-pay_post_scan_gateway_v3_patient_scan_pay_order_status`)

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/order-status \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "queryStatus": {
    "orderNumber": "string",
    "abhaAddress": "<ABHA_ADDRESS>",
    "openOrderRequestId": "0d8bd16b-117c-4d07-9916-109fe3a9ab88"
  }
}'
```

#### 8. Receive the patient scan pay on order status (`scan-and-pay_post_v3_patient_scan_pay_on_order_status`)

Inbound to your bridge at `/v3/patient/scan-pay/on-order-status`. Acknowledge it and continue.

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

### Scan and pay details and version update (`scan-and-pay-utility`)

**Act: the calls in this journey, in order**

#### 1. Get the patient scan pay details (`scan-and-pay_get_scan_gateway_v3_patient_scan_pay_details`)

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/scan-gateway/v3/patient/scan-pay/details \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

#### 2. Update version to the serviceId (`scan-and-pay_patch_gateway_v3_scanpay_updateversion`)

```bash
curl --request PATCH \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/scanPay/updateVersion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "recordShareEnabled": true,
  "scanPayEnabled": true,
  "scanPayVersion": "v2",
  "serviceId": [
    "****_HIP, ***_HIU"
  ]
}'
```

**Exit condition (Observe until this is true)**

A 200 response. The specification gives no body for it, so read what comes back.

## Where the detail is

- Every operation, with its body fields and responses: /docs/hiecm/v3/api/scan-and-pay
- Error codes: /docs/hiecm/v3/api/scan-and-pay/errors
