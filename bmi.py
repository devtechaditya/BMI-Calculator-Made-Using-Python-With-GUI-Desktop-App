import tkinter as tk
from tkinter import font as tkfont
import math

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0f0f11"
SURFACE   = "#1a1a1f"
SURFACE2  = "#22222a"
BORDER    = "#2e2e38"
ACCENT    = "#6c63ff"
ACCENT2   = "#a78bfa"
TEXT      = "#f0eeff"
TEXT_SUB  = "#888899"
GRAD = [
    ("#4ade80", 18.5),   # green  – normal start
    ("#facc15", 25.0),   # yellow – overweight start
    ("#f97316", 30.0),   # orange – obese start
    ("#ef4444", 40.0),   # red    – morbidly obese
]

CAT_COLOR = {
    "Underweight":        "#60a5fa",
    "Normal weight":      "#4ade80",
    "Overweight":         "#facc15",
    "Obese (Class I)":    "#f97316",
    "Obese (Class II)":   "#ef4444",
    "Obese (Class III)":  "#dc2626",
}

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    if bmi < 25.0: return "Normal weight"
    if bmi < 30.0: return "Overweight"
    if bmi < 35.0: return "Obese (Class I)"
    if bmi < 40.0: return "Obese (Class II)"
    return "Obese (Class III)"

def lerp_color(c1, c2, t):
    def h(c): return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
    r1,g1,b1 = h(c1); r2,g2,b2 = h(c2)
    r = int(r1 + (r2-r1)*t); g = int(g1 + (g2-g1)*t); b = int(b1 + (b2-b1)*t)
    return f"#{r:02x}{g:02x}{b:02x}"

def bmi_bar_color(bmi):
    stops = [("#60a5fa", 15), ("#4ade80", 18.5), ("#facc15", 25), ("#f97316", 30), ("#ef4444", 40)]
    for i in range(len(stops)-1):
        c1,v1 = stops[i]; c2,v2 = stops[i+1]
        if v1 <= bmi <= v2:
            t = (bmi-v1)/(v2-v1)
            return lerp_color(c1, c2, t)
    return stops[-1][0]

# ── App ───────────────────────────────────────────────────────────────────────
class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._unit = tk.StringVar(value="metric")
        self._build_ui()
        self._center()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        W = 400

        # Header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=32, pady=(28, 0))
        tk.Label(hdr, text="BMI", font=("Helvetica", 28, "bold"),
                 fg=ACCENT2, bg=BG).pack(side="left")
        tk.Label(hdr, text=" Calculator", font=("Helvetica", 28),
                 fg=TEXT, bg=BG).pack(side="left")

        tk.Label(self, text="Body Mass Index — know your range",
                 font=("Helvetica", 11), fg=TEXT_SUB, bg=BG).pack(anchor="w", padx=32, pady=(2,18))

        # Unit toggle
        tog = tk.Frame(self, bg=SURFACE2, bd=0, highlightthickness=1,
                       highlightbackground=BORDER)
        tog.pack(padx=32, fill="x", pady=(0,20))
        self._metric_btn = self._toggle_btn(tog, "Metric  (kg / cm)", "metric")
        self._imperial_btn = self._toggle_btn(tog, "Imperial  (lb / ft)", "imperial")
        self._metric_btn.pack(side="left", expand=True, fill="both")
        self._imperial_btn.pack(side="left", expand=True, fill="both")

        # Input card
        card = tk.Frame(self, bg=SURFACE, bd=0, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(padx=32, fill="x")

        # Metric inputs
        self._metric_frame = tk.Frame(card, bg=SURFACE)
        self._metric_frame.pack(fill="x", padx=20, pady=20)
        self._h_m = self._input_row(self._metric_frame, "Height", "cm", 0)
        self._w_m = self._input_row(self._metric_frame, "Weight", "kg", 1)

        # Imperial inputs
        self._imperial_frame = tk.Frame(card, bg=SURFACE)
        self._ft  = self._input_row(self._imperial_frame, "Feet",   "ft", 0)
        self._in  = self._input_row(self._imperial_frame, "Inches", "in", 1)
        self._lbs = self._input_row(self._imperial_frame, "Weight", "lb", 2)

        # Calculate button
        self._calc_btn = tk.Button(
            self, text="Calculate BMI", font=("Helvetica", 13, "bold"),
            bg=ACCENT, fg="white", activebackground=ACCENT2, activeforeground="white",
            bd=0, pady=12, cursor="hand2", command=self._calculate,
            highlightthickness=0, relief="flat"
        )
        self._calc_btn.pack(padx=32, fill="x", pady=20)

        # Result area
        self._result_frame = tk.Frame(self, bg=BG)
        self._result_frame.pack(padx=32, fill="x")

        self._bmi_var   = tk.StringVar(value="—")
        self._cat_var   = tk.StringVar(value="")
        self._info_var  = tk.StringVar(value="")

        res_top = tk.Frame(self._result_frame, bg=BG)
        res_top.pack(fill="x")
        tk.Label(res_top, textvariable=self._bmi_var,
                 font=("Helvetica", 52, "bold"), fg=TEXT, bg=BG).pack(side="left")
        right = tk.Frame(res_top, bg=BG)
        right.pack(side="left", padx=14, pady=8)
        self._cat_label = tk.Label(right, textvariable=self._cat_var,
                                   font=("Helvetica", 14, "bold"), fg=ACCENT2, bg=BG, anchor="w")
        self._cat_label.pack(anchor="w")
        tk.Label(right, textvariable=self._info_var,
                 font=("Helvetica", 11), fg=TEXT_SUB, bg=BG, anchor="w",
                 wraplength=210, justify="left").pack(anchor="w", pady=(4,0))

        # BMI gauge bar (canvas)
        self._bar_canvas = tk.Canvas(self._result_frame, bg=BG, bd=0,
                                     highlightthickness=0, height=44)
        self._bar_canvas.pack(fill="x", pady=(8,0))
        self._draw_bar(None)

        # Stats row
        self._stats_frame = tk.Frame(self._result_frame, bg=BG)
        self._stats_frame.pack(fill="x", pady=(16, 28))
        self._stat_boxes = []
        for _ in range(2):
            b = tk.Frame(self._stats_frame, bg=SURFACE2, bd=0,
                         highlightthickness=1, highlightbackground=BORDER)
            b.pack(side="left", expand=True, fill="both",
                   padx=(0,8) if _ == 0 else (0,0))
            lbl = tk.Label(b, text="", font=("Helvetica", 10), fg=TEXT_SUB, bg=SURFACE2)
            lbl.pack(anchor="w", padx=14, pady=(12,0))
            val = tk.Label(b, text="", font=("Helvetica", 15, "bold"), fg=TEXT, bg=SURFACE2)
            val.pack(anchor="w", padx=14, pady=(2,12))
            self._stat_boxes.append((lbl, val))

        # Bind Enter key
        self.bind("<Return>", lambda e: self._calculate())

        # Init toggle state
        self._switch_unit()

    def _toggle_btn(self, parent, label, value):
        btn = tk.Button(parent, text=label, font=("Helvetica", 11),
                        bd=0, pady=8, cursor="hand2",
                        highlightthickness=0, relief="flat",
                        command=lambda: self._set_unit(value))
        self._style_toggle(btn, value == "metric")
        return btn

    def _style_toggle(self, btn, active):
        if active:
            btn.configure(bg=ACCENT, fg="white", activebackground=ACCENT2, activeforeground="white")
        else:
            btn.configure(bg=SURFACE2, fg=TEXT_SUB, activebackground=SURFACE, activeforeground=TEXT)

    def _set_unit(self, u):
        self._unit.set(u)
        self._switch_unit()

    def _switch_unit(self):
        is_metric = self._unit.get() == "metric"
        self._style_toggle(self._metric_btn, is_metric)
        self._style_toggle(self._imperial_btn, not is_metric)
        if is_metric:
            self._imperial_frame.pack_forget()
            self._metric_frame.pack(fill="x", padx=20, pady=20)
        else:
            self._metric_frame.pack_forget()
            self._imperial_frame.pack(fill="x", padx=20, pady=20)
        self._reset_result()

    def _input_row(self, parent, label, unit, row):
        tk.Label(parent, text=label, font=("Helvetica", 12),
                 fg=TEXT_SUB, bg=parent["bg"]).grid(
                     row=row, column=0, sticky="w", pady=8)
        var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=var, font=("Helvetica", 14),
                         bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
                         bd=0, highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=ACCENT, width=10, justify="center")
        entry.grid(row=row, column=1, padx=12, pady=8, ipady=8)
        tk.Label(parent, text=unit, font=("Helvetica", 12),
                 fg=TEXT_SUB, bg=parent["bg"]).grid(row=row, column=2, sticky="w")
        parent.columnconfigure(1, weight=1)
        return var

    # ── calculation ───────────────────────────────────────────────────────────
    def _calculate(self):
        try:
            if self._unit.get() == "metric":
                h_cm = float(self._h_m.get())
                w_kg = float(self._w_m.get())
                if h_cm <= 0 or w_kg <= 0: raise ValueError
                h_m = h_cm / 100
            else:
                ft  = float(self._ft.get()  or 0)
                ins = float(self._in.get()  or 0)
                lb  = float(self._lbs.get())
                h_m = (ft * 12 + ins) * 0.0254
                w_kg = lb * 0.453592
                if h_m <= 0 or w_kg <= 0: raise ValueError

            bmi = w_kg / (h_m ** 2)
            if not (5 < bmi < 100): raise ValueError

            cat   = bmi_category(bmi)
            color = CAT_COLOR.get(cat, TEXT)
            self._bmi_var.set(f"{bmi:.1f}")
            self._cat_var.set(cat)
            self._cat_label.configure(fg=color)

            # healthy range
            low_kg  = 18.5 * h_m**2
            high_kg = 24.9 * h_m**2
            if self._unit.get() == "imperial":
                lo = low_kg / 0.453592; hi = high_kg / 0.453592
                range_str = f"{lo:.0f} – {hi:.0f} lb"
                if bmi < 18.5:
                    diff = (low_kg - w_kg) / 0.453592
                    diff_str = f"Gain {diff:.1f} lb to reach normal"
                elif bmi > 25:
                    diff = (w_kg - high_kg) / 0.453592
                    diff_str = f"Lose {diff:.1f} lb to reach normal"
                else:
                    diff_str = "You're in the healthy range!"
            else:
                range_str = f"{low_kg:.1f} – {high_kg:.1f} kg"
                if bmi < 18.5:
                    diff_str = f"Gain {low_kg - w_kg:.1f} kg to reach normal"
                elif bmi > 25:
                    diff_str = f"Lose {w_kg - high_kg:.1f} kg to reach normal"
                else:
                    diff_str = "You're in the healthy range!"

            self._info_var.set(diff_str)
            self._stat_boxes[0][0].config(text="Healthy range")
            self._stat_boxes[0][1].config(text=range_str)
            self._stat_boxes[1][0].config(text="BMI range")
            self._stat_boxes[1][1].config(text="18.5 – 24.9")
            self._draw_bar(bmi)

        except (ValueError, ZeroDivisionError):
            self._reset_result()
            self._info_var.set("⚠  Please enter valid numbers.")

    def _reset_result(self):
        self._bmi_var.set("—")
        self._cat_var.set("")
        self._cat_label.configure(fg=ACCENT2)
        self._info_var.set("")
        for lbl, val in self._stat_boxes:
            lbl.config(text=""); val.config(text="")
        self._draw_bar(None)

    # ── gauge bar ─────────────────────────────────────────────────────────────
    def _draw_bar(self, bmi):
        c = self._bar_canvas
        c.delete("all")
        self.update_idletasks()
        W = c.winfo_width() or 336
        H = 44
        bh = 10; by = 16
        r = bh // 2

        # gradient segments
        stops = [("#60a5fa",15), ("#4ade80",18.5), ("#facc15",25), ("#f97316",30), ("#ef4444",40)]
        lo, hi = 12, 42

        def x_of(v):
            return r + (v - lo) / (hi - lo) * (W - 2*r)

        segs = 200
        for i in range(segs):
            t1 = i / segs; t2 = (i+1) / segs
            v1 = lo + t1*(hi-lo); v2 = lo + t2*(hi-lo)
            x1 = x_of(v1); x2 = x_of(v2)
            # find color
            col = stops[-1][0]
            for j in range(len(stops)-1):
                c1,s1 = stops[j]; c2,s2 = stops[j+1]
                if s1 <= (v1+v2)/2 <= s2:
                    col = lerp_color(c1, c2, ((v1+v2)/2 - s1)/(s2-s1))
                    break
            c.create_rectangle(x1, by, x2, by+bh, fill=col, outline=col)

        # rounded caps
        c.create_oval(x_of(lo)-r, by, x_of(lo)+r, by+bh,
                      fill=stops[0][0], outline=stops[0][0])
        c.create_oval(x_of(hi)-r, by, x_of(hi)+r, by+bh,
                      fill=stops[-1][0], outline=stops[-1][0])

        # tick labels
        for v, lbl in [(18.5,"18.5"), (25,"25"), (30,"30")]:
            xp = x_of(v)
            c.create_line(xp, by+bh+2, xp, by+bh+6, fill=BORDER)
            c.create_text(xp, by+bh+14, text=lbl, fill=TEXT_SUB,
                          font=("Helvetica", 9))

        # needle
        if bmi is not None:
            bmi_clamped = max(lo, min(hi, bmi))
            nx = x_of(bmi_clamped)
            col = bmi_bar_color(bmi)
            nw = 4; nh = 18
            c.create_rectangle(nx-nw//2, by-4, nx+nw//2, by+nh,
                                fill=col, outline="", width=0)
            c.create_oval(nx-nw, by-nw-4, nx+nw, by-4+nw,
                          fill=col, outline="")

if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()