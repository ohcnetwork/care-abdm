import type { AbdmFailureBlock, AbdmRefusal } from "@/lib/careApi";
import { HttpError } from "@/lib/request";

/** Non-component exports of `failure-notice.tsx` (the fast-refresh rule keeps them apart). */

export type FailureNoticeProps = {
  title?: string;
  lines?: string[];
  code?: string;
  requestId?: string;
  className?: string;
};

/** The notice props for a stored failure block (`onboarding.failure`, `careContext.failure`). */
export function noticeFromFailure(
  failure: AbdmFailureBlock | null | undefined,
): FailureNoticeProps | null {
  if (!failure) return null;
  const lines = failure.details?.length
    ? failure.details
    : failure.detail
      ? [failure.detail]
      : [];
  return {
    // The registry's words stand on their own; the plug sentence only when there are none.
    title: lines.length
      ? undefined
      : `${failure.what} ${failure.nextStep}`.trim(),
    lines,
    code: failure.code,
    requestId: failure.supportReference,
  };
}

/** The notice props for a request the plug answered with a refusal body (`HttpError.cause`). */
export function noticeFromError(
  error: unknown,
  fallback: string,
): FailureNoticeProps {
  const cause =
    error instanceof HttpError
      ? (error.cause as Partial<AbdmRefusal> | undefined)
      : undefined;
  if (!cause || typeof cause.errors !== "string") {
    return { title: fallback };
  }
  const lines = cause.details?.length
    ? cause.details
    : cause.detail
      ? [cause.detail]
      : [];
  return {
    title: lines.length ? undefined : cause.errors,
    lines,
    code: cause.code,
    requestId: cause.requestId,
  };
}
