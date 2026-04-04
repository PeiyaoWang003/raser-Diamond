import argparse
import csv
import os
import re
import ROOT

ROOT.gROOT.SetBatch(True)


def sanitize_column_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^0-9a-zA-Z_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "value"


def find_canvas(root_file, canvas_name=None):
    f = ROOT.TFile.Open(root_file)
    if not f or f.IsZombie():
        raise RuntimeError(f"Cannot open ROOT file: {root_file}")

    if canvas_name:
        canvas = f.Get(canvas_name)
        if not canvas:
            raise RuntimeError(f"Cannot find canvas '{canvas_name}' in {root_file}")
        if not canvas.InheritsFrom("TCanvas") and not canvas.InheritsFrom("TPad"):
            raise RuntimeError(f"Object '{canvas_name}' is not a TCanvas/TPad")
        return f, canvas

    for key in f.GetListOfKeys():
        obj = key.ReadObj()
        if obj and (obj.InheritsFrom("TCanvas") or obj.InheritsFrom("TPad")):
            return f, obj

    raise RuntimeError("No TCanvas/TPad object found in file")


def legend_label_map(canvas):
    mapping = {}
    for prim in canvas.GetListOfPrimitives():
        if prim.InheritsFrom("TLegend"):
            for entry in prim.GetListOfPrimitives():
                obj = entry.GetObject()
                if obj:
                    mapping[obj.GetName()] = entry.GetLabel().strip()
    return mapping


def collect_unique_th1(canvas):
    histograms = []
    seen_names = set()
    for prim in canvas.GetListOfPrimitives():
        if prim.InheritsFrom("TH1") and not prim.InheritsFrom("TH2"):
            name = prim.GetName()
            if name in seen_names:
                continue
            seen_names.add(name)
            histograms.append(prim)
    return histograms


def same_binning(histograms):
    if not histograms:
        return False
    ref = histograms[0]
    n = ref.GetNbinsX()
    xmin = ref.GetXaxis().GetXmin()
    xmax = ref.GetXaxis().GetXmax()
    for h in histograms[1:]:
        if h.GetNbinsX() != n:
            return False
        if abs(h.GetXaxis().GetXmin() - xmin) > 1e-20:
            return False
        if abs(h.GetXaxis().GetXmax() - xmax) > 1e-20:
            return False
    return True


def preferred_sort_key(name_label_pair):
    name, label = name_label_pair
    label_norm = label.strip().lower()
    order = {"total": 0, "hole": 1, "electron": 2}
    return (order.get(label_norm, 999), label_norm, name)


def write_wide_csv(out_csv, histograms, label_map):
    # Sort using legend labels if available
    pairs = []
    for h in histograms:
        label = label_map.get(h.GetName(), h.GetTitle().strip() or h.GetName())
        pairs.append((h.GetName(), label))
    name_to_hist = {h.GetName(): h for h in histograms}
    ordered_names = [name for name, _ in sorted(pairs, key=preferred_sort_key)]
    ordered_histograms = [name_to_hist[n] for n in ordered_names]

    headers = ["bin", "x_low_s", "x_center_s", "x_high_s"]
    col_names = []
    for h in ordered_histograms:
        label = label_map.get(h.GetName(), h.GetTitle().strip() or h.GetName())
        col = sanitize_column_name(label) + "_A"
        if col in col_names:
            col = sanitize_column_name(h.GetName()) + "_A"
        col_names.append(col)
        headers.append(col)

    n_bins = ordered_histograms[0].GetNbinsX()
    xaxis = ordered_histograms[0].GetXaxis()

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in range(1, n_bins + 1):
            row = [
                i,
                f"{xaxis.GetBinLowEdge(i):.12e}",
                f"{xaxis.GetBinCenter(i):.12e}",
                f"{xaxis.GetBinUpEdge(i):.12e}",
            ]
            for h in ordered_histograms:
                row.append(f"{h.GetBinContent(i):.12e}")
            writer.writerow(row)

    print(f"Saved CSV: {out_csv}")
    print("Columns:", ", ".join(headers))
    print("\nCharge integrals (Integral(\"width\")):")
    for h, col in zip(ordered_histograms, col_names):
        charge = h.Integral("width")
        print(f"  {col}: {charge:.12e} C")


def write_separate_csvs(out_prefix, histograms, label_map):
    for h in histograms:
        label = label_map.get(h.GetName(), h.GetTitle().strip() or h.GetName())
        base = sanitize_column_name(label) or sanitize_column_name(h.GetName())
        out_csv = f"{out_prefix}_{base}.csv"
        xaxis = h.GetXaxis()
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["bin", "x_low_s", "x_center_s", "x_high_s", "value_A"])
            for i in range(1, h.GetNbinsX() + 1):
                writer.writerow([
                    i,
                    f"{xaxis.GetBinLowEdge(i):.12e}",
                    f"{xaxis.GetBinCenter(i):.12e}",
                    f"{xaxis.GetBinUpEdge(i):.12e}",
                    f"{h.GetBinContent(i):.12e}",
                ])
        print(f"Saved CSV: {out_csv}")


def main():
    parser = argparse.ArgumentParser(description="Export TH1 histograms drawn on a ROOT canvas to CSV.")
    parser.add_argument("root_file", help="Path to the input ROOT file")
    parser.add_argument("--canvas", default=None, help="Canvas name. If omitted, the first canvas is used.")
    parser.add_argument("--out", default=None, help="Output CSV path for wide table. Default: <root basename>.csv")
    args = parser.parse_args()

    f, canvas = find_canvas(args.root_file, args.canvas)
    label_map = legend_label_map(canvas)
    histograms = collect_unique_th1(canvas)

    if not histograms:
        raise RuntimeError("No TH1 histograms found on the canvas")

    out_base = os.path.splitext(os.path.basename(args.root_file))[0]
    out_csv = args.out or f"{out_base}.csv"

    print(f"Canvas: {canvas.GetName()} ({canvas.ClassName()})")
    print("Histograms found:")
    for h in histograms:
        label = label_map.get(h.GetName(), h.GetTitle().strip() or h.GetName())
        print(f"  {h.GetName()} -> {label}")

    if same_binning(histograms):
        write_wide_csv(out_csv, histograms, label_map)
    else:
        print("Histograms do not share the same binning; writing separate CSV files.")
        write_separate_csvs(out_base, histograms, label_map)

    f.Close()


if __name__ == "__main__":
    main()
