import { useEffect, useState } from "react";
import {
  ArrowRight,
  Command,
  CornerDownLeft,
  Mic,
  Paperclip,
  Search,
  Sparkles,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  recents,
  results,
  suggestions,
  tabs,
  workflows,
  type SearchResult,
} from "./data";

const accentText: Record<SearchResult["accent"], string> = {
  primary: "text-primary",
  purple: "text-purple",
  cyan: "text-cyan",
};

function TabBar({ tab, onTab }: { tab: string; onTab: (t: string) => void }) {
  return (
    <div className="flex items-center gap-1 overflow-x-auto scroll-slim px-5 pt-3">
      {tabs.map((t) => (
        <button
          key={t}
          onClick={() => onTab(t)}
          className={cn(
            "shrink-0 rounded-lg px-3 py-1.5 text-xs font-medium transition-all duration-300",
            tab === t
              ? "bg-glass-strong text-foreground shadow-[var(--shadow-glass)]"
              : "text-muted-foreground hover:bg-glass hover:text-foreground",
          )}
        >
          {t}
        </button>
      ))}
    </div>
  );
}

function SearchField({
  query,
  onQuery,
}: {
  query: string;
  onQuery: (v: string) => void;
}) {
  return (
    <div className="group relative">
      <div className="pointer-events-none absolute -inset-px rounded-3xl bg-[image:var(--gradient-accent)] opacity-25 blur-lg transition-opacity duration-500 group-focus-within:opacity-60" />
      <div className="relative flex items-center gap-3 rounded-3xl border border-border bg-glass-strong px-5 py-4 backdrop-blur-3xl">
        <Search className="size-5 text-muted-foreground" />
        <input
          value={query}
          onChange={(e) => onQuery(e.target.value)}
          placeholder="Ask anything, find anything, do anything…"
          className="flex-1 bg-transparent text-[15px] outline-none placeholder:text-muted-foreground/70"
        />
        <button className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-glass hover:text-foreground">
          <Paperclip className="size-4" />
        </button>
        <button className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-glass hover:text-cyan">
          <Mic className="size-4" />
        </button>
        <kbd className="rounded-md border border-border bg-glass px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
          ⌘K
        </kbd>
      </div>
    </div>
  );
}

function AiAnswer({ query }: { query: string }) {
  const [chars, setChars] = useState(0);
  const text = `Found 3 physics documents indexed on this Mac. "Quantum Physics — Lecture 07.pdf" is the most relevant: 24 pages covering wavefunction collapse and the measurement problem. I can summarize it, extract the equations, or create a study note.`;

  useEffect(() => {
    setChars(0);
    const id = setInterval(() => {
      setChars((c) => (c >= text.length ? (clearInterval(id), c) : c + 3));
    }, 16);
    return () => clearInterval(id);
  }, [query, text.length]);

  return (
    <div className="animate-rise rounded-2xl border border-border bg-glass p-4">
      <div className="flex items-center gap-2 text-xs font-medium">
        <Sparkles className="size-3.5 text-purple" />
        <span className="text-gradient font-semibold">Nebula Intelligence</span>
        <span className="text-muted-foreground">· on-device · streaming</span>
      </div>
      <p className="mt-2.5 text-[13px] leading-relaxed text-secondary-foreground">
        {text.slice(0, chars)}
        <span className="ml-0.5 inline-block h-3.5 w-1.5 translate-y-0.5 rounded-sm bg-cyan animate-glow-pulse" />
      </p>
      <div className="mt-3 overflow-hidden rounded-xl border border-border bg-background/40">
        <div className="flex items-center justify-between border-b border-border px-3 py-1.5 text-[11px] text-muted-foreground">
          <span className="font-mono">summarize.py</span>
          <span>Python</span>
        </div>
        <pre className="overflow-x-auto scroll-slim p-3 font-mono text-[11.5px] leading-relaxed text-secondary-foreground">
{`from nebula import index, ai

doc = index.find("Physics Lecture 07")
print(ai.summarize(doc, style="study-notes"))`}
        </pre>
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {["Summarize", "Extract equations", "Create note", "Ask follow-up"].map((a) => (
          <button
            key={a}
            className="rounded-lg border border-border bg-glass px-2.5 py-1 text-[11px] text-secondary-foreground transition-all hover:border-ring hover:text-foreground"
          >
            {a}
          </button>
        ))}
      </div>
    </div>
  );
}

export function CenterPanel({
  selected,
  onSelect,
}: {
  selected: SearchResult;
  onSelect: (r: SearchResult) => void;
}) {
  const [tab, setTab] = useState("Search");
  const [query, setQuery] = useState("Find my Physics PDF");

  const filtered = results.filter((r) =>
    query.trim().length === 0
      ? true
      : `${r.title} ${r.subtitle} ${r.kind}`.toLowerCase().includes(query.toLowerCase()) ||
        query.length > 6,
  );

  const groups = Array.from(new Set(filtered.map((r) => r.kind)));

  return (
    <section className="flex h-full min-w-0 flex-1 flex-col">
      <TabBar tab={tab} onTab={setTab} />

      <div className="flex-1 overflow-y-auto scroll-slim px-5 pb-6 pt-4">
        <div className="mx-auto w-full max-w-[720px] space-y-5">
          <div>
            <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">
              Good morning, Alex
            </p>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight">
              Welcome back to <span className="text-gradient">Nebula</span>
            </h1>
          </div>

          <SearchField query={query} onQuery={setQuery} />

          <div className="flex flex-wrap gap-2">
            {suggestions.map((s) => (
              <button
                key={s}
                onClick={() => setQuery(s)}
                className="rounded-full border border-border bg-glass px-3 py-1.5 text-[11.5px] text-muted-foreground transition-all duration-300 hover:-translate-y-0.5 hover:border-ring hover:text-foreground"
              >
                {s}
              </button>
            ))}
          </div>

          <AiAnswer query={query} />

          {groups.map((group) => (
            <div key={group} className="space-y-1.5">
              <p className="px-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground/70">
                {group}
              </p>
              {filtered
                .filter((r) => r.kind === group)
                .map((r) => (
                  <button
                    key={r.id}
                    onClick={() => onSelect(r)}
                    className={cn(
                      "group flex w-full items-center gap-3 rounded-2xl border px-3.5 py-2.5 text-left transition-all duration-300",
                      selected.id === r.id
                        ? "border-ring bg-glass-strong shadow-[var(--shadow-glow)]"
                        : "border-transparent hover:border-border hover:bg-glass",
                    )}
                  >
                    <span
                      className={cn(
                        "flex size-9 shrink-0 items-center justify-center rounded-xl border border-border bg-glass text-[13px] font-semibold",
                        accentText[r.accent],
                      )}
                    >
                      {r.kind.slice(0, 1)}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block truncate text-[13.5px] font-medium">{r.title}</span>
                      <span className="block truncate text-[11.5px] text-muted-foreground">
                        {r.subtitle} · {r.meta}
                      </span>
                    </span>
                    <kbd className="hidden rounded-md border border-border bg-glass px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground sm:block">
                      {r.shortcut}
                    </kbd>
                    <ArrowRight className="size-4 -translate-x-1 text-muted-foreground opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:opacity-100" />
                  </button>
                ))}
            </div>
          ))}

          <div className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl border border-border bg-glass p-4">
              <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
                Pinned workflows
              </p>
              <div className="mt-3 space-y-2">
                {workflows.map((w) => (
                  <div key={w.title} className="flex items-center gap-2.5">
                    <w.icon className="size-4 text-purple" />
                    <div className="min-w-0">
                      <p className="truncate text-[12.5px] font-medium">{w.title}</p>
                      <p className="truncate text-[11px] text-muted-foreground">{w.meta}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-2xl border border-border bg-glass p-4">
              <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
                Recently opened
              </p>
              <div className="mt-3 space-y-2">
                {recents.map((r) => (
                  <div key={r.title} className="flex items-center justify-between gap-3">
                    <p className="truncate text-[12.5px] font-medium">{r.title}</p>
                    <p className="shrink-0 text-[11px] text-muted-foreground">{r.meta}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-border px-5 py-2 text-[11px] text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <Command className="size-3" /> Command palette
        </span>
        <span className="flex items-center gap-1.5">
          <CornerDownLeft className="size-3" /> Open · ⌘⌥ Quick actions · ⌃Space Voice
        </span>
      </div>
    </section>
  );
}
