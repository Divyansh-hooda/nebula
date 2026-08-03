import { useEffect, useMemo, useState } from "react";
import { Search, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { results, suggestions } from "./data";

const commands = [
  ...suggestions.map((s) => ({ title: s, group: "AI & Natural language", hint: "↩" })),
  ...results.map((r) => ({ title: r.title, group: r.kind, hint: r.shortcut })),
  { title: "Open Settings", group: "Navigate", hint: "⌘," },
  { title: "New Workspace", group: "Navigate", hint: "⌘N" },
];

export function CommandPalette({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (o: boolean) => void;
}) {
  const [q, setQ] = useState("");
  const [index, setIndex] = useState(0);

  const filtered = useMemo(
    () => commands.filter((c) => c.title.toLowerCase().includes(q.toLowerCase())).slice(0, 8),
    [q],
  );

  useEffect(() => {
    if (!open) {
      setQ("");
      setIndex(0);
    }
  }, [open]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!open) return;
      if (e.key === "Escape") onOpenChange(false);
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setIndex((i) => Math.min(i + 1, filtered.length - 1));
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setIndex((i) => Math.max(i - 1, 0));
      }
      if (e.key === "Enter") onOpenChange(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, filtered.length, onOpenChange]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-background/50 px-4 pt-[16vh] backdrop-blur-sm"
      onClick={() => onOpenChange(false)}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="animate-rise w-full max-w-[620px] overflow-hidden rounded-3xl glass-strong"
      >
        <div className="flex items-center gap-3 border-b border-border px-5 py-4">
          <Search className="size-4 text-muted-foreground" />
          <input
            autoFocus
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setIndex(0);
            }}
            placeholder="Search everything, run commands, ask AI…"
            className="flex-1 bg-transparent text-[14px] outline-none placeholder:text-muted-foreground/70"
          />
          <kbd className="rounded-md border border-border bg-glass px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
            esc
          </kbd>
        </div>
        <div className="max-h-[45vh] overflow-y-auto scroll-slim p-2">
          {filtered.length === 0 ? (
            <p className="px-3 py-6 text-center text-[12.5px] text-muted-foreground">
              No matches — press ↩ to ask Nebula Intelligence
            </p>
          ) : (
            filtered.map((c, i) => (
              <button
                key={c.title}
                onMouseEnter={() => setIndex(i)}
                onClick={() => onOpenChange(false)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left transition-colors",
                  i === index ? "bg-glass-strong" : "hover:bg-glass",
                )}
              >
                <Sparkles
                  className={cn("size-3.5", i === index ? "text-cyan" : "text-muted-foreground")}
                />
                <span className="min-w-0 flex-1 truncate text-[13px]">{c.title}</span>
                <span className="shrink-0 text-[11px] text-muted-foreground">{c.group}</span>
                <kbd className="rounded-md border border-border bg-glass px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
                  {c.hint}
                </kbd>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
