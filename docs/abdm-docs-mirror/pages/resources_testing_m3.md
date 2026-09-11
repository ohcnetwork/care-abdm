# M3 testing use cases

[M3](/docs/hiecm/v3/milestones/m3) is about asking for records you did not
create. Whoever asks is the
[HIU](/docs/hiecm/v3/getting-started/glossary#hiu).

The cases follow one consent request through its whole life. You discover the
patient, raise the request against their
[ABHA address](/docs/hiecm/v3/getting-started/glossary#abha-address), and
handle each outcome the person can choose. A granted request is then fetched
against, one case per
[HI type](/docs/hiecm/v3/getting-started/glossary#hi-type). Revoking the
[consent artefact](/docs/hiecm/v3/getting-started/glossary#consent-artefact)
and letting it expire close the set.

16 are certification cases, and each keeps the id you will be asked about at certification. 16 are
Portal checks, which are suggestions rather than requirements.

Most of these cases expect a callback. Register a callback URL before you start.

## Next

- The calls these cases make: [M3 API reference](/docs/hiecm/v3/api/m3).
- The build order behind them: [M3 Retrieve](/docs/hiecm/v3/milestones/m3).
- The next module: [M4 testing use cases](./m4).
