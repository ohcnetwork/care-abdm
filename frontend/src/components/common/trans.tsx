import { Trans as TransBase } from "react-i18next";

export const Trans = ({ ...props }: React.ComponentProps<typeof TransBase>) => {
  return <TransBase {...props} ns="care_abdm_fe" />;
};
