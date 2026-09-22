import { useEffect } from "react";

export interface PageHeadTitleProps {
  /** Already-translated page title; the " | Care" suffix is added here. */
  title: string;
}

/**
 * Sets `document.title` for a plug route, and restores the previous title on
 * unmount so the host's title survives navigation away.
 *
 * Mirrors the host's own component so plug pages read the same in the tab bar
 * and in the host's pinned-page dialog, which strips the " | CARE" suffix off
 * `document.title` (care_fe/src/components/Common/PageHeadTitle.tsx:7-21,
 * care_fe/src/components/Common/PinPageDialog.tsx:55, read 2026-09-22).
 *
 * The host only sets a title on its own routes and on nav tabs
 * (care_fe/src/components/ui/nav-tabs.tsx:159), never on a plug route, so a
 * plug page without this keeps whatever title the previous page left behind.
 */
export default function PageHeadTitle({ title }: PageHeadTitleProps) {
  useEffect(() => {
    const prevTitle = document.title;
    document.title = title ? `${title} | Care` : "Care";
    return () => {
      document.title = prevTitle;
    };
  }, [title]);

  return null;
}
