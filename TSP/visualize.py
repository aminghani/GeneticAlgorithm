import matplotlib.pyplot as plt

with open('TSP51.txt') as l:
    content = l.readlines()

data = {}
for d in content:
    city_id, x_coord, y_coord = d.split()
    city_id, x_coord, y_coord = int(city_id), int(x_coord), int(y_coord)
    data[city_id] = (x_coord, y_coord)

plt.rcParams["figure.figsize"] = (18, 12)


def plot_solution(list_cities, plot_title, num_plot, draw_plot=False, save_fig=True):
    plt.text(data[list_cities[-1]][0] - 0.015, data[list_cities[-1]][1] + 0.25,
             str(list_cities[-1]))
    for i in range(len(list_cities) - 1):
        city_1_number = list_cities[i]
        city_2_number = list_cities[i + 1]
        x_values = [data[city_1_number][0], data[city_2_number][0]]
        y_values = [data[city_1_number][1], data[city_2_number][1]]
        plt.plot(x_values, y_values, 'bo', linestyle="--")
        plt.text(data[city_1_number][0] - 0.015, data[city_1_number][1] + 0.25,
                 str(city_1_number))
    city_1_number = list_cities[-1]
    city_2_number = list_cities[0]
    x_values = [data[city_1_number][0], data[city_2_number][0]]
    y_values = [data[city_1_number][1], data[city_2_number][1]]
    plt.plot(x_values, y_values, 'bo', linestyle="--")
    plt.title(plot_title)
    if draw_plot:
        plt.show()
    if save_fig:
        plt.savefig("best_solution_plot" + str(num_plot) + ".jpg")


def plot_overall_distance_through_generations(overall_distance, draw_plot=False, save_fig=True):
    plt.plot(range(len(overall_distance)), overall_distance)
    if draw_plot:
        plt.show()
    if save_fig:
        plt.savefig("overall_distance.jpg")
