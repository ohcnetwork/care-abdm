import { selectClass, useMaster } from "@/components/abdm/nhpr-shared";
import { useTranslation } from "@/hooks/use-translation";
import type { AbdmMasterRow } from "@/lib/careApi";
import { cn } from "@/lib/utils";

/**
 * A native <select> fed by 1 NHPR code list (`GET nhpr/masters/<kind>`). The registry accepts
 * codes, never display values (registries/nhpr/hfr §Codes, not names), so every coded field of the
 * M4 forms goes through this control. Options load once per kind and parameters (backend cache 24 h).
 */

export default function MasterSelect({
  id,
  kind,
  params = {},
  value,
  onChange,
  disabled,
  placeholder,
  className,
  multiple,
  enabled = true,
}: {
  id?: string;
  kind: string;
  params?: Record<string, string>;
  value: string | string[];
  onChange: (value: string, row?: AbdmMasterRow) => void;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
  multiple?: boolean;
  enabled?: boolean;
}) {
  const { t } = useTranslation();
  const rows = useMaster(kind, params, enabled);
  const options = rows.data?.results ?? [];
  return (
    <div className="grid gap-1">
      <select
        id={id}
        className={cn(
          selectClass,
          multiple && "h-auto min-h-24 py-2",
          className,
        )}
        value={value}
        multiple={multiple}
        disabled={disabled || rows.isLoading || !enabled}
        onChange={(e) => {
          if (multiple) {
            const picked = Array.from(e.target.selectedOptions).map(
              (o) => o.value,
            );
            onChange(picked.join(","));
            return;
          }
          onChange(
            e.target.value,
            options.find((o) => o.code === e.target.value),
          );
        }}
      >
        {!multiple && (
          <option value="">
            {rows.isLoading
              ? t("abdm_master_loading")
              : (placeholder ?? t("abdm_master_pick"))}
          </option>
        )}
        {options.map((row) => (
          <option key={row.code} value={row.code}>
            {row.name}
          </option>
        ))}
      </select>
      {rows.isError && (
        <span className="text-destructive text-xs">
          {t("abdm_master_failed")}
        </span>
      )}
    </div>
  );
}
