import { hiTypeLabel } from "@/components/abdm/care-context-state";
import { fromDateInput, toDateInput } from "@/components/abdm/hiu-state";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmConsentRequestCreate,
  type AbdmHiuState,
  type AbdmProvider,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { Loader2, Search, X } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

/**
 * "Request records" dialog (ADR-014, M3 journey 1). The defaults come from the backend state
 * (purpose CAREMGT, the 7 clinical record types, the last 12 months, 30 days of validity) and
 * every field is editable. The provider picker is optional: with no provider the request goes to
 * every facility the patient has records at. The dialog keeps a fixed layout; the provider result
 * list grows below the search field and never moves the fields above it.
 */

const VALIDITY_DAYS = [7, 30, 90, 180] as const;

const selectClass =
  "border-input dark:bg-input/30 h-12 w-full rounded-md border bg-transparent px-3 py-1 text-base shadow-2xs outline-none md:h-10 md:px-2.5 md:text-sm";

function addDays(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString();
}

export default function ConsentRequestDialog({
  open,
  onOpenChange,
  state,
  facilityId,
  onSubmit,
  pending,
  error,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  state: AbdmHiuState;
  facilityId: string;
  onSubmit: (body: AbdmConsentRequestCreate) => void;
  pending: boolean;
  error?: string;
}) {
  const { t } = useTranslation();
  const [purpose, setPurpose] = useState(state.defaults.purposeCode);
  const [types, setTypes] = useState<Set<string>>(
    new Set(state.defaults.hiTypes),
  );
  const [from, setFrom] = useState(toDateInput(state.defaults.dateFrom));
  const [to, setTo] = useState(toDateInput(state.defaults.dateTo));
  const [validity, setValidity] = useState<number>(30);
  const [providerQuery, setProviderQuery] = useState("");
  const [provider, setProvider] = useState<AbdmProvider | null>(null);
  const [localError, setLocalError] = useState<string>();

  // Reset to the defaults each time the dialog opens, so a second request starts clean.
  useEffect(() => {
    if (!open) return;
    setPurpose(state.defaults.purposeCode);
    setTypes(new Set(state.defaults.hiTypes));
    setFrom(toDateInput(state.defaults.dateFrom));
    setTo(toDateInput(state.defaults.dateTo));
    setValidity(30);
    setProviderQuery("");
    setProvider(null);
    setLocalError(undefined);
  }, [open, state.defaults]);

  const providers = useQuery({
    queryKey: ["abdm", "providers", providerQuery],
    queryFn: query.debounced(careApi.providers, {
      queryParams: { name: providerQuery },
      silent: true,
    }),
    enabled: open && providerQuery.trim().length >= 3 && !provider,
    retry: false,
  });

  const valid = useMemo(() => {
    if (types.size === 0) return t("abdm_fetch_dialog_no_types");
    if (from && to && from > to) return t("abdm_fetch_dialog_bad_range");
    return "";
  }, [types, from, to, t]);

  const submit = () => {
    if (valid) {
      setLocalError(valid);
      return;
    }
    setLocalError(undefined);
    onSubmit({
      facility_id: facilityId,
      purpose_code: purpose,
      hi_types: [...types],
      date_from: fromDateInput(from),
      date_to: fromDateInput(to, true),
      data_erase_at: addDays(validity),
      hip_id: provider?.id ?? "",
      hip_name: provider?.name ?? "",
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{t("abdm_fetch_dialog_title")}</DialogTitle>
          <DialogDescription>{t("abdm_fetch_dialog_intro")}</DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 text-sm">
          <div className="grid gap-1.5">
            <Label htmlFor="abdm-cr-purpose">{t("abdm_fetch_purpose")}</Label>
            <select
              id="abdm-cr-purpose"
              className={selectClass}
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
            >
              {state.purposes.map((p) => (
                <option key={p.code} value={p.code}>
                  {p.text}
                </option>
              ))}
            </select>
          </div>

          <div className="grid gap-1.5">
            <span className="text-sm font-medium">{t("abdm_fetch_types")}</span>
            <div className="grid gap-2 sm:grid-cols-2">
              {state.hiTypes.map((hiType) => (
                <label key={hiType} className="flex items-center gap-2">
                  <Checkbox
                    checked={types.has(hiType)}
                    onCheckedChange={(value) =>
                      setTypes((prev) => {
                        const next = new Set(prev);
                        if (value) next.add(hiType);
                        else next.delete(hiType);
                        return next;
                      })
                    }
                  />
                  <span>{hiTypeLabel(t, hiType)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            <div className="grid gap-1.5">
              <Label htmlFor="abdm-cr-from">{t("abdm_fetch_from")}</Label>
              <Input
                id="abdm-cr-from"
                type="date"
                value={from}
                max={to}
                onChange={(e) => setFrom(e.target.value)}
              />
            </div>
            <div className="grid gap-1.5">
              <Label htmlFor="abdm-cr-to">{t("abdm_fetch_to")}</Label>
              <Input
                id="abdm-cr-to"
                type="date"
                value={to}
                min={from}
                max={toDateInput(new Date())}
                onChange={(e) => setTo(e.target.value)}
              />
            </div>
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="abdm-cr-validity">{t("abdm_fetch_validity")}</Label>
            <select
              id="abdm-cr-validity"
              className={selectClass}
              value={validity}
              onChange={(e) => setValidity(Number(e.target.value))}
            >
              {VALIDITY_DAYS.map((days) => (
                <option key={days} value={days}>
                  {t("abdm_fetch_validity_days", { days: String(days) })}
                </option>
              ))}
            </select>
            <p className="text-muted-foreground text-xs">
              {t("abdm_fetch_validity_help")}
            </p>
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="abdm-cr-provider">{t("abdm_fetch_provider")}</Label>
            {provider ? (
              <div className="flex items-center gap-2 rounded-md border px-3 py-2">
                <span className="grow">{provider.name}</span>
                <span className="text-muted-foreground font-mono text-xs">
                  {provider.id}
                </span>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon-sm"
                  aria-label={t("abdm_fetch_provider_clear")}
                  onClick={() => setProvider(null)}
                >
                  <X />
                </Button>
              </div>
            ) : (
              <div className="relative">
                <Search className="text-muted-foreground pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2" />
                <Input
                  id="abdm-cr-provider"
                  className="pl-8"
                  placeholder={t("abdm_fetch_provider_placeholder")}
                  value={providerQuery}
                  onChange={(e) => setProviderQuery(e.target.value)}
                />
              </div>
            )}
            <p className="text-muted-foreground text-xs">
              {t("abdm_fetch_provider_help")}
            </p>
            {!provider && providerQuery.trim().length >= 3 && (
              <div className="grid max-h-40 gap-1 overflow-y-auto rounded-md border p-1">
                {providers.isFetching && (
                  <span className="text-muted-foreground flex items-center gap-2 px-2 py-1 text-xs">
                    <Loader2 className="size-3 animate-spin" />{" "}
                    {t("abdm_fetch_provider_searching")}
                  </span>
                )}
                {providers.isError && (
                  <span className="text-destructive px-2 py-1 text-xs">
                    {t("abdm_fetch_provider_failed")}
                  </span>
                )}
                {providers.data &&
                  providers.data.results.length === 0 &&
                  !providers.isFetching && (
                    <span className="text-muted-foreground px-2 py-1 text-xs">
                      {t("abdm_fetch_provider_none")}
                    </span>
                  )}
                {providers.data?.results.map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    className="hover:bg-muted flex items-center gap-2 rounded px-2 py-1 text-left"
                    onClick={() => setProvider(p)}
                  >
                    <span className="grow">{p.name}</span>
                    <span className="text-muted-foreground font-mono text-xs">
                      {p.id}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {(localError || error) && (
            <Alert variant="destructive">
              <AlertDescription>{localError || error}</AlertDescription>
            </Alert>
          )}
        </div>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={pending}
          >
            {t("abdm_cancel")}
          </Button>
          <Button type="button" onClick={submit} disabled={pending}>
            {pending && <Loader2 className="size-4 animate-spin" />}
            {t("abdm_fetch_dialog_submit")}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
