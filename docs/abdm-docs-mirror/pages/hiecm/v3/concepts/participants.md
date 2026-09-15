# Ecosystem participants

[ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) is one network with several kinds of participant on it. Each holds an identifier issued by a registry, and each plays a role in the exchange. This section has one page per participant, and every page answers the same three questions: who you are, what you can do, and why it is worth taking part.

Two of the eight do not integrate with anything. A citizen carries an identity and makes decisions. We run the network and issue the identifiers. The other six build software.

| Participant                                               | Who they are                                                                                                             |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [Citizen](/docs/hiecm/v3/concepts/participants/citizen)   | The person the records are about, holding an [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) number and address     |
| [Doctor](/docs/hiecm/v3/concepts/participants/doctor)     | A registered professional holding an [HPID](/docs/hiecm/v3/getting-started/glossary#hpid) from the professional registry |
| [Hospital](/docs/hiecm/v3/concepts/participants/hospital) | A facility that creates records, shares them, and reads records held elsewhere                                           |
| [Diagnostics](/docs/hiecm/v3/concepts/participants/lab)   | A laboratory or imaging centre, sharing reports as a facility                                                            |
| [Pharmacy](/docs/hiecm/v3/concepts/participants/pharmacy) | A pharmacy, sharing prescription and billing records as a facility                                                       |
| [Insurer](/docs/hiecm/v3/concepts/participants/insurer)   | A payer that reads records under consent, and settles claims on a separate gateway                                       |
| [PHR app](/docs/hiecm/v3/concepts/participants/phr)       | The citizen's own app: identity, linking, consent and records                                                            |
| [NHA](/docs/hiecm/v3/concepts/participants/nha)           | The National Health Authority, which runs the gateways and the registries                                                |

## A role belongs to the entity, not the software

[HIP](/docs/hiecm/v3/getting-started/glossary#hip) and [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) are roles an entity takes, not kinds of software and not kinds of company. Whoever holds a record and publishes it is the HIP: a facility publishing through its [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis), or a citizen pushing a record from their PHR app. Whoever asks to read records they did not create is the HIU, and an insurer or a referral service asks while holding neither an ABHA address nor a facility ID. So a hospital, a laboratory and a pharmacy sit in the same position and differ only in the records they hold.

## Next

- [How the pieces fit](/docs/hiecm/v3/concepts/how-it-fits), the registries, the gateway and the roles in one page.
- [Your integration path](/docs/hiecm/v3/milestones), what each role has to build.
