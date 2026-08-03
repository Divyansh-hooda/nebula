import { FileText, Share2, Star, Trash2 } from "lucide-react";
import { quickActions, type SearchResult } from "./data";

export function Inspector({ item }: { item: SearchResult }) {
  return (
    <aside className="hidden h-full w-[320px] shrink-0 flex-col gap-4 overflow-y-auto scroll-slim border-l border-border/70 bg-sidebar/50 p-4 backdrop-blur-2xl xl:flex">
      <div className="animate-rise rounded-2xl border border-border bg-glass p-3">
        <div className="relative flex h-40 items-center justify-center overflow-hidden rounded-xl border border-border bg-background/50">
          <div className="absolute inset-0 animate-float bg-[image:var(--gradient-accent)] opacity-20 blur-2xl" />
          <FileText className="relative size-10 text-cyan" />
        </div>
        <p className="mt-3 truncate text-[13.5px] font-semibold">{item.title}</p>
        <p className="truncate text-[11.5px] text-muted-foreground">{item.subtitle}</p>
      </div>

      <div className="rounded-2xl border border-border bg-glass p-3">
        <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
          Properties
        </p>
        <dl className="mt-2.5 space-y-1.5 text-[12px]">
          {[
            ["Kind", item.kind],
            ["Where", item.subtitle],
            ["Details", item.meta],
            ["Shortcut", item.shortcut],
            ["Indexed", "On-device · encrypted"],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between gap-3">
              <dt className="text-muted-foreground">{k}</dt>
              <dd className="max-w-[62%] truncate text-right text-secondary-foreground">{v}</dd>
            </div>
          ))}
        </dl>
      </div>

      <div className="rounded-2xl border border-border bg-glass p-3">
        <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
          Quick actions
        </p>
        <div className="mt-2.5 flex flex-wrap gap-1.5">
          {quickActions.map((a) => (
            <button
              key={a}
              className="rounded-lg border border-border bg-glass px-2 py-1 text-[11px] text-secondary-foreground transition-all duration-300 hover:-translate-y-0.5 hover:border-ring hover:text-foreground"
            >
              {a}
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-border bg-glass p-3">
        <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
          System activity
        </p>
        <div className="mt-3 space-y-3">
          {[
            ["Index freshness", 92],
            ["Model latency", 68],
            ["Storage reclaimed", 41],
          ].map(([label, value]) => (
            <div key={label as string}>
              <div className="flex justify-between text-[11px] text-muted-foreground">
                <span>{label}</span>
                <span>{value}%</span>
              </div>
              <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-secondary">
                <div
                  className="h-full rounded-full bg-[image:var(--gradient-accent)] transition-all duration-700"
                  style={{ width: `${value}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex gap-2">
        <button className="flex flex-1 items-center justify-center gap-1.5 rounded-xl border border-border bg-glass py-2 text-[12px] transition-colors hover:border-ring">
          <Star className="size-3.5 text-purple" /> Pin
        </button>
        <button className="flex flex-1 items-center justify-center gap-1.5 rounded-xl border border-border bg-glass py-2 text-[12px] transition-colors hover:border-ring">
          <Share2 className="size-3.5 text-cyan" /> Share
        </button>
        <button className="flex items-center justify-center rounded-xl border border-border bg-glass px-3 py-2 text-destructive transition-colors hover:border-destructive">
          <Trash2 className="size-3.5" />
        </button>
      </div>
    </aside>
  );
}
