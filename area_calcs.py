

def minimiser_area_calc(y_at_x2, y_at_x10):
    h = 8
    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (48 - area)
    return area_difference

def maximiser_area_calc(y_at_x2, y_at_x10):
    h = 8
    area = trapezium_area(y_at_x2, y_at_x10, h)
    area_difference = (area - 48)
    return area_difference

def crosser_area_calc(intercept, slope, x_intersect, y_at_x2, y_at_x10):
    y_intersect = (slope * x_intersect) + intercept

    h_left_trapezium = x_intersect - 2
    h_right_trapezium = 10 - x_intersect

    area_reality_line_left = trapezium_area(2, y_intersect, h_left_trapezium)
    area_reality_line_right = trapezium_area(y_intersect, 10, h_right_trapezium)

    area_reg_line_left = trapezium_area(y_at_x2, y_intersect, h_left_trapezium)
    area_reg_line_right = trapezium_area(y_intersect, y_at_x10, h_right_trapezium)

    area_left = area_reality_line_left - area_reg_line_left
    area_right = area_reg_line_right - area_reality_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def trapezium_area(a, b, h):
    a_plus_b_div_2 = (a + b) / 2
    area = a_plus_b_div_2 * h
    return area
