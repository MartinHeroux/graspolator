import utils
from utils import return_subject_regression_line_type, \
    return_point_of_intersection_regression_line_and_reality_line, return_regression_line_endpoints


def trapezium(a, b, h):
    """
    Return the area of a trapezium

    Parameters
    ---------
    a: float
        one parallel side length of trapezium
    b: float
        one parallel side length of trapezium
    h: float
        perpendicular height of trapezium

    Returns
    -------
    float
        area of trapezium
    """
    a_plus_b_div_2 = (a + b) / 2
    area = a_plus_b_div_2 * h
    return area


def triangle(b, h):
    """
    Return the area of a right-angled triangle

    Parameters
    ---------
    b: float
        base length
    h: float
        perpendicular height of triangle

    Returns
    -------
    float
        area of triangle
    """
    area = (b * h) / 2
    return area


def between_regression_and_reality_absolute(actual_widths, perceived_widths, experiment):
    """
    Return the absolute area between a participant's regression line and the line of identity for a single
    experimental block

    Parameters
    ----------
        actual_widths: list
            actual widths presented to the participant in the current experimental block
        perceived_widths: list
            perceived widths reported by the participant in the current experimental block
        experiment: str
            name of current experiment

    Returns
    -------
        float
            absolute area between participant regression line and line of identity
    """
    intercept, slope = utils.calculate_regression_general(actual_widths, perceived_widths)
    x_intersect, y_intersect = return_point_of_intersection_regression_line_and_reality_line(intercept, slope)
    x1, x2, y_at_x1, y_at_x2 = return_regression_line_endpoints(actual_widths, perceived_widths, experiment)
    group = return_subject_regression_line_type(x_intersect, y_at_x1, experiment)

    if group == "crosser":
        area_left, area_right, area_total = _calculate_crosser_area(
            x_intersect, y_intersect, y_at_x1, y_at_x2, experiment
        )
    elif group == "crosser_triangle":
        area_left, area_right, area_total = _calculate_crosser_triangle_area(
            x_intersect, y_intersect, y_at_x1, y_at_x2, experiment
        )
    elif group == "minimiser":
        area_total = _calculate_minimiser_area(y_at_x1, y_at_x2, experiment)
    else:
        area_total = _calculate_maximiser_area(y_at_x1, y_at_x2, experiment)

    if experiment == "exp1":
        normalised_area = abs(area_total) / 9
    elif experiment == "exp2":
        normalised_area = abs(area_total) / 7

    return normalised_area


def between_regression_and_reality_signed(actual_widths, perceived_widths, experiment):
    """
    Return the signed area between a participant's regression line and the line of identity for a single
    experimental block

    Parameters
    ----------
        actual_widths: list
            actual widths presented to the participant in the current experimental block
        perceived_widths: list
            perceived widths reported by the participant in the current experimental block
        experiment: str
            name of current experiment

    Returns
    -------
        float
            absolute area between participant regression line and line of identity
    """
    intercept, slope = utils.calculate_regression_general(actual_widths, perceived_widths)
    x_intersect, y_intersect = return_point_of_intersection_regression_line_and_reality_line(intercept, slope)
    x2, x10, y_at_x2, y_at_x10 = return_regression_line_endpoints(actual_widths, perceived_widths, experiment)
    group = return_subject_regression_line_type(x_intersect, y_at_x2, experiment)

    if group == "crosser":
        area_total = _calculate_crosser_signed_area(x_intersect, y_intersect, y_at_x2, y_at_x10)
    elif group == "crosser_triangle":
        area_total = _calculate_crosser_triangle_signed_area(
            x_intersect, y_intersect, y_at_x2, y_at_x10
        )
    elif group == "minimiser":
        area_total = _calculate_minimiser_signed_area(y_at_x2, y_at_x10)
    else:
        area_total = _calculate_maximiser_signed_area(y_at_x2, y_at_x10)

    if experiment == "exp1":
        normalised_area_signed = (area_total) / 9
    elif experiment == "exp2":
        normalised_area_signed = (area_total) / 7

    return normalised_area_signed


def _calculate_crosser_area(x_intersect, y_intersect, y_at_smallest_actual_width, y_at_largest_actual_width, experiment):
    """
    Return the area between the line of identity and a regression line that crosses it
    
    Parameters
    ----------
        x_intersect: float
            x-axis point of intersection between regression line and line of identity
        y_intersect: float
            y-axis point of intersection between regression line and line of identity
        y_at_smallest_actual_width: float
            y-value of regression line where x = smallest actual presented width
        y_at_largest_actual_width: float
            y-value of regression line where x = largest actual presented width
        experiment: str
            name of experiment

    Returns
    -------
        float
            area between regression line and line of identity to the left of their intersection
        float
            area between regression line and line of identity to the right of their intersection
        float
            total area between regression line and line of identity
        
    """
    if experiment == "exp1":
        smallest_actual_width = 2
        largest_actual_width = 10
    elif experiment == "exp2":
        smallest_actual_width = 3
        largest_actual_width = 9
    else:
        SystemError("Incorrect experiment string provided")

    h_left_trapezium = x_intersect - smallest_actual_width
    h_right_trapezium = largest_actual_width - x_intersect

    area_reality_line_left = trapezium(smallest_actual_width, y_intersect, h_left_trapezium)
    area_reality_line_right = trapezium(y_intersect, largest_actual_width, h_right_trapezium)

    area_reg_line_left = trapezium(y_at_smallest_actual_width, y_intersect, h_left_trapezium)
    area_reg_line_right = trapezium(y_intersect, y_at_largest_actual_width, h_right_trapezium)

    if y_at_smallest_actual_width < smallest_actual_width:
        area_left = area_reality_line_left - area_reg_line_left
        area_right = area_reg_line_right - area_reality_line_right
    else:
        area_left = area_reg_line_left - area_reality_line_left
        area_right = area_reality_line_right - area_reg_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def _calculate_crosser_triangle_area(
    x_intersect, y_intersect, y_at_smallest_actual_width, y_at_largest_actual_width, experiment
):
    """
    Return the area between the line of identity and a regression line that crosses it, and crosses the y-axis
    below 0, forming a right angled triangle with the x-axis.

    Parameters
    ----------
        x_intersect: float
            x-axis point of intersection between regression line and line of identity
        y_intersect: float
            y-axis point of intersection between regression line and line of identity
        y_at_smallest_actual_width: float
            y-value of regression line where x = smallest actual presented width
        y_at_largest_actual_width: float
            y-value of regression line where x = largest actual presented width
        experiment: str
            name of experiment

    Returns
    -------
        float
            area between regression line and line of identity to the left of their intersection
        float
            area between regression line and line of identity to the right of their intersection
        float
            total area between regression line and line of identity

    """
    if experiment == "exp1":
        x1 = 2
        x2 = 10
    elif experiment == "exp2":
        x1 = 3
        x2 = 9
    else:
        SystemError("Incorrect experiment string provided")

    h_left_shapes = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    b_length = y_intersect + abs(y_at_smallest_actual_width)
    a_length_left = x1 + abs(y_at_smallest_actual_width)

    area_reality_line_left = trapezium(a_length_left, b_length, h_left_shapes)
    area_reality_line_right = trapezium(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = triangle(b_length, h_left_shapes)
    area_reg_line_right = trapezium(y_intersect, y_at_largest_actual_width, h_right_trapezium)

    area_left = area_reality_line_left - area_reg_line_left
    area_right = area_reg_line_right - area_reality_line_right

    area_difference = area_left + area_right

    return area_left, area_right, area_difference


def _calculate_minimiser_area(y_at_smallest_actual_width, y_at_largest_actual_width, experiment):
    """
    Return the area between the line of identity and a regression line that remains below the line of identity

    Parameters
    ----------
        y_at_smallest_actual_width: float
            y-value of regression line where x = smallest actual presented width
        y_at_largest_actual_width: float
            y-value of regression line where x = largest actual presented width
        experiment: str
            name of experiment

    Returns
    -------
        float
            total area between regression line and line of identity

    """
    if experiment == "exp1":
        h = 8
        whole_area = 48
    elif experiment == "exp2":
        h = 6
        whole_area = 36
    else:
        SystemError("Incorrect experiment string provided")

    area = trapezium(y_at_smallest_actual_width, y_at_largest_actual_width, h)
    area_difference = whole_area - area
    return area_difference


def _calculate_maximiser_area(y_at_smallest_actual_width, y_at_largest_actual_width, experiment):
    """
    Return the area between the line of identity and a regression line that remains above the line of identity

    Parameters
    ----------
        y_at_smallest_actual_width: float
            y-value of regression line where x = smallest actual presented width
        y_at_largest_actual_width: float
            y-value of regression line where x = largest actual presented width
        experiment: str
            name of experiment

    Returns
    -------
        float
            total area between regression line and line of identity
    """
    if experiment == "exp1":
        h = 8
        whole_area = 48
    elif experiment == "exp2":
        h = 6
        whole_area = 36
    else:
        SystemError("Incorrect experiment string provided")

    area = trapezium(y_at_smallest_actual_width, y_at_largest_actual_width, h)
    area_difference = area - whole_area
    return area_difference


def _calculate_minimiser_signed_area(y1, y2):
    h = 8
    whole_area = 48

    area = trapezium(y1, y2, h)
    area_total = (whole_area - area) * -1

    return area_total


def _calculate_maximiser_signed_area(y1, y2):
    h = 8
    whole_area = 48

    area = trapezium(y1, y2, h)
    area_total = area - whole_area
    return area_total


def _calculate_crosser_signed_area(x_intersect, y_intersect, y1, y2):
    x1 = 2
    x2 = 10

    h_left_trapezium = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    area_reality_line_left = trapezium(x1, y_intersect, h_left_trapezium)
    area_reality_line_right = trapezium(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = trapezium(y1, y_intersect, h_left_trapezium)
    area_reg_line_right = trapezium(y_intersect, y2, h_right_trapezium)

    if y1 <= x1:
        area_left = (area_reality_line_left - area_reg_line_left) * -1
        area_right = area_reg_line_right - area_reality_line_right
    else:
        area_left = area_reg_line_left - area_reality_line_left
        area_right = (area_reality_line_right - area_reg_line_right) * -1

    area_total = area_left + area_right

    return area_total


def _calculate_crosser_triangle_signed_area(x_intersect, y_intersect, y1, y2):
    x1 = 2
    x2 = 10

    h_left_shapes = x_intersect - x1
    h_right_trapezium = x2 - x_intersect

    b_length = y_intersect + abs(y1)
    a_length_left = x1 + abs(y1)

    area_reality_line_left = trapezium(a_length_left, b_length, h_left_shapes)
    area_reality_line_right = trapezium(y_intersect, x2, h_right_trapezium)

    area_reg_line_left = triangle(b_length, h_left_shapes)
    area_reg_line_right = trapezium(y_intersect, y2, h_right_trapezium)

    area_left = (area_reality_line_left - area_reg_line_left) * -1
    area_right = area_reg_line_right - area_reality_line_right

    area_total = area_left + area_right

    return area_total


