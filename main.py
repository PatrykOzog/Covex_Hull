import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Covex:
    def __init__(self):
        self.number_of_points = 20
        self.x = np.random.randint(1, 99, self.number_of_points)
        self.y = np.random.randint(1, 99, self.number_of_points)
        self.x, self.y = zip(*sorted(zip(self.x, self.y), key=lambda x: x[0]))
        self.dx = np.random.randint(1, 99, self.number_of_points)
        self.dy = np.random.randint(1, 99, self.number_of_points)
        self.vec_x = self.dx - self.x
        self.vec_y = self.dy - self.y
        self.line_x = [self.x[0]]
        self.line_y = [self.y[0]]
        self.line_len = 20
        self.line_points_x = np.array([])
        self.line_points_y = np.array([])
        self.xx = self.x[0]
        self.yy = self.y[0]
        self.pre_x = self.x[1]
        self.pre_y = self.y[1]
        self.rounds = 0

    def draw(self):
        if self.rounds < 4:
            self.x, self.y, self.vec_x, self.vec_y = zip(*sorted(zip(self.x, self.y, self.vec_x, self.vec_y), key=lambda x: x[0]))
            self.vec_x = np.array(self.vec_x)
            self.vec_y = np.array(self.vec_y)
            plt.plot((self.xx, self.pre_x), (self.yy, self.pre_y), 'bo-')
            for i in range(len(self.x)):
                cross = np.cross(
                    [self.pre_x - self.xx, self.pre_y - self.yy],
                    [self.x[i] - self.xx, self.y[i] - self.yy])
                if cross >= 0:
                    self.pre_x = self.x[i]
                    self.pre_y = self.y[i]
                    plt.plot((self.xx, self.pre_x), (self.yy, self.pre_y), 'go-')

            next_vec_x, next_vec_y = self.pre_x - self.xx, self.pre_y - self.yy
            x3 = self.pre_x + self.line_len * next_vec_x / np.sqrt(next_vec_x**2 + next_vec_y**2) - next_vec_x
            y3 = self.pre_y + self.line_len * next_vec_y / np.sqrt(next_vec_x**2 + next_vec_y**2) - next_vec_y
            self.line_x.append(x3)
            self.line_y.append(y3)
            plt.plot(self.line_x, self.line_y, 'ro-')
            self.line_points_x = np.append(self.line_points_x, np.linspace(self.xx, x3, 20))
            self.line_points_y = np.append(self.line_points_y, np.linspace(self.yy, y3, 20))
            self.line_points_x = self.line_points_x.flatten()
            self.line_points_y = self.line_points_y.flatten()
            self.xx = x3
            self.yy = y3
            if np.isclose(self.xx, self.x[0], atol=self.line_len/2) and np.isclose(self.yy, self.y[0], atol=self.line_len/2):
                self.pre_x = self.x[1]
                self.pre_y = self.y[1]
                self.rounds = self.rounds + 1
                print('round')
            else:
                self.pre_x = self.x[0]
                self.pre_y = self.y[0]

        else:
            plt.plot(self.line_x, self.line_y, 'ro-')

    def move(self):
        if self.rounds < 4:
            self.x = self.x + self.vec_x/1000
            self.y = self.y + self.vec_y/1000

        else:
            for i in range(len(self.line_points_x)):
                index = np.where((np.isclose(self.line_points_x[i], self.x, atol=1)) & (np.isclose(self.line_points_y[i], self.y, atol=1)))
                self.vec_x[index] = -self.vec_x[index]
                self.vec_y[index] = -self.vec_y[index]
            self.x = self.x + self.vec_x / 100
            self.y = self.y + self.vec_y / 100
        plt.scatter(self.x, self.y)


covex = Covex()
fig, ax = plt.subplots()

# for i in range(200):
#     #print(i)
#     ax.clear()
#     plt.xlim(0, 100)
#     plt.ylim(0, 100)
#     covex.move()
#     covex.draw()
#     plt.show()

def frame(i):
    ax.clear()
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    covex.move()
    covex.draw()

anim = animation.FuncAnimation(fig, frame, frames=np.arange(1000), interval=5, repeat=False)
plt.show()