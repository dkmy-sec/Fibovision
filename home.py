import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def draw_fibonacci_spiral(n_terms):
    fig, ax = plt.subplots(figsize=(6, 6))
    a, b = 0, 1
    x, y = 0, 0
    angle = 0
    ax.set_aspect('equal')
    ax.axis('off')

    for _ in range(n_terms):
        # Draw square
        square = plt.Rectangle((x, y), b, b, fill=False, edgecolor='blue')
        ax.add_patch(square)

        # Draw arc
        theta = np.linspace(np.radians(angle), np.radians(angle + 90), 100)
        r = b
        x_arc = x + b * np.cos(np.radians(angle))
        y_arc = y + b * np.sin(np.radians(angle))
        ax.plot(x_arc + r * np.cos(theta), y_arc + r * np.sin(theta), color='red')

        # Update variables
        x_new = x + b * np.cos(np.radians(angle))
        y_new = y + b * np.sin(np.radians(angle))
        a, b = b, a + b
        x, y = x_new, y_new
        angle += 90

    st.pyplot(fig)

def draw_phyllotaxis(n_points, c, angle):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    theta = np.radians(angle * np.arange(n_points))
    r = c * np.sqrt(np.arange(n_points))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    colors = np.linspace(0, 1, n_points)
    ax.scatter(x, y, c=colors, cmap='hsv', s=10)

    st.pyplot(fig)

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def draw_fibonacci_tree(x, y, angle, depth, max_depth, ax):
    if depth > max_depth:
        return
    length = fibonacci(depth) * 0.1
    x_new = x + length * np.cos(np.radians(angle))
    y_new = y + length * np.sin(np.radians(angle))
    ax.plot([x, x_new], [y, y_new], color='brown')
    # Recursively draw branches
    draw_fibonacci_tree(x_new, y_new, angle - 30, depth + 1, max_depth, ax)
    draw_fibonacci_tree(x_new, y_new, angle + 30, depth + 1, max_depth, ax)

def plot_fibonacci_tree(max_depth):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    draw_fibonacci_tree(0, 0, 90, 1, max_depth, ax)
    st.pyplot(fig)

def draw_fibonacci_snowflake(p1, p2, depth, ax):
    if depth == 0:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue')
        return
    # Calculate new points using Fibonacci ratios
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    dist = np.hypot(delta_x, delta_y)

    # Fibonacci ratios
    r1 = fibonacci(depth) / fibonacci(depth + 1)
    r2 = fibonacci(depth - 1) / fibonacci(depth + 1)

    # Points calculation
    pA = (p1[0] + r1 * delta_x, p1[1] + r1 * delta_y)
    pB = (p1[0] + r2 * delta_x, p1[1] + r2 * delta_y)

    # Middle triangle point
    angle = np.arctan2(delta_y, delta_x) - np.pi / 3
    pC = (pA[0] + dist * np.cos(angle) * r2, pA[1] + dist * np.sin(angle) * r2)

    # Recursive calls
    draw_fibonacci_snowflake(p1, pA, depth - 1, ax)
    draw_fibonacci_snowflake(pA, pC, depth - 1, ax)
    draw_fibonacci_snowflake(pC, pB, depth - 1, ax)
    draw_fibonacci_snowflake(pB, p2, depth - 1, ax)

def plot_fibonacci_snowflake(depth):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    # Start with an equilateral triangle
    p1 = (-0.5, 0)
    p2 = (0.5, 0)
    p3 = (0, np.sqrt(3)/2)
    draw_fibonacci_snowflake(p1, p2, depth, ax)
    draw_fibonacci_snowflake(p2, p3, depth, ax)
    draw_fibonacci_snowflake(p3, p1, depth, ax)
    st.pyplot(fig)

def draw_fibonacci_lsystem(axiom, rules, angle, length, depth):
    def lsystem(axiom, rules, depth):
        for _ in range(depth):
            axiom = ''.join([rules.get(c, c) for c in axiom])
        return axiom

    def draw_lsystem(commands, angle, length):
        stack = []
        x, y = 0, 0
        current_angle = 0

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for command in commands:
            if command == 'F':
                x_new = x + length * np.cos(np.radians(current_angle))
                y_new = y + length * np.sin(np.radians(current_angle))
                ax.plot([x, x_new], [y, y_new], color='green')
                x, y = x_new, y_new
            elif command == '+':
                current_angle += angle
            elif command == '-':
                current_angle -= angle
            elif command == '[':
                stack.append((x, y, current_angle))
            elif command == ']':
                x, y, current_angle = stack.pop()

        st.pyplot(fig)

    commands = lsystem(axiom, rules, depth)
    draw_lsystem(commands, angle, length)

def main():
    st.title("Fibonacci Fractal Visualizer")

    # Select Fractal Type
    fractal = st.selectbox("Select Fractal Type", [
        "Fibonacci Spiral",
        "Phyllotaxis Pattern",
        "Fibonacci Tree",
        "Fibonacci Snowflake",
        "Fibonacci L-System Fractal"
    ])

    if fractal == "Fibonacci Spiral":
        n_terms = st.slider("Number of Terms", min_value=1, max_value=20, value=5)
        if st.button("Draw"):
            draw_fibonacci_spiral(n_terms)

    elif fractal == "Phyllotaxis Pattern":
        n_points = st.slider("Number of Points", min_value=100, max_value=2000, value=500)
        c = st.slider("Scaling Factor (c)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
        angle = st.slider("Angle (degrees)", min_value=0.0, max_value=360.0, value=137.5, step=0.1)
        if st.button("Draw"):
            draw_phyllotaxis(n_points, c, angle)

    elif fractal == "Fibonacci Tree":
        depth = st.slider("Depth", min_value=1, max_value=10, value=5)
        if st.button("Draw"):
            plot_fibonacci_tree(depth)

    elif fractal == "Fibonacci Snowflake":
        depth = st.slider("Depth", min_value=0, max_value=5, value=2)
        if st.button("Draw"):
            plot_fibonacci_snowflake(depth)

    elif fractal == "Fibonacci L-System Fractal":
        depth = st.slider("Iterations", min_value=1, max_value=7, value=3)
        if st.button("Draw"):
            # Example L-system parameters
            axiom = "X"
            rules = {
                "X": "F+[[X]-X]-F[-FX]+X",
                "F": "FF"
            }
            angle_value = st.slider("Angle", min_value=0, max_value=360, value=25, step=1)
            length = 1 / (2 ** depth)
            draw_fibonacci_lsystem(axiom, rules, angle_value, length, depth)


if __name__ == "__main__":
    main()
