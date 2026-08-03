import { useEffect, useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { PanelRight, Search, SlidersHorizontal } from "lucide-react";
import { Sidebar } from "@/components/nebula/Sidebar";
import { CenterPanel } from "@/components/nebula/CenterPanel";
import { Inspector } from "@/components/nebula/Inspector";
import { CommandPalette } from "@/components/nebula/CommandPalette";
import { results, type SearchResult } from "@/components/nebula/data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Nebula — AI-Powered macOS Productivity Hub" },
      {
        name: "description",
        content:
          "Nebula is an AI operating companion for macOS: universal search, intelligent launcher, file preview, automation and assistant in one glass workspace.",
      },
      { property: "og:title", content: "Nebula — AI-Powered macOS Productivity Hub" },
      {
        property: "og:description",
        content:
          "Nebula is an AI operating companion for macOS: universal search, intelligent launcher, file preview, automation and assistant in one glass workspace.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: NebulaApp,
});

function NebulaApp() {
  const [active, setActive] = useState("Search");
  const [selected, setSelected] = useState<SearchResult>(results[0]!);
  const [paletteOpen, setPaletteOpen] = useState(false);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden p-4 md:p-8">
      <div className="pointer-events-none absolute -left-40 top-[-10%] size-[520px] animate-float rounded-full bg-purple/25 blur-[140px]" />
      <div className="pointer-events-none absolute -right-32 bottom-[-15%] size-[560px] animate-float rounded-full bg-cyan/15 blur-[150px] [animation-delay:-6s]" />

      <div className="animate-rise relative flex h-[min(88vh,900px)] w-full max-w-[1400px] flex-col overflow-hidden rounded-[26px] glass-strong">
        {/* Merged title bar */}
        <header className="flex items-center gap-4 border-b border-border/70 px-4 py-2.5">
          <div className="flex items-center gap-2">
            <span className="size-3 rounded-full bg-mac-red" />
            <span className="size-3 rounded-full bg-mac-yellow" />
            <span className="size-3 rounded-full bg-mac-green" />
          </div>
          <button
            onClick={() => setPaletteOpen(true)}
            className="mx-auto flex w-full max-w-[420px] items-center gap-2 rounded-xl border border-border bg-glass px-3 py-1.5 text-[12px] text-muted-foreground transition-all duration-300 hover:border-ring hover:text-foreground"
          >
            <Search className="size-3.5" />
            <span className="flex-1 text-left">{active} · Nebula</span>
            <kbd className="rounded-md border border-border px-1.5 font-mono text-[10px]">⌘K</kbd>
          </button>
          <div className="flex items-center gap-1 text-muted-foreground">
            <button className="rounded-lg p-1.5 transition-colors hover:bg-glass hover:text-foreground">
              <SlidersHorizontal className="size-4" />
            </button>
            <button className="rounded-lg p-1.5 transition-colors hover:bg-glass hover:text-foreground">
              <PanelRight className="size-4" />
            </button>
          </div>
        </header>

        <div className="flex min-h-0 flex-1">
          <Sidebar active={active} onSelect={setActive} />
          <CenterPanel selected={selected} onSelect={setSelected} />
          <Inspector item={selected} />
        </div>
      </div>

      <CommandPalette open={paletteOpen} onOpenChange={setPaletteOpen} />
    </main>
  );
}
