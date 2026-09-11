# Sandbox data dictionary

The database behind the sandbox portal, the site where you register your
organisation, declare which milestones you will build and apply for sandbox
exit. Read it to find what the portal records about your application, and what
a status you see on screen is called underneath. It is the portal's own store, not an
[ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) API, so nothing here is an endpoint you can
call.

## What the source contains

Three of the portal's five record groups are listed here.

| Sheet | What it holds | On this page |
| --- | --- | --- |
| Tables | 31 tables in the `public` schema, with the owner of each. | Yes, as the sections below |
| Table Columns | 636 columns with type, nullability and a one line description. | Yes |
| Indexes | 45 indexes with their definitions. | Yes, in [Indexes](#indexes) |
| Sequences | 34 Postgres sequences. | No, see [What is not transcribed](#what-is-not-transcribed) |
| Def values | 104 column defaults. | No, see [What is not transcribed](#what-is-not-transcribed) |

## How to read these tables

Each section below is one database table. **Field** is the column name,
**Type** the Postgres type, **Nullable** `No` for a `NOT NULL` column, and
**Meaning** what it records.

- `sd_id` is the self declaration identifier and the join key across most
  tables. `id_public` is a second, public facing identifier many tables carry
  alongside the primary key.
- These names are misspelled in the schema itself and reproduced as they are:
  `messege`, `previlege`, `redy_for_testing`, `suporting_doc`,
  `integratin_phase`, `user_jorny`, `admin_coment`, `sare_date`.
- Thin descriptions, such as `flag` on `sd_exit`, are reproduced as published, not padded
  them out with a guess.

### Abbreviations used in the descriptions

| Short form | What it means |
| --- | --- |
| [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm), NDHM | The programme. NDHM is the former name and both appear in the source. |
| [PHR](/docs/hiecm/v3/getting-started/glossary#phr) | Personal health record application. |
| [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) | Health information user. |
| [UHI](/docs/hiecm/v3/getting-started/glossary#uhi) | Unified Health Interface. |
| [NHCX](/docs/hiecm/v3/getting-started/glossary#nhcx) | National Health Claims Exchange. |
| [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis) | Hospital management information system. |
| [OTP](/docs/hiecm/v3/getting-started/glossary#otp) | One time password. |
| SPOC | Single point of contact, the named person on an application. |
| [HTC](/docs/hiecm/v3/getting-started/glossary#health-tech-committee) | Health Tech Committee, the body that reviews your integration at the end of the exit process. |
| [WASA](/docs/hiecm/v3/getting-started/glossary#wasa) | The security audit that produces your Safe to Host certificate. See [Security audit](/docs/hiecm/v3/getting-started/security-audit). |
| DHIS, V3 | Platform terms used inside the sandbox portal's own records. |

## Tables at a glance

| Group | Table | What it holds |
| --- | --- | --- |
| Registration and account | [`sd_login`](#sd_login) | The main registration record for an organisation on the sandbox portal |
| Registration and account | [`password`](#password) | Password values and their timestamps, held apart from `sd_login` |
| Registration and account | [`ci_sessions`](#ci_sessions) | Web session state for a signed in portal user |
| Registration and account | [`address`](#address) | The registered address attached to a self declaration |
| Registration and account | [`active_integrator`](#active_integrator) | A short record marking an application as an active integrator |
| Self declaration and milestones | [`self_declaration`](#self_declaration) | What an organisation declared it would build, and the start and end dates it gave for each milestone |
| Self declaration and milestones | [`sd_status`](#sd_status) | The review trail for an application: administrator decision, four HTC review stages, production access status |
| Sandbox exit | [`sd_exit`](#sd_exit) | The sandbox exit application: contacts, integration details, uploaded evidence and every review stage on it |
| Sandbox exit | [`sd_exit_docs`](#sd_exit_docs) | Files uploaded with a sandbox exit application |
| Sandbox exit | [`sd_doc_type`](#sd_doc_type) | The list of document types an application may upload |
| Sandbox exit | [`wasa_dhis_initiation_details`](#wasa_dhis_initiation_details) | WASA issue and expiry dates against a client identifier and a bridge identifier |
| Gateway specific registration | [`sd_hiu`](#sd_hiu) | Client identifiers issued for HIU registrations |
| Gateway specific registration | [`sd_uhi`](#sd_uhi) | Requests to work on UHI, with the service type and the stated intent |
| Gateway specific registration | [`hcx`](#hcx) | Organisation details captured for a health claims exchange registration |
| Gateway specific registration | [`hcx_address`](#hcx_address) | The registered address for an `hcx` record |
| Gateway specific registration | [`nhcx_exit`](#nhcx_exit) | The NHCX application and its administrative review status |
| Portal administration | [`mst_role`](#mst_role) | Roles inside the portal and their landing pages |
| Portal administration | [`mst_modules`](#mst_modules) | Portal screens and menu entries |
| Portal administration | [`mst_privilege`](#mst_privilege) | Which role may reach which module |
| Audit, logs and messages | [`audit_log`](#audit_log) | Before and after values for a changed record, with who changed it |
| Audit, logs and messages | [`security_audit_trail`](#security_audit_trail) | Request level audit: endpoint, method, user agent, correlation identifier and payload |
| Audit, logs and messages | [`log`](#log) | Token generation and email dispatch events against a client |
| Audit, logs and messages | [`notification_audit`](#notification_audit) | Notifications sent, by template, recipient and delivery status |
| Audit, logs and messages | [`concern`](#concern) | Support messages raised through the portal |
| Reference data and content | [`std_data`](#std_data) | STD dialling codes, with their state, LDCA and SDCA names |
| Reference data and content | [`upcoming_session`](#upcoming_session) | Sessions listed on the portal, with joining links |
| Replication internals | [`awsdms_apply_exceptions`](#awsdms_apply_exceptions) | Exceptions raised by the portal's AWS Database Migration Service tasks |
| Backup copies | [`sd_login_bk`, `sd_login_bk_16062026`, `sd_login_bk_20012026_updt`, `sd_exit_live`](#backup-copies) | Tables that repeat the column lists of `sd_login` and `sd_exit` |

## sd_login

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `sd_id` | integer | No | Primary key and unique identifier of the self-declaration registration |
| `role_id` | smallint | Yes | Role identifier assigned to the user |
| `name` | character varying | Yes | Name of the registered user |
| `email` | character varying | Yes | Email address of the registered user |
| `mobile` | character varying | Yes | Mobile number of the registered user |
| `password` | character varying | Yes | Encrypted password of the user account |
| `application_status` | character varying | Yes | Current application processing status |
| `status` | character varying | Yes | Account status of the user |
| `statusmessege` | character varying | Yes | Status message associated with the account |
| `organization` | character varying | Yes | Organization name |
| `gst_no` | character varying | Yes | GST registration number |
| `business_type` | text | Yes | Business type of the organization |
| `entity_type` | character varying | Yes | Entity type of the organization |
| `address` | character varying | Yes | Registered address of the organization |
| `register_status` | character varying | Yes | Registration completion status |
| `register_india_status` | character varying | Yes | Indicates whether the organization is registered in India |
| `field_detail` | text | Yes | Additional business or operational details |
| `website` | character varying | Yes | Official website of the organization |
| `ecosystem` | text | Yes | Ecosystem services or solutions associated with the organization |
| `ip_address` | character varying | Yes | IP address from which registration was performed |
| `created_at_old` | character varying | Yes | Legacy creation timestamp stored as text |
| `application_type` | character varying | Yes | Type of application submitted |
| `updated_at_old` | character varying | Yes | Legacy update timestamp stored as text |
| `type_of_application` | character varying | Yes | Detailed classification of the application |
| `application_id` | character varying | Yes | Unique application identifier |
| `category` | character varying | Yes | Category of the organization or application |
| `product_name` | character varying | Yes | Name of the product or solution |
| `integration_level` | character varying | Yes | Level of integration achieved by the application |
| `certificate` | bytea | Yes | Uploaded certificate document |
| `certificate_ext` | character varying | Yes | File extension of the uploaded certificate |
| `solution_type` | text | Yes | Type of solution offered by the organization |
| `hmis` | character varying | Yes | Hospital Management Information System details |
| `service` | text | Yes | Services provided by the organization |
| `location_select_all` | character varying | Yes | Indicator for all-location selection |
| `state_code` | text | Yes | State codes associated with the organization |
| `city_code` | text | Yes | City codes associated with the organization |
| `area_code` | text | Yes | Area codes associated with the organization |
| `address_state` | character varying | Yes | State name of the organization address |
| `address_city` | character varying | Yes | City name of the organization address |
| `created_at_old1` | timestamp without time zone | Yes | Legacy creation timestamp |
| `updated_at_old1` | timestamp without time zone | Yes | Legacy update timestamp |
| `gst_certificate_ext` | character varying | Yes | File extension of the GST certificate |
| `gst_certificate` | bytea | Yes | Uploaded GST certificate document |
| `production_client_id` | character varying | Yes | Production environment client identifier |
| `created_at` | timestamp with time zone | Yes | Timestamp when the record was created |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the record was last updated |
| `upload_time` | timestamp with time zone | Yes | Timestamp when documents were uploaded |
| `transaction_id` | character varying | Yes | Transaction identifier for registration activities |
| `otp_status` | character varying | Yes | Status of OTP verification |
| `solution_type_others` | character varying | Yes | Additional solution type details |
| `payer_category` | character varying | Yes | Payer category associated with the organization |
| `dhis_solution_type` | character varying | Yes | DHIS solution type selected by the organization |

## password

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the password record |
| `created_at` | timestamp with time zone | Yes | Timestamp when the password record was created |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the password record was last updated |
| `value` | character varying | Yes | Encrypted or hashed password value |
| `email_id` | character varying | Yes | Email address associated with the password record |
| `createdat` | timestamp without time zone | Yes | Legacy creation timestamp |
| `updatedat` | timestamp without time zone | Yes | Legacy update timestamp |
| `emailid` | character varying | Yes | Legacy email address field |
| `id_public` | bigint | No | Public identifier of the password record |

## ci_sessions

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | character varying | No | Primary key |
| `ip_address` | character varying | No | IP address associated with the user session |
| `data` | text | No | Serialized session data stored by the application |
| `timestamp` | integer | Yes | timestamp indicating the last session activity |

## address

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the address record |
| `address_line1` | character varying | Yes | Address line 1 |
| `address_line2` | character varying | Yes | Address line 2 |
| `state_code` | bigint | Yes | State code |
| `state_name` | character varying | Yes | State name |
| `district_code` | bigint | Yes | District code |
| `district_name` | character varying | Yes | District name |
| `village_code` | bigint | Yes | Village code |
| `village_name` | character varying | Yes | Village name |
| `pin_code` | character varying | Yes | Postal PIN code |
| `sd_id` | integer | Yes | Self Declaration identifier |
| `complete_address` | character varying | Yes | Complete formatted address |

## active_integrator

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Unique identifier for the active integrator record |
| `application_id` | character varying | Yes | Application identifier |
| `added_by` | character varying | Yes | User who added the record |
| `created_at` | timestamp with time zone | Yes | Timestamp when the record was created |
| `id_public` | bigint | No | Public identifier of the active integrator record |

## self_declaration

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the self declaration record |
| `sd_id` | integer | Yes | Self Declaration identifier associated with the application |
| `complete_mil` | character varying | Yes | Indicates whether the milestones have been completed |
| `will_complete_mil` | character varying | Yes | Expected timeline for milestone completion |
| `working_on` | character varying | Yes | Current area or milestone being worked on |
| `ip_address` | character varying | Yes | IP address from which the self declaration was submitted |
| `created_at` | timestamp with time zone | Yes | Timestamp when the self declaration record was created |
| `m1_start_date` | timestamp with time zone | Yes | Start date of Milestone 1 |
| `m1_end_date` | timestamp with time zone | Yes | Completion date of Milestone 1 |
| `m2_start_date` | timestamp with time zone | Yes | Start date of Milestone 2 |
| `m2_end_date` | timestamp with time zone | Yes | Completion date of Milestone 2 |
| `m3_start_date` | timestamp with time zone | Yes | Start date of Milestone 3 |
| `m3_end_date` | timestamp with time zone | Yes | Completion date of Milestone 3 |
| `tentative_date` | timestamp with time zone | Yes | Tentative date for achieving planned milestones |
| `phr_start_date` | timestamp with time zone | Yes | Start date for PHR integration activities |
| `health_locker_start_date` | timestamp with time zone | Yes | Start date for Health Locker integration activities |
| `phr_end_date` | timestamp with time zone | Yes | Completion date for PHR integration activities |
| `health_locker_end_date` | timestamp with time zone | Yes | Completion date for Health Locker integration activities |
| `m4_start_date` | timestamp with time zone | Yes | Start date of Milestone 4 |
| `m4_end_date` | timestamp with time zone | Yes | Completion date of Milestone 4 |
| `nhcx_start_date` | timestamp with time zone | Yes | Start date of NHCX integration activities |
| `nhcx_end_date` | timestamp with time zone | Yes | Completion date of NHCX integration activities |

## sd_status

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the status  record |
| `sd_id` | bigint | Yes | Self Declaration identifier |
| `client_id` | character varying | Yes | Client identifier associated with the application |
| `admin_id` | smallint | Yes | Administrator identifier who reviewed the application |
| `admin_status` | character varying | Yes | Administrative review status |
| `admin_comment` | character varying | Yes | Comments provided by the administrator |
| `date_old` | character varying | Yes | Legacy date value for administrative review |
| `htc1_id` | character varying | Yes | Reviewer identifier for HTC stage 1 |
| `htc1_status` | character varying | Yes | Status of HTC review stage 1 |
| `htc1_comment` | character varying | Yes | Comments for HTC review stage 1 |
| `date1_old` | character varying | Yes | Legacy date value for HTC stage 1 |
| `htc2_id` | character varying | Yes | Reviewer identifier for HTC stage 2 |
| `htc2_status` | character varying | Yes | Status of HTC review stage 2 |
| `htc2_comment` | character varying | Yes | Comments for HTC review stage 2 |
| `date2_old` | character varying | Yes | Legacy date value for HTC stage 2 |
| `htc3_id` | character varying | Yes | Reviewer identifier for HTC stage 3 |
| `htc3_status` | character varying | Yes | Status of HTC review stage 3 |
| `htc3_comment` | character varying | Yes | Comments for HTC review stage 3 |
| `date3_old` | character varying | Yes | Legacy date value for HTC stage 3 |
| `edit_status` | character varying | Yes | Indicates whether the application is editable |
| `final_status` | bigint | Yes | Final approval or rejection status |
| `user_jorny` | character varying | Yes | Current stage of the user journey |
| `production_status` | character varying | Yes | Production access approval status |
| `admin_production_reject_comment` | text | Yes | Reason for production access rejection |
| `date4_old` | character varying | Yes | Legacy date value for HTC stage 4 |
| `htc4_id` | character varying | Yes | Reviewer identifier for HTC stage 4 |
| `htc4_status` | character varying | Yes | Status of HTC review stage 4 |
| `htc4_comment` | character varying | Yes | Comments for HTC review stage 4 |
| `htc4_date` | character varying | Yes | Date of HTC stage 4 review |
| `gen_token` | text | Yes | Generated access token details |
| `gen_securate` | text | Yes | Generated security credential details |
| `email_send` | text | Yes | Email notification details |
| `send_date` | character varying | Yes | Date when notification email was sent |
| `date` | timestamp without time zone | Yes | Administrative review timestamp |
| `date1` | timestamp without time zone | Yes | HTC stage 1 review timestamp |
| `date2` | timestamp without time zone | Yes | HTC stage 2 review timestamp |
| `date3` | timestamp without time zone | Yes | HTC stage 3 review timestamp |
| `date4` | timestamp without time zone | Yes | HTC stage 4 review timestamp |
| `date_temp` | timestamp with time zone | Yes | Temporary timestamp for administrative review |
| `date1_temp` | timestamp with time zone | Yes | Temporary timestamp for HTC stage 1 review |
| `date2_temp` | timestamp with time zone | Yes | Temporary timestamp for HTC stage 2 review |
| `date3_temp` | timestamp with time zone | Yes | Temporary timestamp for HTC stage 3 review |
| `date4_temp` | timestamp with time zone | Yes | Temporary timestamp for HTC stage 4 review |
| `v3_access` | bigint | Yes | Indicates V3 platform access status |

## sd_exit

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the self-declaration exit record |
| `sd_id` | integer | Yes | Self Declaration identifier |
| `organization` | character varying | Yes | Name of the organization |
| `spoc_name` | character varying | Yes | Name of the Single Point of Contact (SPOC) |
| `spoc_email` | character varying | Yes | Email address of the SPOC |
| `spoc_phone` | character varying | Yes | Mobile number of the SPOC |
| `ndhm_role` | character varying | Yes | NDHM/ABDM role selected by the organization |
| `milestone_dif` | character varying | Yes | Milestone completion status |
| `complete_integration` | character varying | Yes | Indicates whether integration has been completed |
| `integration_detail` | text | Yes | Details of the integration completed by the organization |
| `redy_for_testing` | character varying | Yes | Indicates whether the application is ready for testing |
| `demo_time` | character varying | Yes | Preferred date and time for demo or testing |
| `ip_address` | character varying | Yes | IP address from which the form was submitted |
| `organization_evaluate` | character varying | Yes | Assessment or evaluation details of the organization |
| `closer` | character | Yes | Closure status of the application |
| `host_status` | character varying | Yes | Hosting status of the application |
| `wasa_file` | bytea | Yes | Uploaded WASA document file |
| `host_file` | bytea | Yes | Uploaded hosting document file |
| `ext_wasafile` | character varying | Yes | Extension of the WASA file |
| `ext_hostfile` | character varying | Yes | Extension of the hosting document file |
| `htc1_status` | character varying | Yes | Status of HTC review stage 1 |
| `htc1comment` | character varying | Yes | Comments for HTC review stage 1 |
| `htc2_status` | character varying | Yes | Status of HTC review stage 2 |
| `htc2comment` | character varying | Yes | Comments for HTC review stage 2 |
| `htc3status` | character varying | Yes | Status of HTC review stage 3 |
| `htc3comment` | character varying | Yes | Comments for HTC review stage 3 |
| `admin_status` | character varying | Yes | Administrative review status |
| `admin_coment` | character varying | Yes | Administrative review comments |
| `integratin_phase` | character varying | Yes | Current integration phase |
| `testing_file_ext` | character varying | Yes | Extension of the functional testing report file |
| `function_testing_file` | bytea | Yes | Uploaded functional testing report |
| `bridge_url` | character varying | Yes | Bridge URL used for integration |
| `policy_file` | bytea | Yes | Uploaded policy document |
| `policy_file_ext` | character varying | Yes | Extension of the policy document |
| `webhook` | character varying | Yes | Webhook URL configured for integration |
| `remarks` | character varying | Yes | Additional remarks provided by the applicant |
| `app_status` | character varying | Yes | Application status |
| `live_aap_status` | character varying | Yes | Live application deployment status |
| `app_link` | character varying | Yes | Application access URL |
| `suporting_doc_name` | character varying | Yes | Name of the uploaded supporting document |
| `suporting_doc` | bytea | Yes | Supporting document file |
| `suporting_doc_ext` | character varying | Yes | Extension of the supporting document |
| `flag` | character varying | Yes | Flag indicating special processing status |
| `created_at` | timestamp with time zone | Yes | Timestamp when the record was created |
| `sare_date` | timestamp with time zone | Yes | Date shared with review stakeholders |
| `created_date` | timestamp with time zone | Yes | Submission date of the application |
| `admin_status_date` | timestamp with time zone | Yes | Date of administrative status update |
| `htc1_status_date` | timestamp with time zone | Yes | Date of HTC stage 1 status update |
| `htc2_status_date` | timestamp with time zone | Yes | Date of HTC stage 2 status update |
| `htc3_status_date` | timestamp with time zone | Yes | Date of HTC stage 3 status update |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the record was last updated |
| `htc4_status` | character varying | Yes | Status of HTC review stage 4 |
| `htc4_comment` | character varying | Yes | Comments for HTC review stage 4 |
| `final_status` | bigint | Yes | Final approval status of the application |
| `wasa_file_name` | character varying | Yes | Name of the uploaded WASA file |
| `host_file_name` | character varying | Yes | Name of the uploaded hosting file |
| `function_testing_file_name` | character varying | Yes | Name of the uploaded functional testing report |
| `product_name` | character varying | Yes | Name of the product or application |
| `organisation_website` | character varying | Yes | Official website of the organization |
| `company_logo_url` | character varying | Yes | URL of the organization logo |
| `brief_on_organisation` | text | Yes | Brief description of the organization |
| `self_declaration_id` | integer | Yes | Reference to the self-declaration record |
| `app_name` | character varying | Yes | Application name |
| `supporting_doc_type` | character varying | Yes | Type of supporting document uploaded |
| `gstn_id` | character varying | Yes | GSTN registration number |
| `exempted_gst` | character varying | Yes | Indicates whether GST exemption is applicable |
| `final_status_date` | timestamp with time zone | Yes | Date when the final status was assigned |
| `htc4_status_date` | timestamp with time zone | Yes | Date of HTC stage 4 status update |

## sd_exit_docs

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the SD exit document record |
| `exit_id` | bigint | No | Reference to the SD exit application record |
| `doc_type_id` | integer | No | Reference to the document type |
| `files` | bytea | Yes | Uploaded document file content |
| `file_name` | character varying | Yes | Name of the uploaded document |
| `file_ext` | character varying | Yes | File extension of the uploaded document |
| `supporting_doc_type` | character varying | Yes | Category or type of supporting document |
| `created_at` | timestamp with time zone | Yes | Timestamp when the document record was created |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the document record was last updated |
| `sd_id` | integer | Yes | Self Declaration identifier associated with the document |

## sd_doc_type

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the document type record |
| `name` | character varying | Yes | Name of the supported document type |
| `created_at` | timestamp with time zone | Yes | Timestamp when the document type was created |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the document type was last updated |

## wasa_dhis_initiation_details

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the WASA DHIS initiation details record |
| `sd_id` | integer | Yes | Self Declaration identifier associated with the application |
| `client_id` | character varying | Yes | Client identifier assigned to the participant |
| `bridge_id` | character varying | Yes | Bridge identifier associated with the integration |
| `wasa_issue_date` | timestamp with time zone | Yes | Date when the WASA was issued |
| `wasa_expiry_date` | timestamp with time zone | Yes | Date when the WASA expires |
| `wasa_status` | character varying | Yes | Current status of the WASA |
| `milestone` | character varying | Yes | Current implementation milestone achieved |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the record was last updated |

## sd_HIU

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the SD HIU record |
| `sd_id` | integer | Yes | Self Declaration identifier associated with the HIU registration |
| `client_id` | character varying | Yes | Unique client identifier assigned to the HIU |
| `organization` | character varying | Yes | Name of the HIU organization |
| `created_at` | timestamp with time zone | Yes | Timestamp when the HIU record was created |

## sd_UHI

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the SD UHI record |
| `client_id` | character varying | Yes | Client identifier associated with the UHI request |
| `email_id` | character varying | Yes | Email address of the requester |
| `intent_for_request` | character varying | Yes | Purpose or intent of the UHI request |
| `created_at` | timestamp with time zone | Yes | Timestamp when the UHI request was created |
| `sd_id` | integer | Yes | Self Declaration identifier associated with the request |
| `id_public` | bigint | No | Public identifier of the UHI request record |
| `type_of_service` | character varying | Yes | Type of service requested under UHI |
| `tell_us_about` | character varying | Yes | Description of the requester use case or requirement |
| `extra_details` | character varying | Yes | Additional details provided by the requester |

## hcx

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the HCX record |
| `sd_id` | bigint | Yes | Self Declaration identifier associated with the HCX registration |
| `name` | character varying | Yes | Name of the registrant or organization representative |
| `organization` | character varying | Yes | Organization name |
| `email` | character varying | Yes | Email address of the registrant |
| `mobile` | character varying | Yes | Mobile number of the registrant |
| `password` | character varying | Yes | Encrypted password for the HCX account |
| `solution_type` | text | Yes | Type of solution offered by the organization |
| `field_detail` | text | Yes | Additional details about the solution or field of operation |
| `entity_type` | character varying | Yes | Type of entity participating in HCX |
| `type_of_application` | character varying | Yes | Type of application being registered |
| `category` | character varying | Yes | Category of the organization or application |
| `business_type` | character varying | Yes | Business classification of the organization |
| `registered_in_india_status` | character varying | Yes | Indicates whether the organization is registered in India |
| `gst_no` | character varying | Yes | GST registration number |
| `product_name` | character varying | Yes | Name of the product or solution |
| `website` | character varying | Yes | Official website URL of the organization |
| `application_type` | character varying | Yes | Application role or type within HCX |
| `created_at` | timestamp with time zone | Yes | Timestamp when the record was created |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the record was last updated |
| `id_public` | bigint | No | Public identifier of the HCX record |
| `payer_category` | character varying | Yes | Category of payer associated with the HCX application |

## hcx_address

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the HCX address record |
| `hcx_id` | bigint | Yes | Reference identifier of the associated HCX registration |
| `registered_address` | character varying | Yes | Registered business address of the organization |
| `state_code` | bigint | Yes | State code of the registered address |
| `state_name` | character varying | Yes | State name of the registered address |
| `district_code` | bigint | Yes | District code of the registered address |
| `district_name` | character varying | Yes | District name of the registered address |
| `pin_code` | character varying | Yes | Postal PIN code of the registered address |
| `id_public` | bigint | No | Public identifier of the HCX address record |

## NHCX_exit

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the NHCX exit record |
| `sd_id` | bigint | Yes | Self Declaration identifier associated with the NHCX exit record |
| `name` | character varying | Yes | Name of the applicant or organization representative |
| `organization` | character varying | Yes | Organization name associated with the NHCX registration |
| `email` | character varying | Yes | Email address of the applicant |
| `mobile` | character varying | Yes | Mobile number of the applicant |
| `nhcx_final_status` | bigint | Yes | Final status of the NHCX application |
| `nhcx_admin_status` | character varying | Yes | Administrative review status of the NHCX application |
| `nhcx_admin_comment` | character varying | Yes | Comments or remarks provided by the administrator |
| `nhcx_admin_status_updated_at` | timestamp with time zone | Yes | Timestamp when the administrative status was last updated |
| `created_at` | timestamp with time zone | Yes | Timestamp when the NHCX exit record was created |

## mst_role

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `role_id` | integer | No | Primary key of the role |
| `role_name` | character varying | Yes | Name of the role |
| `role_description` | character varying | Yes | Description of the role and its responsibilities |
| `role_status` | smallint | Yes | Status of the role (e.g., Active or Inactive) |
| `role_created_by` | smallint | Yes | Identifier of the user who created the role |
| `role_created_ip` | character varying | Yes | IP address from which the role was created |
| `role_modified_by` | character varying | Yes | User who last modified the role |
| `role_modified_ip` | character varying | Yes | IP address from which the role was last modified |
| `role_landing_page` | smallint | Yes | Default landing page assigned to the role |
| `is_subrole` | character varying | Yes | Indicates whether the role is a sub-role |
| `parentrole_id` | character varying | Yes | Identifier of the parent role |
| `role_created_date` | timestamp with time zone | Yes | Timestamp when the role was created |
| `role_modified_date` | timestamp with time zone | Yes | Timestamp when the role was last modified |

## mst_modules

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `module_id` | integer | No | Primary key of the module |
| `module_name` | character varying | Yes | Name of the module |
| `module_type` | character varying | Yes | Type or category of the module |
| `module_desc` | character varying | Yes | Description of the module |
| `is_parent` | character varying | Yes | Indicates whether the module is a parent module |
| `parent_id` | character varying | Yes | Identifier of the parent module |
| `order_appearance` | character varying | Yes | Display order of the module in the application |
| `is_display` | character varying | Yes | Indicates whether the module should be displayed |
| `delete_status` | character varying | Yes | Logical deletion status of the module |
| `link` | character varying | Yes | Navigation URL or link associated with the module |
| `image_path` | character varying | Yes | Path of the image associated with the module |
| `icon_class` | character varying | Yes | CSS icon class used for module display |
| `created_by` | character varying | Yes | User who created the module |
| `created_ip` | character varying | Yes | IP address from which the module was created |
| `modified_by` | character varying | Yes | User who last modified the module |
| `modified_ip` | character varying | Yes | IP address from which the module was last modified |
| `created_date` | timestamp with time zone | Yes | Timestamp when the module was created |
| `modified_date` | timestamp with time zone | Yes | Timestamp when the module was last modified |

## mst_privilege

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `previlege_id` | integer | No | Primary key of the privilege record |
| `role_id` | smallint | Yes | Role identifier associated with the privilege |
| `module_id` | character varying | Yes | Module identifier for which access is granted |
| `access_id` | character varying | Yes | Access permission identifier |
| `created_by` | character varying | Yes | User who created the privilege record |
| `created_date_old` | character varying | Yes | Legacy created date value retained for reference |
| `created_ip` | character varying | Yes | IP address from which the privilege record was created |
| `modified_by` | character varying | Yes | User who last modified the privilege record |
| `modified_date_old` | character varying | Yes | Legacy modified date value retained for reference |
| `modified_ip` | character varying | Yes | IP address from which the privilege record was last modified |
| `created_date` | timestamp without time zone | Yes | Timestamp when the privilege record was created |
| `modified_date` | timestamp without time zone | Yes | Timestamp when the privilege record was last modified |
| `id_public` | bigint | No | Public identifier of the privilege record |

## audit_log

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the audit log record |
| `sd_id` | bigint | Yes | Self Declaration identifier associated with the audit entry |
| `name` | character varying | Yes | Name of the user whose data was modified |
| `application_id` | character varying | Yes | Application identifier associated with the audit entry |
| `entity_name` | character varying | Yes | Name of the entity or table being audited |
| `updated_at` | timestamp without time zone | Yes | Timestamp when the modification occurred |
| `email_id` | character varying | Yes | Email address of the user who performed the action |
| `id_public` | bigint | No | Public identifier of the audit log record |
| `old_data` | text | Yes | Data before the update operation |
| `new_data` | text | Yes | Data after the update operation |
| `action_type` | character varying | Yes | Type of action performed (UPDATE) |

## security_audit_trail

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the security audit trail record |
| `process_id` | character varying | Yes | Unique identifier of the process or transaction being audited |
| `ip_address` | character varying | Yes | IP address from which the request originated |
| `user_agent` | text | Yes | User agent details of the requesting client |
| `http_method` | character varying | Yes | HTTP method used in the request (GET, POST, PUT, DELETE, etc.) |
| `endpoint` | character varying | Yes | API endpoint accessed during the request |
| `username` | character varying | Yes | Username associated with the request |
| `status` | character varying | Yes | Processing status of the request |
| `correlation_id` | character varying | Yes | Correlation identifier used for tracing requests across services |
| `created_at` | timestamp with time zone | Yes | Timestamp when the audit record was created |
| `payload` | text | Yes | Request or response payload captured for auditing purposes |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the audit record was last updated |
| `id_public` | bigint | No | Public identifier of the security audit trail record |

## log

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the log record |
| `sd_id` | character varying | Yes | Self Declaration identifier associated with the log entry |
| `client_id` | character varying | Yes | Client identifier associated with the log entry |
| `signup_date` | character varying | Yes | Date when the user signed up |
| `evl_date` | character varying | Yes | Date of evaluation or verification |
| `gen_token` | text | Yes | Generated token details |
| `gen_securate` | text | Yes | Generated security credentials or secure token information |
| `email_send` | text | Yes | Email sending status or details |
| `send_date` | character varying | Yes | Date when the email was sent |
| `update_at` | character varying | Yes | Date when the log record was last updated |
| `email` | character varying | Yes | Email address associated with the log entry |
| `response` | text | Yes | Response received from the external system or service |
| `status` | character varying | Yes | Current status of the operation |
| `id_public` | bigint | No | Public identifier of the log record |

## notification_audit

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | bigint | No | Primary key of the notification audit record |
| `request_id` | character varying | Yes | Unique request identifier associated with the notification |
| `template_id` | character varying | Yes | Identifier of the notification template used |
| `template_name` | character varying | Yes | Name of the notification template used |
| `message` | character varying | Yes | Notification message content sent to the recipient |
| `receiver` | character varying | Yes | Recipient of the notification |
| `type` | character varying | Yes | Type of notification (e.g., Email, SMS, Push Notification) |
| `status` | character varying | Yes | Delivery status of the notification |
| `created_at` | timestamp with time zone | Yes | Timestamp when the notification record was created |
| `updated_at` | timestamp with time zone | Yes | Timestamp when the notification record was last updated |
| `id_public` | bigint | No | Public identifier of the notification audit record |

## concern

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the concern record |
| `sd_id` | smallint | Yes | Self Declaration identifier associated with the concern |
| `clientid` | character varying | Yes | Client identifier associated with the concern |
| `concern_type` | character varying | Yes | Type or category of the concern raised |
| `name` | character varying | Yes | Name of the person who raised the concern |
| `messege` | character varying | Yes | Concern message or details submitted by the user |
| `created` | character varying | Yes | Date and time when the concern was created |
| `created_ip` | character varying | Yes | IP address from which the concern was submitted |
| `id_public` | bigint | No | Public identifier of the concern record |

## std_data

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `id` | integer | No | Primary key of the STD data record |
| `state_code` | character varying | Yes | Code of the state associated with the STD code |
| `ldca_name` | character varying | Yes | Long Distance Charging Area (LDCA) name |
| `sdca_name` | character varying | Yes | Short Distance Charging Area (SDCA) name |
| `std_code` | character varying | Yes | STD telephone dialing code for the area |

## upcoming_session

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `start_time` | character varying | Yes | Scheduled start time of the session |
| `end_time` | character varying | Yes | Scheduled end time of the session |
| `session_name` | character varying | Yes | Name or title of the upcoming session |
| `link` | character varying | Yes | Meeting or session joining link |
| `created_at` | character varying | Yes | Date and time when the session record was created |
| `id` | integer | No | Primary key of the upcoming session record |
| `date` | timestamp without time zone | Yes | Scheduled date of the session |

## awsdms_apply_exceptions

Infrastructure, not portal data.

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `TASK_NAME` | character varying | No | AWS DMS task name that generated the exception |
| `TABLE_OWNER` | character varying | No | Schema owner of the table |
| `TABLE_NAME` | character varying | No | Name of the table where the exception occurred |
| `ERROR_TIME` | timestamp without time zone | No | Timestamp when the exception was recorded |
| `STATEMENT` | text | No | SQL statement that caused the exception |
| `ERROR` | text | No | Error message returned by AWS DMS |

## Backup copies

Three tables are named as backups of `sd_login`. A fourth, `sd_exit_live`,
carries the same column list as `sd_exit`, and the source does not say which of
that pair the portal writes to. All four repeat a column list above, so they are
summarised rather than listed in full.

| Table | Mirrors | Columns | Difference from the table it mirrors |
| --- | --- | --- | --- |
| `sd_login_bk` | `sd_login` | 50 | Same column list, except it does not have `payer_category`, `dhis_solution_type`. |
| `sd_login_bk_16062026` | `sd_login` | 52 | Same column list. |
| `sd_login_bk_20012026_updt` | `sd_login` | 50 | Same column list, except it does not have `payer_category`, `dhis_solution_type`. |
| `sd_exit_live` | `sd_exit` | 68 | Same column list. |

The three `sd_login` copies are owned by `sandboxportaluser`, every other table
in the schema by `appprdusrsandbox`. The digits in `sd_login_bk_16062026` and
`sd_login_bk_20012026_updt` read as dates, and the source does not say what they
mark.

## Indexes

Every index, with the columns it covers.

| Table | Index | Unique | On |
| --- | --- | --- | --- |
| `active_integrator` | `active_integrator_pkey` | Yes | `id_public` |
| `address` | `address_pkey` | Yes | `id` |
| `address` | `address_sd_id_uk` | Yes | `sd_id` |
| `audit_log` | `audit_log_pkey` | Yes | `id_public` |
| `ci_sessions` | `ci_sessions_pkey` | Yes | `id` |
| `ci_sessions` | `idx_ci_sessions_data` | No | `data` |
| `ci_sessions` | `idx_ci_sessions_ip` | No | `ip_address` |
| `ci_sessions` | `idx_ci_sessions_timestamp` | No | `timestamp` |
| `concern` | `concern_pkey` | Yes | `id_public` |
| `hcx` | `hcx_pkey` | Yes | `id_public` |
| `hcx_address` | `hcx_address_pkey` | Yes | `id_public` |
| `log` | `log_pkey` | Yes | `id_public` |
| `mst_modules` | `mst_modules_pkey` | Yes | `module_id` |
| `mst_privilege` | `mst_privilege_pkey` | Yes | `id_public` |
| `mst_role` | `idx_role_name_sandbox` | No | `role_name` |
| `mst_role` | `mst_role_pkey` | Yes | `role_id` |
| `notification_audit` | `notification_audit_pkey` | Yes | `id_public` |
| `password` | `password_pkey` | Yes | `id_public` |
| `sd_doc_type` | `sd_doc_type_pkey` | Yes | `id` |
| `sd_exit` | `idx_sd_exit_final_status` | No | `final_status` |
| `sd_exit` | `idx_sd_exit_sd_id` | No | `sd_id` |
| `sd_exit` | `sd_exit_pkey1` | Yes | `id` |
| `sd_exit_docs` | `idx_sd_exit_docs_exit_id` | No | `exit_id` |
| `sd_exit_docs` | `idx_sd_exit_docs_id` | No | `id` |
| `sd_exit_docs` | `idx_sd_exit_docs_sd_id` | No | `sd_id` |
| `sd_exit_docs` | `sd_exit_docs_pkey` | Yes | `id` |
| `sd_exit_live` | `sd_exit_pkey` | Yes | `id` |
| `sd_hiu` | `sd_hiu_pkey` | Yes | `id` |
| `sd_login` | `idx_sd_login_created_at` | No | `created_at_old` |
| `sd_login` | `idx_sd_login_email` | No | `email` |
| `sd_login` | `idx_sd_login_role_id` | No | `role_id` |
| `sd_login` | `idx_sd_login_sd_id` | No | `sd_id` |
| `sd_login` | `idx_sd_login_updated_at` | No | `updated_at` |
| `sd_login` | `sd_login_pkey` | Yes | `sd_id` |
| `sd_login` | `sd_login_type_of_application_idx` | No | `type_of_application` |
| `sd_status` | `idx_sd_status_sd_id` | No | `sd_id` |
| `sd_status` | `sd_status_pkey` | Yes | `id` |
| `sd_uhi` | `sd_uhi_pkey` | Yes | `id_public` |
| `security_audit_trail` | `security_audit_trail_pkey` | Yes | `id_public` |
| `self_declaration` | `self_declaration_m1_start_date_idx` | No | `m1_start_date`, `m1_end_date`, `m2_start_date`, `m2_end_date`, `m3_start_date`, `m3_end_date`, `m4_start_date`, `m4_end_date` |
| `self_declaration` | `self_declaration_pkey` | Yes | `id` |
| `self_declaration` | `self_declaration_sd_id_idx` | No | `sd_id` |
| `std_data` | `std_data_pkey` | Yes | `id` |
| `upcoming_session` | `upcoming_session_pkey` | Yes | `id` |
| `wasa_dhis_initiation_details` | `wasa_dhis_initiation_details_pkey` | Yes | `id` |

Every index in the source is a btree.

## What is not transcribed

Two sheets are left out, and neither carries anything you act on.

- **Sequences**, 34 Postgres sequences, one per auto incrementing key, with
  start value, minimum, maximum and increment. Every one increments by 1 and
  does not cycle.
- **Def values**, 104 column defaults, of two kinds:
  `nextval('<sequence>'::regclass)` on identifier columns and
  `NULL::character varying` on text columns.

Both are in the sandbox document pack, data dictionary v1.0.

## What this page does not tell you

This dictionary describes the sandbox portal, not the [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm)
APIs. It carries no request shape, no response shape and no endpoint. Registry
identifiers such as [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) numbers do not appear in
it at all.

For the APIs, start at [choose your gateway](/docs/hiecm/v3). For the sandbox
itself and how to sign up, read [get started](/docs/hiecm/v3/getting-started/sandbox).
