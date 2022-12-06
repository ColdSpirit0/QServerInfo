from colour import Color


def pick_by_sign(signed_value, left_pick, right_pick, zero_pick):
    if signed_value > 0:
        return right_pick

    elif signed_value < 0:
        return left_pick

    return zero_pick


def calculate_contrast_lightness(bg_lightness: float, fg_lightness: float, contrast_min: float):

    # get points on lightness gradient, like:
    #
    #       contrast                    contrast
    #        point            bg         point
    #        left          lightness     right
    #          │                │          │
    # 0├───────┼────────────────┼──────────┤1
    #          │                │          │
    #          │◄──────────────►│◄────────►│
    #               contrast      contrast
    #               distance      distance
    #                 left         right
    #

    contrast_point_left = max(bg_lightness - contrast_min, 0)
    contrast_point_right = min(bg_lightness + contrast_min, 1)

    # check is fg is contrast already - not in range between points
    if fg_lightness < contrast_point_left or fg_lightness > contrast_point_right:
        return None  # not modified

    # get distance from bg to points
    contrast_distance_left = bg_lightness - contrast_point_left
    contrast_distance_right = contrast_point_right - bg_lightness

    # check if one of distances is bigger, set it as final lightness value
    distance_diff = contrast_distance_right - contrast_distance_left

    # get most contrast point if they are different
    result = pick_by_sign(distance_diff, contrast_point_left, contrast_point_right, None)

    if result is not None:
        return result

    # get contrast points by bg to fg direction
    return pick_by_sign(fg_lightness - bg_lightness, contrast_point_left, contrast_point_right, contrast_point_right)


def get_contrast_color(bg_color: Color, fg_color: Color, contrast_min=0.1) -> Color:
    """find closest contrast color by move fg lightness value away from bg lightness value"""

    # copy color and change its lightness if required
    color = Color(fg_color)

    # color.luminance is lighntess from HSL by fact
    lightness = calculate_contrast_lightness(bg_color.luminance, fg_color.luminance, contrast_min)
    if lightness is not None:
        color.luminance = lightness

    return color
