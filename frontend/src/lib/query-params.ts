import { useQueryParams } from "raviger";

/**
 * URL query state with the host's clean rule (findings J11).
 *
 * raviger 5.3 `useQueryParams` serialises through `URLSearchParams` and drops only `null`
 * (`serializeQuery` in `raviger/dist/module.js`). A value of `undefined` becomes the string
 * "undefined" in the URL, and it reads back as a truthy id. care_fe avoids this in `useFilters`:
 * `FiltersCache.utils.clean` keeps a key only when `(value ?? "") != ""`, and every write uses
 * `replace: true` (`care_fe/src/hooks/useFilters.tsx`, `care_fe/src/Utils/FiltersCache.tsx`).
 * A remote cannot import that hook, so this file mirrors it.
 */

type Query = Record<string, string | undefined>;

/**
 * Keep a key only when its value is present and not blank. The literals "undefined" and "null"
 * are dropped too: a link written before this rule can carry them, and no id or name has that text.
 */
export function cleanQuery<T extends Query>(query: T): T {
  const out: Record<string, string> = {};
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null) continue;
    const text = String(value).trim();
    if (text === "" || text === "undefined" || text === "null") continue;
    out[key] = text;
  }
  return out as T;
}

/**
 * `useQueryParams` with the clean rule on both sides. `set` merges `next` into the current
 * query; a key set to `undefined` or "" leaves the URL. A write replaces the history entry unless
 * `push` is true: a place (a tab, an opened sheet) pushes, so Back returns to the view before it;
 * an adjustment (a filter, a closed sheet) replaces.
 */
export function useCleanQueryParams<T extends Query>(): [
  T,
  (next: Partial<T>, options?: { push?: boolean }) => void,
] {
  const [raw, setRaw] = useQueryParams<Record<string, string>>();
  const params = cleanQuery(raw) as T;
  const set = (next: Partial<T>, { push = false }: { push?: boolean } = {}) =>
    setRaw(cleanQuery({ ...raw, ...next }), { replace: !push });
  return [params, set];
}
