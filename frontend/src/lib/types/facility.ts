export type FacilityLike = {
  id: string;
  name?: string;
  extensions?: {
    abdm?: Record<string, unknown>;
  };
};
