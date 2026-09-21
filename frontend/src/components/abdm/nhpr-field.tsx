import FieldHelp, { type FieldHelpContent } from "@/components/abdm/field-help";
import { useNhprHelp } from "@/components/abdm/nhpr-shared";
import { Label } from "@/components/ui/label";
import { useTranslation } from "@/hooks/use-translation";
import type { ReactNode } from "react";

/**
 * 1 labelled M4 field (ADR-016 §Field help). The label key doubles as the help key: when
 * `abdm_nhpr_help_<key without abdm_>_what` exists in the locale, a question-mark icon shows the
 * 4-part help (title, what, how, example) written from the NHPR pages. Fields without help text
 * render the label alone, so a missing key never breaks a form.
 */

export default function NhprField({
  labelKey,
  label,
  htmlFor,
  children,
  hint,
  help,
  className,
}: {
  /** Locale key of the label; also selects the help text. */
  labelKey?: string;
  /** A ready label, for the few fields whose text is not a locale key. */
  label?: string;
  htmlFor?: string;
  children: ReactNode;
  hint?: string;
  help?: FieldHelpContent;
  className?: string;
}) {
  const { t } = useTranslation();
  const helpFor = useNhprHelp();
  const content = help ?? (labelKey ? helpFor(labelKey) : undefined);
  const text = label ?? (labelKey ? t(labelKey) : "");
  return (
    <div className={className ?? "grid gap-1.5"}>
      <div className="flex items-center gap-1">
        <Label htmlFor={htmlFor}>{text}</Label>
        {content && <FieldHelp {...content} />}
      </div>
      {children}
      {hint && <span className="text-muted-foreground text-xs">{hint}</span>}
    </div>
  );
}
