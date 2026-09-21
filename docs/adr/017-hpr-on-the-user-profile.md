# ADR-017 — "My HPR ID" moves to the user profile, and the long flows move into sheets

Status: Accepted (Rithvik, 2026-09-21: "we don't need a facility scoped route for it in the first
place right?"; "in care core, we support `UserProfileSections` … we could move everything there";
"let's have the world's best UX and UI experience for this". Design chosen by him: a side sheet.)
Date: 2026-09-21
Depends on: ADR-015 (M4: the NHPR from CARE), ADR-003 (host slots).
Amends: ADR-015 (the `userNavItems` entry and the 2 `abdm-hpr` routes are removed).

## Context

ADR-015 put the professional side of M4 on a page of its own, `hpr-page.tsx`, and opened it from a
`userNavItems` entry.

The host builds such an entry into a facility path and gives no other form:

```tsx
// care_fe/src/components/ui/sidebar/nav-user.tsx:123-131
onClick={() => navigate(
  `/facility/${selectedFacilityId}/users/${user.username}/${item.url}`,
)}
```

The host's own "Profile" item has a fallback for the state with no facility; a plug item has none.
So a person who opened "My HPR ID" from outside a facility went to
`/facility/undefined/users/<name>/abdm-hpr`. The plug route matched, but the page then read the
facility `undefined` and showed "not found".

Facts that shape the design:

| Fact | Source |
|---|---|
| `userNavItems` always navigates to `/facility/${selectedFacilityId}/users/${username}/${url}`. No fallback. | `care_fe/src/components/ui/sidebar/nav-user.tsx:123-131` |
| The host has a plug slot on the user profile: `UserProfileSectionsComponentType = React.FC<{user: UserRead; isOwnProfile: boolean; className?: string}>`. | `care_fe/src/pluginTypes.ts:141-146` |
| The host renders that slot at the end of the profile summary, inside the page container. | `care_fe/src/components/Users/UserSummary.tsx:203-207` |
| Each host section of that page is a `UserColumns`: `<section className="flex flex-col gap-5 sm:flex-row">`, a `sm:w-1/4` heading and note, a `sm:w-3/4` body. | `care_fe/src/components/Common/UserColumns.tsx` |
| Every HPR route of the plug reads the caller (`users/me/...`). No route takes a username. | `abdm/nhpr/views.py`, `frontend/src/lib/careApi.ts` |
| The plug rewrites `:root` to `.care-abdm-fe-container`, so a portal outside that element loses every token. | `frontend/postcss.config.js`, `docs/05-codebase-map.md` |

## Decisions

1. **The slot replaces the route.** The plug registers `UserProfileSections`. The 2 routes
   (`/facility/:facilityId/users/:username/abdm-hpr` and `/users/:username/abdm-hpr`), the
   `userNavItems` entry and `hpr-page.tsx` are removed. Nothing is in production, so no bookmark
   must survive.

2. **The section shows nothing on another person's profile.** The backend answers for the caller
   only, so the component returns `null` when `isOwnProfile` is false.

3. **The profile page keeps a stable height.** The section is a summary card: the HPR ID, the HPR ID
   number, the role, the registration state, the session state and the session expiry. A disclosure
   holds the account details. Nothing on the page moves when a person opens a flow.

4. **Every long flow opens in a sheet.** 3 sheets: create an HPR ID (`HpidCreateWizard`), the
   professional profile (the registry facts, then `HprRegisterForm`), and the documents
   (`HprDocuments`). A sheet is full height and scrolls on its own, so a 5-block form does not push
   the profile page down. Each of the 2 forms takes an `embedded` flag that drops its own card frame
   and header, because the sheet header carries the title.

5. **The registry answer becomes a field list.** The old page printed the professional block as raw
   JSON. `RegistryFacts` shows each scalar as a labelled field and keeps the nested blocks behind a
   disclosure. The shape of that blob is still unproven (sandbox proof 7), so the disclosure stays.

6. **The secondary actions go into a menu.** Log in again, read the registry, log out and unlink sit
   in a dropdown menu at the end of the card footer. The 3 first actions stay as buttons.

7. **A linked HPR ID gets the inverted hero card** (Rithvik, 2026-09-21). The card carries the same
   gradient, the same blur orbs and the same field tiles as the care-context hero of the encounter
   ABDM tab, so the 2 ABDM identity cards read alike. The green button variants disappear on that
   gradient, so a hero button is white with green words (`heroSolid`) or a translucent white face
   (`heroGhost`). The state with no HPR ID keeps the plain card: it is a prompt, not an identity.

8. **The sheet renders into the plug container.** `ui/sheet.tsx` comes from the Care UI registry with
   1 local change: the portal takes `container={usePortalContainer()}`, like `dialog.tsx` and
   `dropdown-menu.tsx`. Without it the sheet loses every token.

## Consequences

- A person reaches the HPR ID from the profile page, with or without a facility. The host bug of the
  plug `userNavItems` URL no longer applies to this plug.
- The entry point is 1 click deeper than a menu item. The profile page is the place a person looks
  for an identity, so this is acceptable.
- If the host later gives `userNavItems` a non-facility fallback, a menu item can come back and open
  the same profile page.

## Alternatives not taken

- **Keep the route and guard the facility.** The page would still open at
  `/facility/undefined/...`, which is a wrong URL to show a person.
- **A `navItems` entry instead.** The same host builder applies, with the same result.
- **Full-page steps inside the profile page.** The page would grow and shrink as a person moves
  through a 5-block form. Rithvik asked for stable layouts.
