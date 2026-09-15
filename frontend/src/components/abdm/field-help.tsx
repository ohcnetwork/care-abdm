import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { CircleHelp } from "lucide-react";
import { useState } from "react";

export type FieldHelpContent = {
  title: string;
  what: string;
  how: string;
  example: string;
};

export default function FieldHelp({
  title,
  what,
  how,
  example,
  className,
}: FieldHelpContent & { className?: string }) {
  const [open, setOpen] = useState(false);

  return (
    <TooltipProvider delay={150}>
      <Tooltip open={open} onOpenChange={(next) => setOpen(next)}>
        <TooltipTrigger asChild>
          <Button
            type="button"
            variant="ghost"
            size="icon-xs"
            aria-label={title}
            className={cn(
              "text-muted-foreground hover:text-foreground size-5 shrink-0",
              className,
            )}
            onClick={(event) => {
              event.preventDefault();
              setOpen(true);
            }}
          >
            <CircleHelp className="size-4" />
          </Button>
        </TooltipTrigger>
        <TooltipContent
          side="top"
          align="start"
          className="grid max-w-xs gap-2 text-left text-xs leading-snug whitespace-normal"
        >
          <p className="font-semibold">{title}</p>
          <p>{what}</p>
          <p>{how}</p>
          <p>{example}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
