import matplotlib as mpl
mpl.get_configdir()
import matplotlib.pyplot as plt

plt.style.use('graspolator_style')

# Create figure
fig = plt.figure()
# Add subplot to figure
ax = fig.add_subplot(111)
plt.plot([2,4], [2,4])
# Show empty plot
plt.show()

def between_condition_pair(data_pair):
    x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b = utils.compute_area_calc_inputs(
        data_pair)
    group = utils.subject_group_reg_lines(x_intersect)

    if group == 'cross':
        total_area = reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a,
                                           y_at_x2_b,
                                           y_at_x10_b)
    else:
        total_area = reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b)
    return total_area

def compute_area_calc_inputs(data_pair):
    intercept_a, slope_a = utils.calculate_regression(data_pair.data_1)
    intercept_b, slope_b = utils.calculate_regression(data_pair.data_2)

    x2_a, x10_a, y_at_x2_a, y_at_x10_a = reg_line_endpoints(intercept_a, slope_a)
    x2_b, x10_b, y_at_x2_b, y_at_x10_b = reg_line_endpoints(intercept_b, slope_b)
    x_intersect, y_intersect = point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)

    return x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b