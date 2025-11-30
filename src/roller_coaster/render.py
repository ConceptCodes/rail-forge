import os
import subprocess


def render_segments(num_segments, openscad_path, output_dir, scad_file="track.scad"):
    if output_dir != ".":
        os.makedirs(output_dir, exist_ok=True)

    for i in range(num_segments):
        filename = f"track_segment_{i + 1:02d}_of_{num_segments:02d}.stl"
        output_file = os.path.join(output_dir, filename)
        print(f"Rendering {output_file}...")

        cmd = [openscad_path, "-o", output_file, "-D", f"segment_id={i}", scad_file]

        try:
            subprocess.run(cmd, check=True, capture_output=False)
        except FileNotFoundError:
            print(f"Error: OpenSCAD executable '{openscad_path}' not found.")
            break
        except subprocess.CalledProcessError as e:
            print(f"Error rendering segment {i}: {e}")
            break
    print("All renders complete.")
