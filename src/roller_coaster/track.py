from .geometry import vec_sub, vec_norm, vec_mag, vec_cross


def process_path_data(points):
    """
    Calculates Forward and Up vectors for each point.
    Returns list of [pos, fwd, up].
    """
    path_data = []

    if len(points) < 2:
        print("Error: Path must have at least 2 points")
        return []

    for i in range(len(points)):
        pos = points[i]

        # Calculate Forward (Tangent)
        if i < len(points) - 1:
            pos_next = points[i + 1]
            diff = vec_sub(pos_next, pos)
        else:
            prev_pos = points[i - 1]
            diff = vec_sub(pos, prev_pos)

        fwd = vec_norm(diff)

        if vec_mag(fwd) == 0:
            if i > 0 and len(path_data) > 0:
                fwd = path_data[-1][1]
            else:
                fwd = [1, 0, 0]

        # Calculate Up vector (Orthogonal)
        global_up = [0, 0, 1]
        right = vec_cross(fwd, global_up)

        if vec_mag(right) < 0.01:
            right = [1, 0, 0]
        else:
            right = vec_norm(right)

        ortho_up = vec_cross(right, fwd)
        up = vec_norm(ortho_up)

        path_data.append([pos, fwd, up])

    return path_data


def partition_path(path_data, max_length):
    """
    Splits the path into overlapping segments.
    Returns:
      segments: List of lists of [pos, fwd, up]
      segment_ranges: List of (start_dist, end_dist) tuples
      total_length: float
    """
    segments = []
    segment_ranges = []

    current_seg = [path_data[0]]
    seg_start_dist = 0
    current_seg_dist = 0
    total_dist = 0

    last_pos = path_data[0][0]

    for i in range(1, len(path_data)):
        p = path_data[i]
        step = vec_mag(vec_sub(p[0], last_pos))

        current_seg_dist += step
        total_dist += step
        last_pos = p[0]

        current_seg.append(p)

        # Check if we need to split (and ensure we aren't at the very end)
        if current_seg_dist >= max_length and i < len(path_data) - 1:
            segments.append(current_seg)
            segment_ranges.append((seg_start_dist, total_dist))

            # Start new segment with the current point (overlap)
            current_seg = [p]
            seg_start_dist = total_dist
            current_seg_dist = 0

    # Append the final segment
    segments.append(current_seg)
    segment_ranges.append((seg_start_dist, total_dist))

    return segments, segment_ranges, total_dist
