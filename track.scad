/*
=================================================================
  Parametric Roller Coaster Track Generator using BOSL2 Library
=================================================================
*/


// sudo sh -c 'echo "setenv OPENSCADPATH $HOME/Documents/OpenSCAD/libraries" >> /etc/launchd.conf'

// Use the BOSL2 standard library. Assumes it's in your library folder.
use <BOSL2/std.scad>;

// --- Include the processed spline data from your external file ---
// This file must contain an array called 'spline_path'
// Format: spline_path = [ [[pos],[fwd],[up]], [[pos],[fwd],[up]], ... ];
include <spline_data.scad>;


// ================================================================
//             PART 1: DATA PRE-PROCESSING FOR BOSL2
// ================================================================

// BOSL2's sweep function works best with separate lists for points and orientations.
// Let's create those from our single 'spline_path' array.
// path_points = [for(p=spline_path) p[0]]; // List of all [x,y,z] position vectors
// path_ups = [for(p=spline_path) p[2]];    // List of all [x,y,z] up vectors for roll/bank


// ================================================================
//                       PART 2: PARAMETERS
//            Adjust these values to change the track's look
// ================================================================

track_gauge = 50;         // Distance between the center of the running rails
rail_diameter = 6;        // Diameter of the running rails

crosstie_width = track_gauge + rail_diameter;
crosstie_height = 3;
crosstie_depth = 4;       // Thickness of the tie along the track's path
crosstie_spacing = 25;    // Desired distance between crossties

spine_width = 15;
spine_height = 10;
spine_y_offset = -15;     // How far below the crossties the spine sits (center to center)


// ================================================================
//               PART 3: COMPONENT & PROFILE MODULES
// ================================================================

// 2D Profile of the continuous parts (rails and spine) for sweeping.
module rails_and_spine_profile() {
    // Left Rail
    translate([-track_gauge/2, 0])
        circle(d=rail_diameter, $fn=24);
    // Right Rail
    translate([track_gauge/2, 0])
        circle(d=rail_diameter, $fn=24);
    // Central Spine
    translate([0, spine_y_offset])
        square([spine_width, spine_height], center=true);
}

// 3D Module for a single crosstie.
module crosstie() {
    // Main crosstie bar
    translate([0, -crosstie_height/2, -crosstie_depth/2])
        cube([crosstie_width, crosstie_height, crosstie_depth], center=true);

    // Vertical spine connector
    translate([0, (spine_y_offset+spine_height/2)/2, -crosstie_depth/2])
        cube([3, abs(spine_y_offset)-spine_height/2, crosstie_depth], center=true);
}


// ================================================================
//                       PART 4: MAIN LOGIC
//                 Generate the final track assembly
// ================================================================

// --- Generate the continuous Rails and Spine using sweep() ---

// Define profiles as lists of 2D points (BOSL2 sweep prefers paths/regions over primitives)
function make_circle_path(d, fn) = [for (i=[0:fn-1]) [d/2*cos(i*360/fn), d/2*sin(i*360/fn)]];
function make_rect_path(w, h) = [[-w/2, -h/2], [w/2, -h/2], [w/2, h/2], [-w/2, h/2]];

rail_poly = make_circle_path(rail_diameter, 24);
spine_poly = make_rect_path(spine_width, spine_height);

// Offset the polygons
left_rail_poly  = [for (p=rail_poly) p + [-track_gauge/2, 0]];
right_rail_poly = [for (p=rail_poly) p + [track_gauge/2, 0]];
spine_poly_offset = [for (p=spine_poly) p + [0, spine_y_offset]];

// Sweep them
color("silver") {
    sweep(transforms=track_transforms, shape=left_rail_poly);
    sweep(transforms=track_transforms, shape=right_rail_poly);
    sweep(transforms=track_transforms, shape=spine_poly_offset);
}


// --- Distribute the discrete Crossties along the path ---

color("dimgray")
for (m = crosstie_transforms) {
    multmatrix(m)
        crosstie();
}


// ================================================================
//                           VISUALIZATION
//           Uncomment one of these to see the components
// ================================================================

// rails_and_spine_profile();
// crosstie();