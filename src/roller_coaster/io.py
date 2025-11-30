import csv
from .geometry import get_matrix, vec_mag, vec_sub


def load_points_from_csv(filename):
    points = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                values = [float(x) for x in row if x.strip()]
                if len(values) >= 3:
                    points.append(values[:3])
            except ValueError:
                continue
    return points


def format_scad(segments, segment_ranges, total_dist, crosstie_spacing=25):
    lines = []

    # --- Track Segments ---
    lines.append("track_segments = [")
    for seg in segments:
        lines.append("  [")
        for p in seg:
            m = get_matrix(p[0], p[1], p[2])
            row_strs = []
            for row in m:
                row_strs.append(
                    f"[{row[0]:.4f},{row[1]:.4f},{row[2]:.4f},{row[3]:.4f}]"
                )
            lines.append(f"    [{','.join(row_strs)}],")
        lines.append("  ],")
    lines.append("];")
    lines.append("")

    # --- Crosstie Segments ---
    # We generate ties continuously, then bucket them into segments
    crosstie_segments = [[] for _ in segments]

    dist_cursor = 0
    # Add first tie at 0
    crosstie_positions = [0]

    while dist_cursor + crosstie_spacing <= total_dist:
        dist_cursor += crosstie_spacing
        crosstie_positions.append(dist_cursor)

    # Now assign to segments
    tie_idx = 0
    for seg_idx, (start_d, end_d) in enumerate(segment_ranges):
        seg_data = segments[seg_idx]

        # Check ties that might be at the very start of segment
        while tie_idx < len(crosstie_positions):
            target_dist = crosstie_positions[tie_idx]

            if target_dist < start_d - 0.001:
                # Tie was in previous segment
                tie_idx += 1
                continue

            if target_dist > end_d + 0.001:
                # Tie is in next segment
                break

            # Tie is in this segment range. Find matrix.
            target_local = target_dist - start_d

            best_p = seg_data[0]
            curr_d = 0
            found = False

            prev_p = seg_data[0]

            for i in range(1, len(seg_data)):
                p = seg_data[i]
                step = vec_mag(vec_sub(p[0], prev_p[0]))
                if curr_d + step >= target_local:
                    best_p = p
                    found = True
                    break
                curr_d += step
                prev_p = p

            if not found:
                best_p = seg_data[-1]

            crosstie_segments[seg_idx].append(
                get_matrix(best_p[0], best_p[1], best_p[2])
            )
            tie_idx += 1

    lines.append("crosstie_segments = [")
    for seg_ties in crosstie_segments:
        lines.append("  [")
        for m in seg_ties:
            row_strs = []
            for row in m:
                row_strs.append(
                    f"[{row[0]:.4f},{row[1]:.4f},{row[2]:.4f},{row[3]:.4f}]"
                )
            lines.append(f"    [{','.join(row_strs)}],")
        lines.append("  ],")
    lines.append("];")

    return "\n".join(lines), len(segments)
