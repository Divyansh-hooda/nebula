import { Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { navGroups } from "./data";

export function Sidebar({
  active,
  onSelect,
}: {
  active: string;
  onSelect: (label: string) => void;
}) {
  return (
    <aside className="flex h-full w-[236px] shrink-0 flex-col gap-6 border-r border-border/70 bg-sidebar/60 px-3 pb-4 pt-3 backdrop-blur-2xl">
      <div className="flex items-center gap-2.5 px-2">
        <span className="relative flex size-8 items-center justify-center rounded-xl bg-[image:var(--gradient-accent)] shadow-[var(--shadow-glow)]">
          <Sparkles className="size-4 text-primary-foreground" />
        </span>
        <div className="leading-tight">
          <p className="text-sm font-semibold tracking-tight">Nebula</p>
          <p className="text-[11px] text-muted-foreground">Operating companion</p>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-5 overflow-y-auto scroll-slim">
        {navGroups.map((group) => (
          <div key={group.title} className="space-y-1">
            <p className="px-3 pb-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-muted-foreground/70">
              {group.title}
            </p>
            {group.items.map((item) => {
              const isActive = active === item.label;
              return (
                <button
                  key={item.label}
                  onClick={() => onSelect(item.label)}
                  className={cn(
                    "group flex w-full items-center gap-2.5 rounded-xl px-3 py-2 text-[13px] font-medium transition-all duration-300",
                    isActive
                      ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-[var(--shadow-glass)]"
                      : "text-muted-foreground hover:bg-sidebar-accent/60 hover:text-foreground",
                  )}
                >
                  <item.icon
                    className={cn(
                      "size-4 transition-colors",
                      isActive ? "text-primary" : "text-muted-foreground group-hover:text-cyan",
                    )}
                  />
                  <span className="flex-1 text-left">{item.label}</span>
                  {item.badge ? (
                    <span className="rounded-md border border-border bg-glass px-1.5 py-0.5 text-[10px] text-muted-foreground">
                      {item.badge}
                    </span>
                  ) : null}
                </button>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="rounded-2xl border border-border bg-glass p-3">
        <div className="flex items-center gap-2 text-[11px] text-muted-foreground">
          <span className="size-1.5 rounded-full bg-mac-green animate-glow-pulse" />
          Indexing 482,109 items
        </div>
        <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground/80">
          On-device model active · 0 data leaves your Mac
        </p>
      </div>
    </aside>
  );
}
