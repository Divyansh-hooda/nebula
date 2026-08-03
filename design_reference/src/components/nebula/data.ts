import {
  AppWindow,
  Bot,
  Boxes,
  Clipboard,
  Clock,
  Compass,
  FileText,
  FolderOpen,
  Home,
  LayoutGrid,
  Notebook,
  Search,
  Settings,
  Sparkles,
  Wand2,
  type LucideIcon,
} from "lucide-react";

export type NavItem = { label: string; icon: LucideIcon; badge?: string };

export const navGroups: { title: string; items: NavItem[] }[] = [
  {
    title: "Discover",
    items: [
      { label: "Home", icon: Home },
      { label: "Search", icon: Search, badge: "⌘K" },
      { label: "AI", icon: Sparkles, badge: "New" },
    ],
  },
  {
    title: "Library",
    items: [
      { label: "Files", icon: FileText },
      { label: "Apps", icon: AppWindow },
      { label: "Clipboard", icon: Clipboard },
      { label: "Notes", icon: Notebook },
    ],
  },
  {
    title: "Power",
    items: [
      { label: "Automation", icon: Wand2 },
      { label: "Browser", icon: Compass },
      { label: "Workspaces", icon: LayoutGrid },
      { label: "History", icon: Clock },
      { label: "Extensions", icon: Boxes },
      { label: "Settings", icon: Settings },
    ],
  },
];

export type ResultKind =
  | "Applications"
  | "Files"
  | "Folders"
  | "Images"
  | "Emails"
  | "Clipboard"
  | "Browser history"
  | "Calendar"
  | "Commands";

export type SearchResult = {
  id: string;
  kind: ResultKind;
  title: string;
  subtitle: string;
  meta: string;
  shortcut: string;
  accent: "primary" | "purple" | "cyan";
};

export const results: SearchResult[] = [
  {
    id: "r1",
    kind: "Files",
    title: "Quantum Physics — Lecture 07.pdf",
    subtitle: "~/Documents/University/Physics",
    meta: "PDF · 4.2 MB · 2d ago",
    shortcut: "↩",
    accent: "primary",
  },
  {
    id: "r2",
    kind: "Files",
    title: "Thermodynamics Problem Set.pdf",
    subtitle: "~/Downloads",
    meta: "PDF · 1.1 MB · 6d ago",
    shortcut: "⌘1",
    accent: "purple",
  },
  {
    id: "r3",
    kind: "Applications",
    title: "Visual Studio Code",
    subtitle: "/Applications",
    meta: "Opened 14 min ago",
    shortcut: "⌘2",
    accent: "cyan",
  },
  {
    id: "r4",
    kind: "Folders",
    title: "Physics Notes",
    subtitle: "~/iCloud Drive/Study",
    meta: "128 items",
    shortcut: "⌘3",
    accent: "primary",
  },
  {
    id: "r5",
    kind: "Images",
    title: "Screenshot 2026-07-29 at 14.03.png",
    subtitle: "~/Desktop/Screenshots",
    meta: "PNG · 2560×1600",
    shortcut: "⌘4",
    accent: "purple",
  },
  {
    id: "r6",
    kind: "Emails",
    title: "Re: Lab report deadline",
    subtitle: "Dr. Alvarez · Mail",
    meta: "Yesterday 09:12",
    shortcut: "⌘5",
    accent: "cyan",
  },
  {
    id: "r7",
    kind: "Clipboard",
    title: "curl -X POST https://api.nebula.app/v1/index",
    subtitle: "Copied from Terminal",
    meta: "37 min ago",
    shortcut: "⌘6",
    accent: "primary",
  },
  {
    id: "r8",
    kind: "Browser history",
    title: "Feynman lectures — Chapter 4",
    subtitle: "caltech.edu · Arc",
    meta: "Visited 3d ago",
    shortcut: "⌘7",
    accent: "purple",
  },
  {
    id: "r9",
    kind: "Commands",
    title: "Organize Downloads folder",
    subtitle: "Automation · 4 safe steps",
    meta: "Preview before run",
    shortcut: "⌘8",
    accent: "cyan",
  },
];

export const quickActions = [
  "Open",
  "Reveal in Finder",
  "Copy Path",
  "Summarize",
  "Translate",
  "Explain",
  "Generate Code",
  "Create Reminder",
  "Compress",
  "Share",
  "Rename",
  "Pin",
];

export const suggestions = [
  "Find my Physics PDF",
  "Summarize this document",
  "Show screenshots from last week",
  "Organize my Downloads folder",
  "Generate a Python script",
  "Translate these notes to Spanish",
];

export const recents = [
  { title: "Nebula Roadmap.md", meta: "Notes · 12m ago" },
  { title: "budget-2026.xlsx", meta: "Numbers · 1h ago" },
  { title: "onboarding-flow.fig", meta: "Figma · 3h ago" },
  { title: "server.ts", meta: "VS Code · yesterday" },
];

export const workflows = [
  { title: "Rename screenshots", meta: "Runs on Desktop", icon: Wand2 },
  { title: "Images → PDF", meta: "Batch convert", icon: FileText },
  { title: "Daily digest", meta: "AI summary at 9am", icon: Bot },
  { title: "Archive Downloads", meta: "Older than 30 days", icon: FolderOpen },
];

export const tabs = [
  "Search",
  "Chat",
  "Canvas",
  "Notes",
  "Browser",
  "Code",
  "Whiteboard",
  "PDF Reader",
];
