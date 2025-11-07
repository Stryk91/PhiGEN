from __future__ import annotations
import os
import sys
import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

# Windows private font loading
FR_PRIVATE = 0x10
try:
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
    AddFontResourceExW = gdi32.AddFontResourceExW
    RemoveFontResourceExW = gdi32.RemoveFontResourceExW
except Exception:
    gdi32 = None
    AddFontResourceExW = None
    RemoveFontResourceExW = None

FONT_EXTS = {".ttf", ".otf", ".ttc", ".otc"}


def load_private_fonts(fonts_dir: Path, recursive: bool = True) -> list[Path]:
    """Load font files from fonts_dir as private fonts (Windows-only).
    Returns a list of files attempted to load (success not guaranteed for all TTC/OTC).
    """
    loaded: list[Path] = []
    if not fonts_dir.exists() or not fonts_dir.is_dir():
        return loaded

    def iter_files(root: Path):
        if recursive:
            for p in root.rglob("*"):
                if p.is_file() and p.suffix.lower() in FONT_EXTS:
                    yield p
        else:
            for p in root.iterdir():
                if p.is_file() and p.suffix.lower() in FONT_EXTS:
                    yield p

    for p in sorted(iter_files(fonts_dir)):
        try:
            if os.name == "nt" and AddFontResourceExW is not None:
                AddFontResourceExW(str(p), FR_PRIVATE, None)
            loaded.append(p)
        except Exception:
            # Continue; some complex collections may not fully register
            loaded.append(p)
    return loaded


def setup_theme(root: tk.Tk) -> None:
    # Neon-on-black palette to match the main app
    bg = "#0a0a0a"
    surface = "#111111"
    text = "#e6e6e6"
    accent = "#39ff14"

    root.configure(bg=bg)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=text)
    style.configure("TEntry", fieldbackground="#0f0f0f", foreground=text, insertcolor=accent)
    style.configure("TButton", background=surface, foreground=text, borderwidth=1)
    style.map("TButton", background=[("active", "#1a1a1a")])
    style.configure("Accent.TButton", background=accent, foreground="#000000")
    style.map("Accent.TButton", background=[("active", "#6aff3f"), ("pressed", "#2bd80f")])


class FontPreviewApp:
    def __init__(self, root: tk.Tk, families: list[str]):
        self.root = root
        setup_theme(self.root)
        self.root.title("Font Preview - PhiGEN")
        self.root.geometry("1000x740")
        self.root.minsize(720, 480)

        bg = "#0a0a0a"
        text = "#e6e6e6"

        header = ttk.Frame(root, padding=10)
        header.pack(fill="x")

        ttk.Label(header, text="Filter:").pack(side="left")
        self.filter_var = tk.StringVar()
        ent = ttk.Entry(header, textvariable=self.filter_var, width=28)
        ent.pack(side="left", padx=(6, 12))
        ent.focus_set()

        ttk.Label(header, text="Size:").pack(side="left")
        self.size_var = tk.IntVar(value=18)
        size_scale = ttk.Scale(header, from_=8, to=64, orient="horizontal",
                               command=lambda v: self.update_sizes(int(float(v))))
        size_scale.set(self.size_var.get())
        size_scale.pack(side="left", fill="x", expand=True, padx=(6, 12))

        reset_btn = ttk.Button(header, text="Reset", command=self.reset_controls)
        reset_btn.pack(side="left")

        # Scrollable container
        container = ttk.Frame(root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=vsb.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Build rows
        self.sample_line1 = "The quick brown fox jumps over the lazy dog"
        self.sample_line2 = "0123456789 !@#$%^&*()_+-=[]{};:'\",.<>/?"
        self.rows: list[tuple[str, ttk.Frame, tk.Label, tkfont.Font]] = []

        for fam in families:
            try:
                self._add_family_row(fam)
            except Exception:
                # Skip faulty faces
                pass

        # Wire events
        self.filter_var.trace_add("write", lambda *_: self.apply_filter())
        self.root.bind_all("<MouseWheel>", self._on_wheel)

        # Keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.root.quit())
        self.root.bind("<Control-f>", lambda e: ent.focus_set())

        # Keep consistent font sizes initially
        self.update_sizes(self.size_var.get())

    def _add_family_row(self, family: str) -> None:
        bg = "#0a0a0a"
        text = "#e6e6e6"

        frm = ttk.Frame(self.inner, padding=(8, 10))
        frm.pack(fill="x", pady=4)

        top = ttk.Frame(frm)
        top.pack(fill="x")
        name_font = tkfont.Font(family=family, size=14, weight="bold")
        ttk.Label(top, text=family, font=name_font).pack(side="left")
        ttk.Button(top, text="Copy name", command=lambda f=family: self.copy_name(f)).pack(side="right")

        sample_font = tkfont.Font(family=family, size=self.size_var.get())
        lbl1 = tk.Label(frm, text=self.sample_line1, bg=bg, fg=text, font=sample_font)
        lbl2 = tk.Label(frm, text=self.sample_line2, bg=bg, fg=text, font=sample_font)
        lbl1.pack(anchor="w")
        lbl2.pack(anchor="w")

        self.rows.append((family, frm, lbl1, sample_font))

    def apply_filter(self) -> None:
        q = self.filter_var.get().strip().lower()
        for fam, frm, _lbl, _fnt in self.rows:
            visible = (q in fam.lower()) if q else True
            if visible:
                frm.pack(fill="x", pady=4)
            else:
                frm.pack_forget()

    def update_sizes(self, size: int) -> None:
        self.size_var.set(size)
        for _fam, _frm, _lbl, fnt in self.rows:
            try:
                fnt.configure(size=size)
            except Exception:
                pass

    def copy_name(self, name: str) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(name)

    def reset_controls(self) -> None:
        self.filter_var.set("")
        self.update_sizes(18)

    def _on_wheel(self, event):
        # Standard Windows delta is 120 per notch
        delta_units = -1 * (event.delta // 120)
        self.canvas.yview_scroll(delta_units, "units")


def main(argv: list[str]) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Preview fonts in a folder (private load, Windows)")
    default_fonts_dir = str(Path(__file__).with_name("FONTS"))
    parser.add_argument("--fonts-dir", default=default_fonts_dir, help="Path to folder with fonts (ttf/otf/ttc/otc)")
    parser.add_argument("--no-recursive", action="store_true", help="Do not scan subfolders")
    args = parser.parse_args(argv)

    root = tk.Tk()

    # Families before
    before = set(tkfont.families(root))

    fonts_dir = Path(args.fonts_dir)
    load_private_fonts(fonts_dir, recursive=not args.no_recursive)

    # Refresh family list after loading
    after = set(tkfont.families(root))
    new_families = sorted(f for f in after - before)

    # If none detected as new, just display all (useful when fonts already installed)
    if not new_families:
        families_to_show = sorted(after)
    else:
        # Put newly loaded first, then others for convenience
        others = sorted(f for f in after if f not in new_families)
        families_to_show = new_families + others

    FontPreviewApp(root, families_to_show)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
